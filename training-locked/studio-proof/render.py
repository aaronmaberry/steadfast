# Studio-format proof, Lesson 1 opening (0-63.0s of poc4-voice.mp3, Wes Hart - Podcast LxMQ, eleven_v3)
import numpy as np, subprocess, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1280,720,24
DUR=63.0
P='/workspace/artifacts/training/w01-poc/poc4/lipsync-test/'
B='broll/'
F='/workspace/steadfast-main/fonts/ttf/'
def font(n,s): return ImageFont.truetype(F+n,s)
def load(path,ss=0,t=None,fps=FPS,size=None):
    vf=f'fps={fps}'
    cmd=['ffmpeg','-v','error','-ss',str(ss)]+(['-t',str(t)] if t else [])+['-i',path,'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-']
    info=subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height','-of','csv=p=0',path]).decode().split()[0].split(',')
    w,h=int(info[0]),int(info[1])
    raw=subprocess.check_output(cmd)
    return np.frombuffer(raw,np.uint8).reshape(-1,h,w,3)
def cover(fr,w,h):
    im=Image.fromarray(fr);s=max(w/im.width,h/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-w)//2;t=(im.height-h)//2
    return np.asarray(im.crop((l,t,l+w,t+h)))
# ---- backdrop (walksteadfast.com palette: bg #07070a/#0c0c10, accent-2 #5b6ef5, accent #8b9cff glow)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
base=np.array([12,12,16],np.float32)
g1=np.exp(-(((xx-W*0.78)/520)**2+((yy-H*0.15)/380)**2))[...,None]*np.array([91,110,245])*0.30
g2=np.exp(-(((xx-W*0.12)/480)**2+((yy-H*0.95)/300)**2))[...,None]*np.array([120,80,200])*0.16
BG=np.clip(base+g1+g2,0,255).astype(np.uint8)
ACC=(139,156,255);ACC2=(91,110,245);TXT=(244,244,245);MUT=(161,161,170)
def wordmark(d):
    d.text((56,44),'STEADFAST MEN',font=font('GeistMono-Medium.ttf',18),fill=ACC)
    d.text((56,70),'LESSON 01 · A QUIET TUESDAY',font=font('GeistMono-Regular.ttf',14),fill=MUT)
def board(lines,sub=None):
    im=Image.fromarray(BG.copy());d=ImageDraw.Draw(im);wordmark(d)
    f=font('Geist-SemiBold.ttf',58);y=H//2-len(lines)*38-10
    d.rectangle((W//2-40,y-36,W//2+40,y-32),fill=ACC2)
    for ln in lines:
        tw=d.textlength(ln,font=f);d.text(((W-tw)/2,y),ln,font=f,fill=TXT);y+=76
    if sub:
        f2=font('GeistMono-Regular.ttf',18);tw=d.textlength(sub,font=f2);d.text(((W-tw)/2,y+18),sub,font=f2,fill=ACC)
    return np.asarray(im)
BOARD1=board(['Every man in this room','belongs in the chair he\u2019s in.'])
BOARD2=board(['Nobody in here','is a guest.'])
# ---- Wes sources
X1=load(P+'t03ls/x1/x1-raw.mp4')            # 241 fr @24
S3=load(P+'t03ls/x1/x1-sync3-restored-1.33s.mp4')  # 32 fr
OM=load(P+'om3/om3-v13-harm-5.2s.mp4')      # 25fps -> resampled to 24
STILL=np.asarray(Image.open(P+'om3/src13-blend.png').convert('RGB').resize((1280,720)))
def pending_still(tag):
    im=Image.fromarray(STILL).convert('L').convert('RGB')
    im=Image.blend(im,Image.new('RGB',im.size,(12,12,16)),0.45)
    d=ImageDraw.Draw(im);f=font('GeistMono-Medium.ttf',30)
    t='PAID TAKE PENDING · '+tag;tw=d.textlength(t,font=f)
    d.rectangle(((W-tw)/2-16,430,(W+tw)/2+16,480),fill=(91,110,245))
    d.text(((W-tw)/2,436),t,font=f,fill=(255,255,255))
    return np.asarray(im)
# ---- B-roll (Pexels, no faces/no chairs)
def br(id,ss,t): return [cover(f,W,H) for f in load(B+f'px-{id}.mp4',ss,t)]
# ---- timeline: layout segments; Wes source per sub-span
# each wes span: (t0,t1,kind,arg) kind: x1(frame offset s), s3, om, pend(tag)
SEG=[
 dict(kind='pip',t0=0.0,t1=35.30,broll=[(9945020,0.5,0.0,6.2),(4957763,1.0,5.7,13.6),(8292929,0.0,13.1,19.9),(12374854,4.0,19.4,26.9),(9843017,2.0,26.4,31.4),(9512571,1.0,30.9,35.8)],
      wes=[(0.0,5.70,'x1',0.0),(5.70,25.48,'pend','W02'),(25.48,26.81,'s3',0),(26.81,33.50,'pend','W04'),(33.50,35.80,'x1',8.25-33.50+0)]),
 dict(kind='board',t0=35.30,t1=38.10,img=BOARD1),
 dict(kind='split',t0=38.10,t1=52.40,broll=[(5612232,3.0,37.8,42.6),(3676982,0.0,42.1,46.2),(3051693,2.0,45.7,52.9)],
      wes=[(37.8,42.0,'pend','W06'),(42.0,47.2,'om',0),(47.2,52.9,'pend','W08')]),
 dict(kind='board',t0=52.40,t1=54.55,img=BOARD2),
 dict(kind='full',t0=54.55,t1=DUR,wes=[(54.0,DUR,'pend','W09-FULL')]),
]
XF=0.5
CACHE={}
def brframe(spec,t):
    for (id,ss,a,b) in spec:
        pass
    cands=[(id,ss,a,b) for (id,ss,a,b) in spec if a<=t<b]
    out=None
    for (id,ss,a,b) in cands:
        k=(id,ss,a,b)
        if k not in CACHE: CACHE[k]=br(id,ss,b-a+0.1)
        fr=CACHE[k][min(int((t-a)*FPS),len(CACHE[k])-1)].astype(np.float32)
        if out is None: out=fr;oa=a
        else:
            w=np.clip((t-a)/XF,0,1);out=out*(1-w)+fr*w   # crossfade over overlap
    return out
PEND={}
def wesframe(spec,t):
    for (a,b,k,arg) in spec:
        if a<=t<b:
            if k=='x1':
                i=int(round((t+arg)*FPS)) if arg else int(round((t-a)*FPS))
                return X1[min(i,len(X1)-1)]
            if k=='s3': return S3[min(int((t-a)*FPS),len(S3)-1)]
            if k=='om':
                fr=OM[min(int((t-a)*FPS),len(OM)-1)];return cover(fr,1280,720) if fr.shape[1]!=1280 else fr
            if k=='pend':
                if arg not in PEND: PEND[arg]=pending_still(arg)
                return PEND[arg]
    return PEND.get('x') if False else STILL
yy2,xx2=np.mgrid[0:300,0:300]
def circmask(D):
    y,x=np.mgrid[0:D,0:D];r=np.sqrt((x-D/2+.5)**2+(y-D/2+.5)**2)
    return np.clip(D/2-r,0,1)[...,None]
def rrmask(w,h,r):
    m=Image.new('L',(w,h),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r,fill=255)
    return (np.asarray(m)/255.0)[...,None]
D=360;CM=circmask(D);CR=circmask(D+8)
def layout(seg,t):
    k=seg['kind']
    if k=='board': return seg['img'].astype(np.float32)
    if k=='pip':
        out=brframe(seg['broll'],t).copy()
        wf=wesframe(seg['wes'],t)
        # face-centred square crop (face ~ (625,300) in X1 framing); hands stay below crop
        cx,cy,S=630,290,540
        sq=np.asarray(Image.fromarray(wf[cy-S//2:cy+S//2,cx-S//2:cx+S//2]).resize((D,D),Image.LANCZOS)).astype(np.float32)
        X0,Y0=W-D-48,H-D-44
        ring=np.array(ACC,np.float32)
        reg=out[Y0-4:Y0+D+4,X0-4:X0+D+4];reg[:]=reg*(1-CR)+ring*CR
        reg=out[Y0:Y0+D,X0:X0+D];reg[:]=reg*(1-CM)+sq*CM
        return out
    if k=='split':
        out=BG.astype(np.float32).copy()
        im=Image.fromarray(out.astype(np.uint8));d=ImageDraw.Draw(im);wordmark(d);out=np.asarray(im).astype(np.float32)
        pw,ph=560,540;y0=130
        wf=wesframe(seg['wes'],t)
        cx,cy=640,300
        crop=wf[max(cy-260,0):max(cy-260,0)+ph*1, cx-280:cx+280] if wf.shape[0]>=ph else wf
        crop=np.asarray(Image.fromarray(np.ascontiguousarray(crop)).resize((pw,ph),Image.LANCZOS)).astype(np.float32)
        m=rrmask(pw,ph,18)
        reg=out[y0:y0+ph,64:64+pw];reg[:]=reg*(1-m)+crop*m
        b=cover(brframe(seg['broll'],t).astype(np.uint8),pw,ph).astype(np.float32)
        reg=out[y0:y0+ph,W-64-pw:W-64];reg[:]=reg*(1-m)+b*m
        return out
    if k=='full':
        return wesframe(seg['wes'],t).astype(np.float32)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
   '-i','voice63.wav','-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','studio-proof-L01-60s-v1.mp4'],stdin=subprocess.PIPE)
N=int(DUR*FPS)
for n in range(N):
    t=n/FPS
    cur=[s for s in SEG if s['t0']<=t<s['t1']][0]
    fr=layout(cur,t)
    i=SEG.index(cur)
    # crossfade into this segment from previous over XF centred on boundary
    if i>0 and t<cur['t0']+XF/2:
        w=0.5+(t-cur['t0'])/XF; prev=layout(SEG[i-1],t); fr=prev*(1-w)+fr*w
    elif i<len(SEG)-1 and t>=cur['t1']-XF/2:
        w=0.5-(cur['t1']-t)/XF; nxt=layout(SEG[i+1],t); fr=fr*(1-w)+nxt*w
    if t<0.4: fr=fr*(t/0.4)
    if t>DUR-0.5: fr=fr*((DUR-t)/0.5)
    enc.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
enc.stdin.close();enc.wait();print('done')
