import subprocess,re,json
def sil(f):
    o=subprocess.run(['ffmpeg','-i',f,'-af','silencedetect=noise=-40dB:d=0.7','-f','null','-'],capture_output=True,text=True).stderr
    s=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',o)];e=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',o)]
    return s,e
segs={}
for h in 'WJ':
    s,e=sil(h+'.mp3');dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',h+'.mp3']))
    st=[0]+e;en=s+[dur];segs[h]=[]
    for i,(a,b) in enumerate(zip(st,en)):
        a=max(0,a-0.08);b=min(dur,b+0.15);fn=f'{h}{i:02d}.wav'
        # dry-ish: highpass, gate tails, light denoise
        af='highpass=f=80,agate=threshold=0.02:ratio=3:attack=5:release=120,afftdn=nr=8'
        if h=='W':af+=',equalizer=f=2500:t=q:w=1:g=1.5'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',h+'.mp3','-af',af,'-ar','48000','-ac','1',fn])
        segs[h].append([fn,round(b-a,3)])
L=[l.split('|')[0] for l in open('../script.txt') if l.strip()]
ci={'W':0,'J':0};tl=[];t=0.6
for k in L:
    fn,d=segs[k][ci[k]];ci[k]+=1
    tl.append(dict(h=k,f=fn,t=round(t,3),d=d));t+=d+0.18
json.dump(tl,open('timeline.json','w'),indent=0);print(round(t,1),'s total')
