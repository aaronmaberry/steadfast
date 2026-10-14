import sys,subprocess,os
src,bad,rep=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); W,H=1280,720; N=W*H*3
p=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
fr=[]
while True:
    b=p.stdout.read(N)
    if len(b)<N: break
    fr.append(b)
fr[bad]=fr[rep]; tmp=src[:-4]+'_fix.mp4'
e=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','25','-i','-','-i',src,'-map','0:v','-map','1:a','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','-c:a','copy',tmp],stdin=subprocess.PIPE)
for b in fr: e.stdin.write(b)
e.stdin.close(); e.wait(); os.rename(src,src[:-4]+'_orig.mp4'); os.rename(tmp,src); print('ok',len(fr))
