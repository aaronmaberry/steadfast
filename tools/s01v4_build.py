import cv2
import json,math,os,sys,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H,FPS=1920,1080,30
A='/workspace/steadfast/social-daily/assets/'
FL,FR,FM=A+'Geist-Light.ttf',A+'Geist-Regular.ttf',A+'Geist-Medium.ttf'; FMONO=A+'GeistMono-Medium.ttf'
BG=(7,7,10); TEXT=(244,244,245); DM=(200,200,208); FAINT=(113,113,122)
PA=(91,110,245); PB=(80,40,160); ACC=(139,156,255)
_f={}
def F(n,s):
    if (n,s) not in _f: _f[(n,s)]=ImageFont.truetype(n,s)
    return _f[(n,s)]
ease=lambda x:1-(1-max(0.,min(1.,x)))**3
WORDS=json.load(open('words.json')); PLAN=json.load(open(os.environ.get('PLANF','plan.json')))
rng=np.random.default_rng(3)
GRAIN=[rng.normal(0,2.2,(H,W,1)).astype(np.float32) for _ in range(6)]
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.38*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)/2)[...,None].astype(np.float32)
CARDS={
 'belong':dict(eb='SESSION 1  ·  WELCOME',wm='BELONG',text="Every man in this room belongs in the chair he's in.",hl={'belongs'},w0=52.1,size=64),
 'laugh':dict(eb='SESSION 1  ·  THE ROOM',wm='LAUGH',text="A man who can laugh in a room like this can usually tell the truth in one.",hl={'laugh','truth'},w0=123.9,size=58),
 'boots':dict(eb='SESSION 1  ·  WELCOME',wm='WORK',text="A few of you came straight from work, boots still on.",hl={'boots'},w0=38.7,size=72),
 'ontime':dict(eb='SESSION 1  ·  ON TIME',wm='ON TIME',text="Divorced, still a dad, the house got real quiet. Or you figured, you know, this was for a younger guy. You're on time.",hl={'quiet.','on','time.'},w0=66.7,size=54),
 'chairs':dict(eb='SESSION 1  ·  WELCOME BACK',wm='BACK',text="Same folding chairs, same kind of quiet right before somebody starts talking. You could probably run this thing yourself, right? Glad you're back.",hl={'quiet','back.'},w0=9.5,size=52),
 'plain':dict(eb='SESSION 1  ·  PLAIN',wm='PLAIN',text="So here's the thing I wish somebody had told me, plain, a long time ago.",hl={'plain,'},w0=130.1,size=64),
 'tuesday':dict(eb='SESSION 1  ·  THE DAY',wm='THE DAY',text="Okay, I call that day a Tuesday. If you vanish on a Thursday, call it Thursday. The name isn't magic, the day is.",hl={'Tuesday.','day','is.'},w0=164.1,size=56),
 'guest':dict(eb='SESSION 1  ·  WELCOME',wm='GUEST',text="Nobody in here is a guest.",hl={'guest.'},w0=75.5,size=88),
 'checking':dict(eb='SESSION 1  ·  THE ROOM',wm='NAME TAG',text="A whole room full of guys just checking it out with a name tag on.",hl={'checking'},w0=111.2,size=64),
 'key1':dict(eb='SESSION 1  ·  A QUIET TUESDAY',wm='TUESDAY',text="A man's life gets decided on the days nobody photographs.",hl={'decided','nobody','photographs.'},w0=135.4,size=72),
 'verse':dict(eb='LUKE 16:10  ·  NIV',wm='FAITHFUL',text="“Whoever can be trusted with very little can also be trusted with much, and whoever is dishonest with very little will also be dishonest with much.”",hl={'very','little'},w0=147.7,size=46,ref='Luke 16:10',reft=157.4),
 'key2':dict(eb='KEY POINT',wm='ORDINARY',text="A man is trusted on an ordinary day.",hl={'ordinary','day.'},w0=160.7,size=80),
}
def wtimes(c):
    toks=c['text'].split(); ws=[w for w in WORDS if w[1]>=c['w0']-0.3]; out=[]
    for j,tk in enumerate(toks): out.append(ws[j][1] if j<len(ws) else out[-1]+0.25)
    return out
for c in CARDS.values(): c['wt']=wtimes(c)
def wrap(words,font,maxw):
    lines=[[]]
    for w in words:
        if font.getlength(' '.join(lines[-1]+[w]))>maxw and lines[-1]: lines.append([w])
        else: lines[-1].append(w)
    return lines
BGC={}
def card_bg(t,var):
    k=(int(t*6),var)
    if k in BGC: return BGC[k]
    a=np.zeros((270,480,3),np.float32)+np.array(BG,np.float32); Y,X=np.mgrid[0:270,0:480]
    for (cx,cy,r,col,ph) in [(0.25,0.3,0.55,PA,0),(0.8,0.75,0.5,PB,2),(0.6,0.15,0.35,PA,4)]:
        cx2=cx+0.06*math.sin(t*0.15+ph+var); cy2=cy+0.05*math.cos(t*0.12+ph)
        d=np.sqrt(((X/480-cx2)*1.78)**2+(Y/270-cy2)**2)/r
        a+=np.clip(1-d,0,1)[...,None]**2*np.array(col,np.float32)*0.30
    img=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).resize((W,H),Image.BICUBIC); dd=ImageDraw.Draw(img)
    for x in range(0,W,96): dd.line((x,0,x,H),fill=(14,14,20))
    for y in range(0,H,96): dd.line((0,y,W,y),fill=(14,14,20))
    if len(BGC)>20: BGC.clear()
    BGC[k]=img; return img
def card_frame(key,t,a,b,pw=W,a0=None):
    """board in a pw-wide panel (pw=W full screen). a0 = board's first appearance (for split continuation)"""
    c=CARDS[key]; a0=a if a0 is None else a0; sc=pw/W if pw<W else 1.0
    img=card_bg(t,hash(key)%5).copy().convert('RGBA'); lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    q=ease((t-a0)/0.5); cx=pw/2; m=96 if pw==W else 72
    f=F(FL,int(330*(0.7 if pw<W else 1))); wm=c['wm']; x=cx-f.getlength(wm)/2+40*math.sin(t*0.2)-30*((t-a)/(b-a))
    d.text((x,H-(470 if pw==W else 400)),wm,font=f,fill=(0,0,0,0),stroke_width=2,stroke_fill=ACC+(int(34*q),))
    cc=ACC+(int(120*q),)
    for (x0,y0,sx,sy) in [(m,m,1,1),(pw-m,m,-1,1),(m,H-m,1,-1),(pw-m,H-m,-1,-1)]:
        d.line((x0,y0,x0+50*sx,y0),fill=cc,width=2); d.line((x0,y0,x0,y0+50*sy),fill=cc,width=2)
    fe=F(FM,26 if pw==W else 22); eb=c['eb']; tr=5 if pw==W else 4
    ew=sum(fe.getlength(ch)+tr for ch in eb)-tr; ex=cx-ew/2
    ft=F(FL,c['size']); words=c['text'].split(); lines=wrap(words,ft,(1400 if key=='verse' else 1300) if pw==W else pw-200)
    lh=int(c['size']*1.32); y=(H-len(lines)*lh)/2+10; ey=y-130
    for ch in eb: d.text((ex,ey),ch,font=fe,fill=ACC+(int(235*q),)); ex+=fe.getlength(ch)+tr
    lw=int(70*q); d.line((cx-lw,ey+44,cx+lw,ey+44),fill=ACC+(int(200*q),),width=2)
    hl={h.strip('“”,.') for h in c['hl']}; i=0
    for ln in lines:
        x=cx-ft.getlength(' '.join(ln))/2
        for w in ln:
            qq=ease((t-c['wt'][i]+0.08)/0.35); al=int(255*qq)
            if al>0: d.text((x,y+14*(1-qq)),w,font=ft,fill=(ACC if w.strip('“”,.') in hl else TEXT)+(al,))
            x+=ft.getlength(w+' '); i+=1
        y+=lh
    if 'ref' in c:
        q2=ease((t-c['reft'])/0.5); fs=F(FR,30); s='— '+c['ref']; d.text((cx-fs.getlength(s)/2,y+30),s,font=fs,fill=DM+(int(230*q2),))
    fm=F(FMONO,20 if pw==W else 17); s='STEADFAST MEN  ·  SESSION 1'; d.text((m,H-m-54),s,font=fm,fill=FAINT+(int(220*q),))
    d.line((m,H-m-68,pw-m,H-m-68),fill=(255,255,255,int(22*q)),width=1)
    d.line((m,H-m-68,m+int((pw-2*m)*(t-a)/(b-a)),H-m-68),fill=ACC+(int(150*q),),width=2)
    img.alpha_composite(lay); return img.convert('RGB')
LOGO=Image.open('/workspace/steadfast/img/logo-lockup.jpg').convert('RGB'); LOGO=LOGO.resize((760,int(760*LOGO.height/LOGO.width)),Image.LANCZOS)
LMASK=LOGO.convert('L').point(lambda v:min(255,max(0,(v-22)*3)))
def name_frame(t,a,b):
    img=card_bg(t,1).copy(); q=ease((t-91.5)/0.7)
    img.paste(LOGO,(W//2-LOGO.width//2,H//2-LOGO.height//2-40),LMASK.point(lambda v:int(v*q)))
    d=ImageDraw.Draw(img); fs=F(FMONO,22); s='SESSION 1  ·  WEEK ONE'; q2=ease((t-93.0)/0.6)
    d.text((W/2-fs.getlength(s)/2,H//2+LOGO.height//2+10),s,font=fs,fill=tuple(int(c*q2) for c in ACC))
    return img
# ---- clip frames
class Clip:
    def __init__(s,path,fps):
        s.dir=path; import subprocess as sp; r=sp.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=r_frame_rate','-of','csv=p=0',path[:-2]+'.mp4'],capture_output=True,text=True).stdout.strip().split('/'); s.fps=int(r[0])/int(r[1]); s.n=len(os.listdir(path))
    def get(s,t):
        n=min(s.n,max(1,int(t*s.fps)+1)); return Image.open(f'{s.dir}/%05d.png'%n).convert('RGB')
PICK=json.load(open('pick.json')) if os.path.exists('pick.json') else {}
CROP=json.load(open('crop.json')) if os.path.exists('crop.json') else {}
def grade(im,n):
    arr=np.asarray(im).astype(np.float32); w=arr.shape[1]; arr=np.clip((arr-13)*1.07,0,None)*VIG[:,W-w:]+GRAIN[n%6][:,:w]
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
SPEED={}
LOGOFIX=json.load(open('logofix.json')) if os.path.exists('logofix.json') else {}
_LF={}
def logofix(key,im):
    if key not in LOGOFIX: return im
    mode,plate=LOGOFIX[key]; a=np.asarray(im).astype(np.float32)
    if key not in _LF:
        m=cv2.imread(f'mask/{plate}.png',0)
        if m.shape!=a.shape[:2]: m=cv2.resize(m,(a.shape[1],a.shape[0]))
        md=cv2.GaussianBlur(cv2.dilate(m,np.ones((9,9))),(0,0),2.5).astype(np.float32)/255
        bg=cv2.inpaint(np.asarray(im)[:,:,::-1].copy(),(cv2.dilate(m,np.ones((11,11)))>20).astype(np.uint8),9,cv2.INPAINT_TELEA)[:,:,::-1].astype(np.float32)
        _LF[key]=(md,bg)
    md,bg=_LF[key]
    if mode=='erase': a=a*(1-md[...,None])+bg*md[...,None]
    else:
        soft=cv2.GaussianBlur(a,(0,0),0.9); k=float(mode)
        a=a*(1-md[...,None])+(bg+(soft-bg)*k)*md[...,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def clip_frame(clip,key,t,p,box_w=W):
    im=logofix(key,clip.get(t*SPEED.get(key,1.0)))
    if im.size!=(W,H): im=im.resize((W,H),Image.LANCZOS)
    z0,fx,fy=CROP.get(key,[1.0,0.5,0.5])
    z=z0*(1.0+0.03*ease(p)); ch=H/z; cw=ch*box_w/H
    x0=min(max(0,fx*W-cw/2),W-cw); y0=min(max(0,fy*H-ch/2),H-ch)
    return im.resize((box_w,H),Image.BICUBIC,box=(x0,y0,x0+cw,y0+ch))
def lower_third(img,t):
    a,b=2.0,6.0
    if not a<=t<b: return img
    q=min(ease((t-a)/0.5),ease((b-t)/0.5)); im=img.convert('RGBA'); lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    x=110+int(-30*(1-q)); y=H-250
    d.rectangle((x-30,y-20,x+460,y+92),fill=(7,7,10,int(140*q))); d.rectangle((x-30,y-20,x-26,y+92),fill=ACC+(int(255*q),))
    d.text((x,y-6),'Wes Hart',font=F(FM,44),fill=TEXT+(int(255*q),)); d.text((x,y+52),'STEADFAST MEN',font=F(FMONO,20),fill=DM+(int(220*q),))
    im.alpha_composite(lay); return im.convert('RGB')
def render(i):
    a,b,kind,plate=PLAN[i]; nf=round(b*FPS)-round(a*FPS); n0=round(a*FPS)
    clip=None
    if kind in('HG','IV') or kind.startswith('SPLIT'):
        clip=Clip('clips/'+PICK.get(str(i),f's{i:02d}')+'_f',24 if 'walk' in PICK.get(str(i),'') else 25)
    out=f'shots/s{i:02d}.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for k in range(nf):
        n=n0+k; t=n/FPS; lt=k/FPS; pr=k/max(1,nf-1)
        if kind.startswith('CARD:'):
            key=kind[5:]; fr=name_frame(t,a,b) if key=='name' else card_frame(key,t,(142.0 if key=='verse' else a),(159.4 if key=='verse' else b),a0=(142.0 if key=='verse' else None))
        elif kind.startswith('SPLIT:'):
            key=kind[6:]; a0=142.0 if key=='verse' else a
            fr=card_frame(key,t,a,b,pw=W//2,a0=a0)
            wes=grade(clip_frame(clip,f's{i:02d}',lt,pr,box_w=W//2),n)
            q=ease(lt/0.4) if a0==a else 1.0
            fr.paste(wes,(W//2+int((1-q)*120),0)); d=ImageDraw.Draw(fr); d.line((W//2,0,W//2,H),fill=(30,30,40),width=2)
        else:
            fr=grade(clip_frame(clip,f's{i:02d}',lt,pr),n)
            if i==0: fr=lower_third(fr,t)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
if __name__=='__main__':
    for s in sys.argv[1:]: render(int(s)); print('done',s,flush=True)
