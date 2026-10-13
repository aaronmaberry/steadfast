# v5 audio plan: pieces cut from v4 voice (proof_audio.wav, Option D) + new charge line
import json,subprocess,os
SRC='/workspace/s01anim/proof_audio.wav'; GAP=0.45
R={ # render: plate, pieces
 'R1':('80',[(135.3,139.3),(164.95,173.25)]),
 'R2':('81',[(174.6,184.0)]),
 'R3':('72',[(49.7,61.1),(61.8,69.9),(70.4,78.2)]),
 'R4':('89walk',[(96.2,105.7),(108.7,121.8)]),
 'R5':('77',[(19.3,27.5),(28.3,37.7)]),
 'R6':('73',[(9.4,18.5),(79.4,90.2),(91.5,94.9),(123.1,129.3)]),
 'R7':('89',[('charge',)]),
 'B1':(None,[(142.1,163.1)]),
 'B2':(None,[(38.6,48.5)]),
}
def build(k):
    pl,ps=R[k]; parts=[]; 
    for j,p in enumerate(ps):
        f=f'aud/{k}_{j}.wav'
        if p[0]=='charge': subprocess.run(['ffmpeg','-v','error','-y','-i','aud/charge.mp3','-ar','44100','-ac','1',f],check=True)
        else: subprocess.run(['ffmpeg','-v','error','-y','-ss',str(p[0]),'-to',str(p[1]),'-i',SRC,'-ar','44100','-ac','1','-af','afade=t=in:d=0.04,areverse,afade=t=in:d=0.08,areverse',f],check=True)
        parts.append(f)
    # concat with gaps
    inp=[];fc=''
    for j,f in enumerate(parts): inp+=['-i',f]
    inp+=['-f','lavfi','-t',str(GAP),'-i','anullsrc=r=44100:cl=mono']
    n=len(parts); seq=''
    for j in range(n): seq+=f'[{j}:a]'+ (f'[{n}:a]' if j<n-1 else '')
    cnt=2*n-1
    # anullsrc input can only be used once per graph; split it
    fc=f'[{n}:a]asplit={max(1,n-1)}'+''.join(f'[g{j}]' for j in range(max(1,n-1)))+';'
    seq=''.join(f'[{j}:a]'+(f'[g{j}]' if j<n-1 else '') for j in range(n))
    if n==1: fc=''; seq='[0:a]'; inp=inp[:2]
    fc+=f'{seq}concat=n={cnt}:v=0:a=1[o]'
    subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',fc,'-map','[o]','-b:a','192k',f'aud/{k}.mp3'],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'aud/{k}.mp3'],capture_output=True,text=True).stdout)
    return d
if __name__=='__main__':
    D={k:build(k) for k in R}; print(D); json.dump(D,open('durs.json','w'))
