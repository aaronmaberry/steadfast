import json,subprocess,sys
def dur(f):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
LAY={'L00':'W_hook','L01':'J_hook','L02':'W_hook','L03':'W_intro','L04':'J_intro','L05':'W_q','L06':'J_sales','L07':'W_story','L08':'J_story','L09':'W_exit','L10':'J_hill','L11':'W_close','L12':'J_close'}
ORDER=sys.argv[1].split(',')
tl=[];t=0.5;GAP=0.45;INTRO=dur('LOCKED-intro.mp3');music_t=None
for n in ORDER:
    if n=='M':
        t+=0.4;music_t=t;tl.append(dict(kind='music',t=t,d=6.9));t+=6.9;continue  # voice enters on tail (~6.9s, after the power chord)
    if n=='O':outro_t=t-1.0;continue
    d=dur(f'audio/n/{n}.mp3');tl.append(dict(kind='line',f=n+'.mp4',a=f'audio/n/{n}.mp3',t=round(t,3),d=d,lay=LAY[n]));t+=d+GAP
OUT=dur('LOCKED-outro.mp3');vend=t-GAP
TOTAL=max(t+2.0,outro_t+OUT+0.3)
tl.append(dict(kind='music',card='end',t=t,d=TOTAL-t,end=TOTAL))
json.dump(tl,open('timeline.json','w'),indent=0)
ins=[];fl=[];k=0
for x in tl:
    if x['kind']!='line':continue
    ins+=['-i',x['a']];fl.append(f'[{k}]aresample=48000,adelay={int(x["t"]*1000)}:all=1[a{k}]');k+=1
vt=tl[[i for i,x in enumerate(tl) if x['kind']=='music'][0]+1]['t']
# intro: -18 LUFS alone (gain ~-2.6dB), ducked to ~-31 LUFS (15 dB under -16 voice) once voice enters, fade out by end of ring
ins+=['-i','LOCKED-intro.mp3']
fl.append(f"[{k}]aresample=48000,volume=-2.6dB,volume='if(lt(t,{vt-music_t:.2f}),1,max(0.18,1-(t-{vt-music_t:.2f})*3))':eval=frame,afade=t=out:st={INTRO-1.2:.2f}:d=1.2,adelay={int(music_t*1000)}:all=1[a{k}]");k+=1
ins+=['-i','LOCKED-outro.mp3']
a,b=vend-outro_t,vend-outro_t+1.5
fl.append(f"[{k}]aresample=48000,volume=-17dB,afade=t=in:d=1.0,volume='if(lt(t,{a:.2f}),1,min(5.0,1+(t-{a:.2f})*2.7))':eval=frame,adelay={int(outro_t*1000)}:all=1[a{k}]");k+=1
fl.append(''.join(f'[a{i}]' for i in range(k))+f'amix=inputs={k}:normalize=0,apad,atrim=0:{TOTAL:.2f}[out]')
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fl),'-map','[out]','-ac','2','-ar','48000','mix.wav'],check=True)
print('TOTAL',round(TOTAL,2),'voice-in',round(vt-music_t,2))
