import json,os,subprocess,sys,numpy as np
from PIL import Image
sys.argv=[sys.argv[0]]
import b5lib as B
W,H,FPS=1920,1080,30
D=json.load(open('durs.json'))
for k,a,b in [('C1',0,7.12),('C2',7.12,11.39),('C3',11.39,18.44)]: D[k]=round(b-a,2)
T=0.4
SEQ=[('W1','clip'),('W2','clip'),('W3','clip'),('B1','board','luke'),('W4','clip'),('W5','clip'),('W6','clip'),('W7','clip'),
     ('B2','board','point'),('walk1','walk'),('W8','clip'),('W9','clip'),('W10','clip'),('S1','split','door'),('S2','split','small'),
     ('W11','clip'),('W12','clip'),('W13','clip'),('W14','clip'),('walk2','walk'),('C1','clip'),('C2','clip'),('C3','clip'),('END','end')]
def vdur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def frames_of(f):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',f,'-r',str(FPS),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    info=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height','-of','csv=p=0',f],capture_output=True,text=True).stdout.split(',')
    w,h=int(info[0]),int(info[1])
    while True:
        b=p.stdout.read(w*h*3)
        if len(b)<w*h*3: break
        yield Image.frombytes('RGB',(w,h),b)
def enc(out):
    return subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
os.makedirs('v7/seg',exist_ok=True)
t=0; plan=[]; place=[]
for i,s in enumerate(SEQ):
    k,kind=s[0],s[1]
    if kind in('clip','split'): d=D[k]+T
    elif kind=='board': d=D[k]+T+(2.5 if k=='B2' else 0)
    elif kind=='walk': d=vdur(f'v7/shots/{k}.mp4')
    else: d=2.6
    nf=round(d*FPS); plan.append(dict(i=i,k=k,kind=kind,t0=round(t,3),dur=round(nf/FPS,3)))
    if kind in('clip','split','board'): place.append((k,round(t,3)))
    t+=nf/FPS
json.dump(plan,open('v7/timeline.json','w'),indent=0); json.dump(place,open('v7/place7.json','w'))
print('total',round(t,2))
def render(e):
    i,k,kind,t0,d=e['i'],e['k'],e['kind'],e['t0'],e['dur']; nf=round(d*FPS); out=f'v7/seg/{i:02d}.mp4'; P=enc(out); n=0
    last=None
    if kind=='board':
        for j in range(nf): P.stdin.write(B.board(SEQ[i][2],t0+j/FPS,j/FPS).tobytes())
        n=nf
    elif kind=='end':
        subprocess.run(f'rm -rf v7/endf; mkdir v7/endf; ffmpeg -v error -i /workspace/s01v4/shots/s21.mp4 v7/endf/%04d.png',shell=True); fs=sorted(os.listdir('v7/endf'))
        for j in range(nf): P.stdin.write(Image.open('v7/endf/'+fs[min(len(fs)-1,j)]).convert('RGB').resize((W,H)).tobytes())
        n=nf
    else:
        src=f'v7/shots/{k}.mp4'
        for fr in frames_of(src):
            if n>=nf: break
            lt=n/FPS
            if kind=='split':
                full=Image.new('RGB',(W,H)); full.paste(B.board(SEQ[i][2],t0+lt,lt,pw=W//2),(0,0))
                q=B.ease(lt/0.45) if k=='S1' else 1.0
                full.paste(fr,(W//2+int((1-q)*120),0)); from PIL import ImageDraw; ImageDraw.Draw(full).line((W//2,0,W//2,H),fill=(30,30,40),width=2); fr=full
            elif k=='W1': fr=B.lower_third(fr,lt)
            P.stdin.write(fr.tobytes()); last=fr; n+=1
        while n<nf: P.stdin.write(last.tobytes()); n+=1
    P.stdin.close(); P.wait(); print('v7/seg',i,k,flush=True)
if __name__=='__main__':
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(4) as ex: list(ex.map(render,plan))
