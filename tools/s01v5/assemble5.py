import subprocess,os,json
S=json.load(open('shots.json'))
open('concat.txt','w').write(''.join(f"file '{os.path.abspath(f'shots/s{i:02d}.mp4')}'\n" for i in range(len(S))))
OUT='/workspace/tmp-send/s01-anim-proof-v5'; os.makedirs(OUT,exist_ok=True)
m=f'{OUT}/S01-anim-proof-v5-master.mp4'; sh=f'{OUT}/S01-anim-proof-v5-share.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-i','mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-shortest',m],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',m,'-c:v','libx264','-preset','slow','-b:v','1900k','-maxrate','2400k','-bufsize','4800k','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',sh],check=True)
for f in (m,sh): print(f,round(os.path.getsize(f)/1e6,1),'MB',subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height','-of','csv=p=0',f],capture_output=True,text=True).stdout.split())
