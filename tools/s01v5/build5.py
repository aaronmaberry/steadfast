# S01 proof v5 builder: clean boards (kicker + one line, no grid/brackets/footer/ghost/word-by-word), HeyGen clips, split, walk comp
import json,math,os,sys,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont
W,H,FPS=1920,1080,30
A='/workspace/steadfast/social-daily/assets/'; FL,FM=A+'Geist-Light.ttf',A+'Geist-Medium.ttf'
TEXT=(244,244,245); ACC=(139,156,255); BG=(7,7,10); PA=(91,110,245); PB=(80,40,160)
_f={}
def F(n,s):
    if (n,s) not in _f: _f[(n,s)]=ImageFont.truetype(n,s)
    return _f[(n,s)]
ease=lambda x:1-(1-max(0.,min(1.,x)))**3
rng=np.random.default_rng(5); GRAIN=[rng.normal(0,2.0,(H,W,1)).astype(np.float32) for _ in range(6)]
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.36*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)/2)[...,None].astype(np.float32)
BOARDS={
 'luke':('LUKE 16:10',"Whoever can be trusted with very little can also be trusted with much.",62),
 'point':('THE POINT',"Name the day. Then show up for it.",76),
 'door':('WEEK ONE',"The first step is just walking through the door.",56),
 'small':('THE POINT',"Small, faithful, ordinary. That is where a man is built.",52),
}
def glow(t,pw):
    a=np.zeros((135,240,3),np.float32)+np.array(BG,np.float32); Y,X=np.mgrid[0:135,0:240]
    for (cx,cy,r,col,ph) in [(0.3,0.35,0.6,PA,0),(0.75,0.7,0.5,PB,2)]:
        cx2=cx+0.05*math.sin(t*0.12+ph); cy2=cy+0.04*math.cos(t*0.1+ph)
        d=np.sqrt(((X/240-cx2)*1.78)**2+(Y/135-cy2)**2)/r
        a+=np.clip(1-d,0,1)[...,None]**2*np.array(col,np.float32)*0.16
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).resize((pw,H),Image.BICUBIC)
def wrap(text,font,maxw):
    lines=[[]]
    for w in text.split():
        if font.getlength(' '.join(lines[-1]+[w]))>maxw and lines[-1]: lines.append([w])
        else: lines[-1].append(w)
    return [' '.join(l) for l in lines]
def board(key,t,lt,pw=W):
    kick,text,size=BOARDS[key]
    if pw<W: size=int(size*0.82)
    img=glow(t,pw).convert('RGBA'); lay=Image.new('RGBA',(pw,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    q=ease(lt/0.6); q2=ease((lt-0.35)/0.8); cx=pw/2
    ft=F(FL,size); lines=wrap(text,ft,1250 if pw==W else pw-170); lh=int(size*1.34)
    y=(H-len(lines)*lh)/2+30
    fe=F(FM,30 if pw==W else 24); tr=7 if pw==W else 6; ew=sum(fe.getlength(c)+tr for c in kick)-tr; ex=cx-ew/2; ey=y-95
    for c in kick: d.text((ex,ey+8*(1-q)),c,font=fe,fill=ACC+(int(240*q),)); ex+=fe.getlength(c)+tr
    for ln in lines:
        d.text((cx-ft.getlength(ln)/2,y+12*(1-q2)),ln,font=ft,fill=TEXT+(int(255*q2),)); y+=lh
    img.alpha_composite(lay); return img.convert('RGB')
class Clip:
    def __init__(s,d):
        s.d=d; s.n=len(os.listdir(d)); s.fps=25
    def get(s,t): return Image.open(f'{s.d}/%05d.png'%min(s.n,max(1,int(t*s.fps)+1))).convert('RGB')
def grade(im):
    arr=np.asarray(im).astype(np.float32); w=arr.shape[1]
    arr=np.clip((arr-10)*1.05,0,None)*VIG[:,(W-w)//2:(W-w)//2+w]+GRAIN[int(1e3*arr[5,5,0])%6][:,:w]
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
def crop(im,z,fx,fy,box_w=W):
    if im.size!=(W,H): im=im.resize((W,H),Image.LANCZOS)
    ch=H/z; cw=ch*box_w/H; x0=min(max(0,fx*W-cw/2),W-cw); y0=min(max(0,fy*H-ch/2),H-ch)
    return im.resize((box_w,H),Image.BICUBIC,box=(x0,y0,x0+cw,y0+ch))
def lower_third(img,t):
    if not 1.5<=t<5.5: return img
    q=min(ease((t-1.5)/0.5),ease((5.5-t)/0.5)); im=img.convert('RGBA'); lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    x=110+int(-30*(1-q)); y=H-250
    d.rectangle((x-30,y-20,x+460,y+92),fill=(7,7,10,int(140*q))); d.rectangle((x-30,y-20,x-26,y+92),fill=ACC+(int(255*q),))
    d.text((x,y-6),'Wes Hart',font=F(FM,44),fill=TEXT+(int(255*q),)); d.text((x,y+52),'STEADFAST MEN',font=F(FM,20),fill=(200,200,208,int(220*q)))
    im.alpha_composite(lay); return im.convert('RGB')
PLAN=json.load(open('shots.json'))
def render(i):
    s=PLAN[i]; kind=s['kind']; nf=round(s['dur']*FPS); out=f'shots/s{i:02d}.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    clip=Clip(s['frames']) if 'frames' in s else None
    global ENDF
    if kind=='end':
        os.makedirs('endf',exist_ok=True); subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/s01v4/shots/s21.mp4','endf/%04d.png']); ENDF=sorted('endf/'+f for f in os.listdir('endf'))
    for k in range(nf):
        lt=k/FPS; t=s['t0']+lt; ct=s.get('c0',0)+lt; pr=k/max(1,nf-1)
        if kind=='end':
            fr=Image.open(ENDF[min(len(ENDF)-1,k)])
        elif kind=='board': fr=board(s['board'],t,lt)
        elif kind=='split':
            fr=board(s['board'],t,t-s.get('b0',s['t0']),pw=W//2)
            z,fx,fy=s['crop']; wes=grade(crop(clip.get(ct),z*(1+0.025*pr),fx,fy,box_w=W//2))
            q=ease((t-s.get('b0',s['t0']))/0.45) if s.get('slide') else 1.0
            full=Image.new('RGB',(W,H)); full.paste(fr,(0,0)); full.paste(wes,(W//2+int((1-q)*120),0))
            ImageDraw.Draw(full).line((W//2,0,W//2,H),fill=(30,30,40),width=2); fr=full
        else:
            z,fx,fy=s['crop']; z2=s.get('zend',z*1.03); zz=z+(z2-z)*ease(pr)
            fr=grade(crop(clip.get(ct),zz,fx,fy))
            if i==0: fr=lower_third(fr,lt)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

# ---- logo lock: HeyGen sometimes animates the stamped letters (e.g. a blue bar under STEADFAST). The background is static,
# so wherever Wes is not covering the logo box we put back the stamped plate pixels (letters lifted from LOCKED-stage-screen.jpg).
import cv2
def _box(cx,cy,wf,pad=0.02):
    lh=wf*W*220/575/H; return (cx-wf/2-pad,cx+wf/2+pad,cy-lh/2-pad,cy+lh/2+pad)
LOCK={'R1':('up/80-wes-work-room.jpg',_box(0.27,0.17,0.30)),'R2b':('up/80-wes-work-room.jpg',_box(0.27,0.17,0.30)),
      'R3':('up/72-wes-three-quarter-palms.jpg',_box(0.28,0.16,0.28)),'R5b':('up/72s.jpg',_box(0.535,0.10,0.13)),
      'R6':('up/73-wes-side-close.jpg',_box(0.72,0.17,0.20)),'R7b':('up/A09.jpg',(0.03,0.40,0.05,0.33))}
_LK={}
def lock(src,im,fidx):
    if src not in LOCK: return im
    if src not in _LK:
        p,(x0,x1,y0,y1)=LOCK[src]; pl=np.asarray(Image.open(p).convert('RGB').resize((W,H))).astype(np.float32)
        X0,X1,Y0,Y1=int(max(0,x0)*W),int(min(1,x1)*W),int(max(0,y0)*H),int(min(1,y1)*H)
        fm=np.zeros((H,W),np.float32); fm[Y0:Y1,X0:X1]=1; fm=cv2.GaussianBlur(fm,(0,0),12)
        masks=np.load(f'masks/{src}.npy') if os.path.exists(f'masks/{src}.npy') else None
        _LK[src]=(pl,fm,masks)
    pl,fm,masks=_LK[src]; a=np.asarray(im).astype(np.float32); w=fm.copy()
    if masks is not None:
        j=min(len(masks)-1,fidx//5); mm=np.maximum(masks[j],masks[min(len(masks)-1,j+1)])
        mm=cv2.resize(cv2.dilate(mm,np.ones((7,7))),(W,H)).astype(np.float32)/255
        w=w*(1-cv2.GaussianBlur(mm,(0,0),6))
    a=a*(1-w[...,None])+pl*w[...,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
_get=Clip.get
def _lget(s,t):
    k=min(s.n,max(1,int(t*s.fps)+1)); src=os.path.basename(s.d)[:-2]
    return lock(src,Image.open(f'{s.d}/%05d.png'%k).convert('RGB'),k-1)
Clip.get=_lget

if __name__=='__main__':
    for a in sys.argv[1:]: render(int(a)); print('done',a,flush=True)
