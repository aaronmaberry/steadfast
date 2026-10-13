import json,subprocess,pickle,sys,cv2,numpy as np
from PIL import Image,ImageDraw
FPS=24;W,H=1920,1080;P='/workspace/pp3/';L=P+'L/'
TL=json.load(open(P+'timeline.json'));TOTAL=TL[-1]['end'] if 'end' in TL[-1] else TL[-1]['t']+TL[-1]['d']+1.5
meta=pickle.load(open(L+'meta.pkl','rb'))
def dur(f):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def facebox(f):
    cap=cv2.VideoCapture(f);ok,fr=cap.read();h,w=fr.shape[:2]
    d=cv2.FaceDetectorYN.create('/workspace/pp2/tools/yunet.onnx','',(w,h),0.6);_,fs=d.detect(fr);x,y,fw,fh=fs[0][:4];return x+fw/2,y+fh/2,w,h
def frames(f,n,bw,bh):
    cx,cy,sw,sh=facebox(f);hh=min(sh,sh*0.92);ww=hh*bw/bh;x0=max(0,min(cx-ww/2,sw-ww));y0=max(0,min(cy-0.36*hh,sh-hh))
    vf=f'crop={int(ww)}:{int(hh)}:{int(x0)}:{int(y0)},scale={bw}:{bh},fps=24'
    p=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',vf,'-frames:v',str(n),'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    a=np.frombuffer(p,np.uint8).reshape(-1,bh,bw,3)
    if len(a)<n:a=np.concatenate([a,np.repeat(a[-1:],n-len(a),0)])
    return a
def rmask(w,h,r=36):
    m=Image.new('L',(w*2,h*2),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w*2-1,h*2-1),r*2,fill=255);return m.resize((w,h),Image.LANCZOS)
# build per-frame plan
nf=int(TOTAL*FPS);plan=[None]*nf
for x in TL:
    if x['kind']=='music':
        for i in range(int(x['t']*FPS),min(nf,int((x['t']+x['d'])*FPS))):plan[i]=('music',x.get('card','music'),0)
    else:
        a=int(round(x['t']*FPS));n=int(round(x['d']*FPS))
        for i in range(a,min(nf,a+n)):plan[i]=('line',x,i-a)
# fill gaps: hold previous line's last frame (short gaps only) else music card
last=None
for i in range(nf):
    if plan[i] is None:plan[i]=('hold',last,0) if last and last[0]=='line' else ('music','music',0)
    else:last=plan[i]
BASE={k:Image.open(L+k+'.png').convert('RGB') for k in set(x['lay'] for x in TL if x['kind']=='line')|{'music','end'}}
OV={k:Image.open(L+k+'_o.png') for k in BASE if k not in ('music','end')}
cache={};enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',P+'video_noaudio.mp4'],stdin=subprocess.PIPE)
prev=None;STILL=json.load(open(P+'stills.json')) if len(sys.argv)>1 else {}
for i,(k,x,j) in enumerate(plan):
    if k=='music':c=BASE[x or 'music'].copy()
    else:
        if k=='hold':x=x[1];j=None
        lay=x['lay'];b,h=meta[lay];bw,bh=b[2]-b[0],b[3]-b[1]
        if x['f'] not in cache:cache.clear();cache[x['f']]=frames(P+'av/'+x['f'],int(round(x['d']*FPS)),bw,bh)
        arr=cache[x['f']];fr=arr[-1] if j is None else arr[min(j,len(arr)-1)]
        c=BASE[lay].copy();c.paste(Image.fromarray(fr),(b[0],b[1]),rmask(bw,bh));c.paste(OV[lay],(0,0),OV[lay])
    if prev is not None and (k=='music')!=(prev[0]=='music'):xf=8;old=prev[1]
    if 'xf' in dir() and xf>0:c=Image.blend(c,old,xf/9);xf-=1
    if i<12:c=Image.blend(Image.new('RGB',(W,H)),c,i/12)
    if i>nf-18:c=Image.blend(Image.new('RGB',(W,H)),c,max(0,(nf-i)/18))
    prev=(k,c);enc.stdin.write(c.tobytes())
    if str(i) in STILL:c.save(P+'still-'+STILL[str(i)]+'.jpg',quality=92)
enc.stdin.close();enc.wait();print('done',TOTAL)
