import json,subprocess
A=json.load(open('place6.json')); TL=json.load(open('timeline.json')); T=TL[-1]['t0']+TL[-1]['dur']
inp=[]; fc=[]
for j,(k,t) in enumerate(A):
    inp+=['-i',f'aud/{k}.wav']; fc.append(f'[{j}:a]aresample=48000,aformat=channel_layouts=mono,adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={T}[v{j}]')
n=len(A)
bed=("sine=f=110:d=%.2f,volume=0.5[s1];sine=f=164.81:d=%.2f,volume=0.35[s2];sine=f=220:d=%.2f,volume=0.25[s3];sine=f=277.18:d=%.2f,volume=0.18[s4];"
     "anoisesrc=c=pink:d=%.2f:a=0.05,lowpass=f=500[nz];[s1][s2][s3][s4][nz]amix=inputs=5:normalize=0,tremolo=f=0.12:d=0.35,lowpass=f=900,"
     "aresample=48000,volume=0.2,afade=t=in:d=2.5,afade=t=out:st=%.2f:d=3[bed]")%(T,T,T,T,T,T-3)
fc.append(bed)
fc.append(''.join(f'[v{j}]' for j in range(n))+f'amix=inputs={n}:normalize=0[vox]')
fc.append('[vox][bed]amix=inputs=2:normalize=0,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[out]','-t',str(T),'-ar','48000','mix.wav'],check=True)
print(subprocess.run(['ffmpeg','-i','mix.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr[-300:])
