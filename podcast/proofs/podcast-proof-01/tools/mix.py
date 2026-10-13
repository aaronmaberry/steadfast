import json,subprocess
P='/workspace/pp1/';T0=5.0;TOTAL=174.0
tl=json.load(open(P+'audio/timeline.json'))
M='/workspace/biblical-manhood/studio/podcast-show/episodes/E001/music/'
ins=['-f','lavfi','-t',str(TOTAL),'-i','anullsrc=r=48000:cl=mono']
fl=[];n=1
for x in tl:
    ins+=['-i',P+'audio/'+x['f']];d=int((T0+x['t'])*1000)
    fl.append(f'[{n}]adelay={d},apad=whole_dur={TOTAL}[a{n}]');n+=1
ins+=['-i',M+'theme-D-sting-3s.wav'];fl.append(f'[{n}]aformat=channel_layouts=mono,volume=0.55,apad=whole_dur={TOTAL}[a{n}]');n+=1
ins+=['-i',M+'theme-D-outro-bed_E001-levels.wav'];s=T0+163-1
fl.append(f'[{n}]aformat=channel_layouts=mono,atrim=0,afade=t=in:d=1.5,volume=0.5,adelay={int(s*1000)},afade=t=out:st={TOTAL-3}:d=3,apad=whole_dur={TOTAL}[a{n}]');n+=1
fl.append('[0]'+''.join(f'[a{i}]' for i in range(1,n))+f'amix=inputs={n}:normalize=0,atrim=0:{TOTAL},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[out]')
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fl),'-map','[out]','-ac','2','-c:a','pcm_s16le',P+'build/mix.wav'],check=True)
print('ok')
