import os
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets')+'/'
import subprocess
wh=[2.5,9.05,17.65,27.05,36.3,42.3]; hit=[0.0,19.3,39.3,42.4]
inputs=['-i','video.mp4','-i','vo.mp3','-i',A+'music.mp3']; fc=[]; mix=['[vo]','[mu]']
fc.append('[1]apad=pad_dur=2,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80[vo]')
fc.append('[2]atrim=0:44,afade=t=in:d=0.4,afade=t=out:st=42.6:d=1.4,volume=0.12[mu]')
n=3
for i,t in enumerate(wh):
    inputs+=['-i',A+'whoosh.mp3']; fc.append(f'[{n}]volume=0.22,adelay={int(t*1000)}|{int(t*1000)}[w{i}]'); mix.append(f'[w{i}]'); n+=1
for i,t in enumerate(hit):
    inputs+=['-i',A+'hit.mp3']; fc.append(f'[{n}]volume=0.30,lowpass=f=900,adelay={int(t*1000)}|{int(t*1000)}[h{i}]'); mix.append(f'[h{i}]'); n+=1
fc.append(''.join(mix)+f'amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[o]')
subprocess.run(['ffmpeg','-y','-loglevel','error']+inputs+['-filter_complex',';'.join(fc),'-map','0:v','-map','[o]','-c:v','copy','-c:a','aac','-b:a','192k','-t','44','-movflags','+faststart','../steadfast-daily-2026-10-12-v4.mp4'],check=True)
