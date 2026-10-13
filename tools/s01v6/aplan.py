import json,subprocess
SRC='/workspace/s01anim/proof_audio.wav'
P={ # shot audio: list of (t0,t1) from v5/v4 voice; 'C' = v5 charge file ranges
 'W1':[(135.3,139.6),(164.95,166.6)],'W2':[(167.3,173.25)],'W3':[(174.6,183.9)],
 'W4':[(49.7,55.2)],'W5':[(55.9,61.1)],'W6':[(61.8,69.9)],'W7':[(70.4,78.2)],
 'W8':[(96.2,105.7)],'W9':[(108.7,116.1)],'W10':[(117.4,121.8)],
 'S1':[(19.3,27.5)],'S2':[(28.3,37.7)],
 'W11':[(9.4,18.5)],'W12':[(79.4,85.42)],'W13':[(85.5,90.2)],'W14':[(91.5,94.9),(123.1,129.3)],
 'B1':[(142.1,163.1)],'B2':[(38.6,48.5)],
}
D={}
def cut(k,ps):
    fs=[]
    for j,(a,b) in enumerate(ps):
        f=f'aud/{k}_{j}.wav'; subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',SRC,'-ar','44100','-ac','1','-af','afade=t=in:d=0.04,areverse,afade=t=in:d=0.08,areverse',f],check=True); fs.append(f)
    if len(fs)>1:
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-t','0.45','-i','anullsrc=r=44100:cl=mono','aud/gap.wav'],check=True)
        lst=[]; 
        for j,f in enumerate(fs): lst+= [f] + (['aud/gap.wav'] if j<len(fs)-1 else [])
        open('aud/l.txt','w').write(''.join(f"file '{x.split('/')[-1]}'\n" for x in lst))
        subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','aud/l.txt',f'aud/{k}.wav'],check=True)
    else: subprocess.run(['cp',fs[0],f'aud/{k}.wav'])
for k,ps in P.items(): cut(k,ps)
# charge (v5 new line): split on pauses into 3 shots
subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/s01v5/aud/charge.mp3','-ar','44100','-ac','1','aud/charge.wav'],check=True)
o=subprocess.run(['ffmpeg','-i','aud/charge.wav','-af','silencedetect=n=-38dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
import re; st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',o)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',o)]
print('charge silences',list(zip(st,en)))
json.dump({'sil':list(zip(st,en))},open('aud/charge_sil.json','w'))
for k in list(P): D[k]=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'aud/{k}.wav'],capture_output=True,text=True).stdout)
json.dump(D,open('durs.json','w')); print(D)
