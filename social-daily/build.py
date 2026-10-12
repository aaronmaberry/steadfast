import json, subprocess, sys, math, datetime, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from daily_style import style_for
from daily_wes import wes_for, head_x
W,H,FPS=1080,1920,30; DUR=44.0
DATE=datetime.date.fromisoformat(os.environ.get('DAY','2026-10-12')); PAL,TREAT=style_for(DATE)
IMG=os.path.join(HERE,'..','img')+'/'; A=os.path.join(HERE,'assets')+'/'
WES=wes_for(DATE)
BG=(7,7,10); SURF=(18,18,24); TEXT=(244,244,245); DMUTE=(200,200,208); FAINT=(113,113,122); ACC=PAL['acc']
FL=A+'Geist-Light.ttf'; FR=A+'Geist-Regular.ttf'; FM=A+'Geist-Medium.ttf'
_fc={}
def F(n,s):
    if (n,s) not in _fc: _fc[(n,s)]=ImageFont.truetype(n,s)
    return _fc[(n,s)]
ease=lambda x: 1-(1-max(0.0,min(1.0,x)))**3
# ---------- tokens
w=json.load(open('words.json')); T=[]; i=0
while i<len(w):
    t,s,e=w[i]
    if t=='16,': T.append(['16:10',s,w[i+1][2]]); i+=2; continue
    if t==',000.': T[-1][0]='$10,000.'; T[-1][2]=e; i+=1; continue
    T.append([t,s,e]); i+=1
for t in T:
    if t[0]=='challenge,': t[0]='challenge:'
    if t[0]=='fix': t[0]='Fix'
    if t[0]=='Whoever': t[1]=4.55
idx=lambda word,after=0: next(k for k,t in enumerate(T) if t[0]==word and t[1]>=after)
P=[]
def phrase(a,b,style): P.append((a,b,style))
phrase(0,2,'hook'); phrase(3,5,'hook')
L=idx('Luke'); phrase(L,L+1,'ref')
WH=idx('Whoever'); MU=idx('much.')
LM=idx('The',9); phrase(LM,LM+2,'g'); phrase(LM+3,LM+5,'g')
SH=idx('Small'); phrase(SH,SH+5,'g')
FX=idx('Fix'); phrase(FX,FX+5,'cap')
TC=idx("Today's"); phrase(TC,TC+1,'eyebig'); phrase(TC+2,TC+5,'big')
NM=idx('Name'); phrase(NM,NM+7,'g')
TI=idx('The',23); phrase(TI,TI+1,'chip'); phrase(TI+2,TI+3,'chip'); phrase(TI+4,TI+10,'g2')
FI=idx('Fix',27); phrase(FI,FI+2,'big')
CO=idx('Correct'); phrase(CO,CO+4,'cap')
OR=idx('or',31); phrase(OR,OR+4,'g'); phrase(OR+5,OR+12,'cap')
TB=idx('Tell'); phrase(TB,TB+5,'g')
BE=idx('Be',36); phrase(BE,BE+5,'money1'); phrase(BE+6,BE+11,'money2')
SE=idx('Send'); phrase(SE,SE+7,'hcap')
# ---------- shots  (G:n = graphic with layout variant n; W:file = Wes wide card; HG:offset = HeyGen take)
# Hook/CTA: bank stills with a slow push (zero spend). Set HOOKDIR/CTADIR to frame dirs of optional HeyGen idle takes instead.
HOOKDIR=os.environ.get('HOOKDIR','still:hook'); CTADIR=os.environ.get('CTADIR','still:cta'); CTA_OFF=float(os.environ.get('CTA_OFF','40.5'))
SHOTS=[(0,2.62,'HG:'+HOOKDIR),(2.62,4.5,'G:0'),(4.5,6.62,'CARD:1'),(6.62,9.15,'CARD:2'),
(9.15,10.6,'G:1'),(10.6,12.1,'G:2'),(12.1,15.25,'G:3'),(15.25,17.75,'W:0'),
(17.75,19.3,'G:4'),(19.3,21.0,'G:0'),(21.0,23.9,'G:1'),(23.9,27.2,'G:2'),(27.2,29.15,'G:3'),
(29.15,31.1,'W:1'),(31.1,32.6,'G:4'),(32.6,34.5,'W:2'),(34.5,36.4,'G:0'),
(36.4,38.5,'G:1'),(38.5,40.5,'G:2'),(40.5,42.4,'HG:'+CTADIR),(42.4,DUR,'END')]
HG_START={HOOKDIR:0.0,CTADIR:CTA_OFF}
# ---------- daily background
YY,XX=np.mgrid[0:H,0:W].astype(np.float32)
def glow(cx,cy,r,col,a):
    d=np.sqrt((XX-cx)**2+(YY-cy)**2)/r; m=np.clip(1-d/0.7,0,1)**1.6*a
    return m[...,None]*np.array(col,np.float32)
grid=np.zeros((H,W),np.float32); grid[:, ::96]=1; grid[::96,:]=1
VIG=np.clip(1-((XX-W/2)/(W*0.75))**2-((YY-H*0.45)/(H*0.7))**2,0,1)[...,None]**0.8
rng=np.random.default_rng(7)
cloud=np.asarray(Image.fromarray((rng.random((60,34))*255).astype(np.uint8)).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(60))).astype(np.float32)[...,None]/255
GRAIN=[np.asarray(Image.fromarray(np.clip(np.random.default_rng(s).normal(128,6,(H//2,W//2)),0,255).astype(np.uint8)).resize((W,H))).astype(np.float32)[...,None]-128 for s in range(6)]
VARS=[(0.78,0.22),(0.25,0.30),(0.5,0.15),(0.7,0.7),(0.3,0.75)]  # glow anchors per layout variant
def bg_frame(t,var):
    A,B=np.array(PAL['a'],np.float32),np.array(PAL['b'],np.float32)
    ax,ay=VARS[var%5]; ox=40*math.sin(t*0.45); oy=60*math.cos(t*0.35)
    img=np.zeros((H,W,3),np.float32)+np.array(BG,np.float32)
    if TREAT.startswith('mesh'):
        img+=glow(W*ax+ox,H*ay+oy,900,A,0.38)+glow(W*(1-ax)-ox,H*(ay+0.12)-oy,780,B,0.28)
        gm=np.clip(1-np.sqrt(((XX-W*ax)/(W*0.75))**2+((YY-H*ay)/(H*0.55))**2)/0.72,0,1); img+=(grid*gm*0.045*255)[...,None]
    elif TREAT.startswith('spotlight'):
        img+=glow(W*ax+ox*0.6,H*ay*0.8+oy*0.4,1350,A,0.62)+glow(W*(1-ax),H*0.95,1000,B,0.45)
        img*=0.45+0.55*VIG; img+=GRAIN[int(t*12)%6]*0.8
    elif TREAT.startswith('diagonal'):
        d=((XX*0.6+YY*0.4)/(W*0.6+H*0.4)+0.08*math.sin(t*0.3)+var*0.11)%1.0
        band=np.exp(-((d-0.5)/0.16)**2)[...,None]; img+=band*A*0.30+(1-band)*B*0.10
    elif TREAT.startswith('horizon'):
        hy=H*(0.62+0.05*(var%3-1)); band=np.exp(-((YY-hy)/(H*0.18))**2)[...,None]
        img+=band*A*0.34+np.clip((YY-hy)/H,0,1)[...,None]*B*0.5
    else:
        img+=cloud*A*0.35+(1-cloud)*B*0.12+glow(W*ax+ox,H*ay+oy,900,A,0.2)
    return img
BCACHE={}
def bg(t,var):
    k=(round(t*6)/6,var)
    if k not in BCACHE:
        if len(BCACHE)>6: BCACHE.clear()
        BCACHE[k]=bg_frame(k[0],var)
    return BCACHE[k]
# ---------- Wes plates (ghost-cleaned)
WC={}
def bank_crop(path,aspect):
    im=Image.open(path).convert('RGB'); h=im.height; w=min(im.width,int(round(h*aspect)))
    cx=head_x(path)*im.width; x0=int(max(0,min(im.width-w,cx-w/2)))
    return im.crop((x0,0,x0+w,h))
def wide_card(src):
    if src in WC: return WC[src]
    c=bank_crop(WES['room'][int(src)],1080/828)
    c=ImageEnhance.Color(c).enhance(0.92)
    big=c.resize((int(1080*1.08),int(828*1.08)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,40,2))
    WC[src]=big; return big
CARD_Y=470; CARD_H=828
mask_card=Image.new('L',(1080,CARD_H),0); ImageDraw.Draw(mask_card).rounded_rectangle((0,0,1079,CARD_H-1),28,fill=255)
STILL={}
def hg_frame(dr,t):
    if dr.startswith('still:'):
        if dr not in STILL: STILL[dr]=bank_crop(WES[dr[6:]],W/H).resize((W,H),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,30,2))
        return STILL[dr]
    n=int(t*FPS)+1; f=f'{dr}/%04d.png'%n
    if not os.path.exists(f): f=dr+'/'+sorted(os.listdir(dr))[-1]
    return Image.open(f).convert('RGB')
logo=Image.open(IMG+'logo-lockup.jpg').convert('RGB'); logo=logo.resize((640,int(640*logo.height/logo.width)),Image.LANCZOS)
logo_mask=logo.convert('L').point(lambda v:min(255,max(0,(v-22)*3)))
g=np.zeros((H,1),np.float32)
for y in range(H):
    f=y/H; g[y]=0.12 if f<0.5 else 0.12+0.7*((f-0.5)/0.5)
GRAD=np.repeat(g,W,1)[...,None]
# ---------- text
def tw(text,font,track): return font.getlength(text)+track*max(0,len(text)-1)
def dtext(d,xy,text,font,fill,track=0,anchor='l'):
    x,y=xy
    if anchor=='m': x-=tw(text,font,track)/2
    if track==0: d.text((x,y),text,font=font,fill=fill); return
    for i,ch in enumerate(text): d.text((x+font.getlength(text[:i])+track*i,y),ch,font=font,fill=fill)
def layout(words,font,track,maxw,space):
    lines=[[]]; cur=0
    for wd in words:
        ww=tw(wd,font,track)
        if lines[-1] and cur+space+ww>maxw: lines.append([]); cur=0
        cur+=(space if lines[-1] else 0)+ww; lines[-1].append((wd,ww))
    return lines
STY={'hook':(FL,150,-0.045,1.0,TEXT),'big':(FL,140,-0.045,1.0,TEXT),'cap':(FM,74,-0.01,1.18,TEXT),'hcap':(FM,74,-0.01,1.18,TEXT),
 'chip':(FM,80,-0.01,1.18,TEXT),'g':(FL,104,-0.04,1.08,TEXT),'g2':(FL,92,-0.04,1.08,TEXT),'ref':(FL,170,-0.045,1.0,TEXT),
 'eyebig':(FM,60,0.08,1,ACC),'money1':(FL,104,-0.045,1.08,TEXT),'money2':(FL,104,-0.045,1.08,TEXT)}
CXC=500
def active_phrases(t):
    out=[]
    for n,(a,b,st) in enumerate(P):
        start=T[a][1]-0.12; end=T[P[n+1][0]][1]-0.12 if n+1<len(P) else DUR
        if st=='eyebig': end=T[P[n+1][1]][2]+1.6
        if st=='chip': end=min(T[TI+10][2]+0.25,27.2)
        if st=='g2': end=27.2
        if st=='money1': end=38.5
        if n==len(P)-1: end=42.4
        if st=='hook' and n==0: end=T[3][1]-0.12; start=-1
        if start<=t<end: out.append((n,a,b,st,start,end))
    return out
def draw_phrase(d,t,n,a,b,st,start,end,mode):
    name,size,trk,lh,col=STY[st]; font=F(name,size); track=trk*size
    words=[T[k][0] for k in range(a,b+1)]
    if st in('hook','eyebig'): words=[x.upper() for x in words]
    space=font.getlength(' ')+track*0.5
    lines=layout(words,font,track,800 if st not in('cap','hcap') else 820,space); lhpx=int(size*lh*1.12)
    if st in('cap','hcap'):
        y0=(1320 if mode=='W' else 1390-len(lines)*lhpx)
    elif st=='chip': y0=760+[p for p in range(len(P)) if P[p][2]=='chip'].index(n)*130
    elif st=='g2': y0=1060
    elif st in('g',): y0=960-len(lines)*lhpx//2
    else: y0={'hook':1250 if mode=='H' else 1000,'big':800,'ref':780,'eyebig':640,'money1':560,'money2':980}[st]
    k=a
    for li,ln in enumerate(lines):
        lw=sum(x[1] for x in ln)+space*(len(ln)-1); x=CXC-lw/2; y=y0+li*lhpx
        if st=='chip':
            qc=ease((t-(T[k][1]-0.12))/0.16)
            if qc>0: d.rounded_rectangle((x-30,y-16,x+lw+30,y+size*1.1),20,fill=SURF+(int(210*qc),),outline=ACC+(int(90*qc),),width=2)
        for wd,ww in ln:
            ts=T[k][1]; q=1.0 if (st=='hook' and n==0 and k==0) else ease((t-(ts-0.12))/0.16)
            if st=='eyebig': q=ease((t-start)/0.25)
            if q>0:
                live=ts<=t<=T[k][2]+0.1
                c=ACC if (live and st!='ref') else col
                if st=='money1' and t>=T[P[n+1][0]][1]-0.12: c=FAINT
                if st=='hook' and wd=='TEST.': c=ACC
                al=int(255*q); dy=int((26 if st in('cap','hcap','chip') else 40)*(1-q))
                if st in('cap','hcap') and mode!='W':
                    pass
                dtext(d,(x,y+dy),wd,font,c+(al,),track)
            x+=ww+space; k+=1
def card(d,t):
    q=ease((t-4.5)/0.35); yo=int(50*(1-q)); x0,x1,y0,y1=90,910,600,1300
    d.rounded_rectangle((x0,y0+yo,x1,y1+yo),30,fill=(18,18,24,int(215*q)),outline=(255,255,255,int(40*q)),width=2)
    dtext(d,(x0+64,y0+64+yo),'VERSE OF THE DAY',F(FM,30),ACC+(int(255*q),),0.08*30)
    vf=F(FR,66); words=T[WH:MU+1]; sp=vf.getlength(' ')
    lines=layout([x[0] for x in words],vf,-0.6,820-128,sp); y=y0+150+yo; k=0
    for ln in lines:
        x=x0+64
        for wd,ww in ln:
            dtext(d,(x,y),wd,vf,(TEXT if t>=words[k][1]-0.06 else (82,82,92))+(int(255*q),),-0.6); x+=ww+sp; k+=1
        y+=int(66*1.42)
    d.line((x0+64,y1-150+yo,x0+164,y1-150+yo),fill=ACC+(int(200*q),),width=2)
    dtext(d,(x0+64,y1-120+yo),'Luke 16:10',F(FM,40),DMUTE+(int(255*q),))
    dtext(d,(x0+64,y1-70+yo),'walksteadfast.com',F(FR,28),FAINT+(int(255*q),))
RNG=np.random.default_rng(11); PTS=[(RNG.uniform(60,1020),RNG.uniform(0,1920),RNG.uniform(1.2,3.6),RNG.uniform(12,40),RNG.uniform(0,6.28)) for _ in range(70)]
SECT=[(0,9.15,'01','VERSE','16:10'),(9.15,17.75,'02','SILENT TOUCH','LITTLE'),(17.75,36.4,'03','CHALLENGE','FIX IT'),(36.4,42.4,'04','THE STANDARD','$10,000')]
def rich(d,lay,t,a,b,src):
    sec=next((x for x in SECT if x[0]<=t<x[1]),None)
    if not sec: return
    q=ease((t-a)/0.4)
    # oversized outlined watermark word, slow drift
    wm=sec[4]; f=F(FL,250); w=tw(wm,f,-8); x=CXC-w/2+60*math.sin(t*0.25)-40*((t-a)/(b-a)); y=1100
    for i,ch in enumerate(wm): d.text((x+f.getlength(wm[:i])-8*i,y),ch,font=f,fill=(0,0,0,0),stroke_width=2,stroke_fill=PAL['acc']+(int(60*q),))
    # drifting light motes
    for (px,py,r,sp,ph) in PTS:
        yy=(py-t*sp)%1920; al=int((40+30*math.sin(t*1.3+ph))*q)
        if 220<yy<1500: d.ellipse((px-r,yy-r,px+r,yy+r),fill=(255,255,255,al))
    # top-left corner bracket and top-right tick (kept left of right rail)
    c=PAL['acc']+(int(110*q),); d.line((60,240,60,290),fill=c,width=2); d.line((60,240,110,240),fill=c,width=2)
    d.line((870,240,920,240),fill=c,width=2); d.line((920,240,920,290),fill=c,width=2)
    vs='“Whoever can be trusted with very little can also be trusted with much.”'
    dtext(d,(90,1372),vs,F(FL,25),DMUTE+(int(150*q),))
    # section index top right
    dtext(d,(800,300),sec[2]+' / 04',F(FM,30),DMUTE+(int(200*q),),2.4)
    # footer meta row (above bottom 20%)
    fy=1440; d.line((90,fy-22,830,fy-22),fill=(255,255,255,int(28*q)),width=1)
    dtext(d,(90,fy),'LUKE 16:10',F(FM,28),ACC+(int(230*q),),2.2)
    dtext(d,(300,fy),'·  '+sec[3],F(FM,28),FAINT+(int(230*q),),2.2)
    for i in range(4):
        x0=640+i*50; on=(i==int(sec[2])-1)
        d.rounded_rectangle((x0,fy+8,x0+36,fy+14),3,fill=(ACC if on else (90,90,100))+(int(230*q),))
    # progress bar within section
    pr=(t-sec[0])/(sec[1]-sec[0]); d.line((90,fy-22,90+int(740*pr),fy-22),fill=ACC+(int(160*q),),width=2)
def shot_at(t):
    for s in SHOTS:
        if s[0]<=t<s[1]: return s
    return SHOTS[-1]
def frame(n):
    t=n/FPS; a,b,src=shot_at(t); p=(t-a)/(b-a); si=SHOTS.index((a,b,src)); mode='G'
    var=int(src.split(':')[1]) if src.startswith(('G:','CARD:')) else si%5
    arr=bg(t,var).copy()
    if src.startswith('HG:'):
        mode='H'; fr=hg_frame(src[3:],t-HG_START[src[3:]]).resize((W,H),Image.LANCZOS)
        z=1.0+0.03*p; cw,ch=W/z,H/z; fr=fr.resize((W,H),Image.BICUBIC,box=((W-cw)/2,(H-ch)*0.35,(W+cw)/2,(H-ch)*0.35+ch))
        arr=np.asarray(fr).astype(np.float32); arr=arr*(1-GRAD)+np.array(BG,np.float32)*GRAD; arr+=GRAIN[n%6]*0.6
    base=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert('RGBA')
    if src.startswith('W:'):
        mode='W'; big=wide_card(src[2:]); z=1.0+0.06*ease(p)
        cw,ch=big.width/1.08/z*1.0,big.height/1.08/z
        dx=(big.width-cw)/2+(si%3-1)*20*(p-0.5); dy=(big.height-ch)*0.45
        c=big.resize((1080,CARD_H),Image.BICUBIC,box=(dx,dy,dx+cw,dy+ch))
        ca=np.asarray(c).astype(np.float32)+GRAIN[n%6][:CARD_H]; c=Image.fromarray(np.clip(ca,0,255).astype(np.uint8))
        q=ease((t-a)/0.25); m=mask_card.point(lambda v:int(v*q))
        base.paste(c,(0,CARD_Y+int(30*(1-q))),m)
    if t-a<2/FPS and si>0: base=Image.eval(base,lambda v:int(v*0.82))
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    if src.startswith('W:'): d.rounded_rectangle((0,CARD_Y,1079,CARD_Y+CARD_H-1),28,outline=(255,255,255,26),width=2)
    eb=None
    if 0<=t<2.62 and not src.startswith('HG'): eb='STEADFAST  ·  DAILY'
    elif 9.15<=t<17.75: eb='SILENT TOUCH'
    elif 23.9<=t<36.4 and not src.startswith('G:0') and not (27.2<=t<29.15): eb="TODAY'S CHALLENGE"
    if eb: dtext(d,(90,300),eb,F(FM,34),ACC+(235,),0.08*34); d.line((90,352,150,352),fill=ACC+(200,),width=2)
    if 9.15<=t<17.75 and mode!='W': dtext(d,(90,380),'The little money, the little minute',F(FL,46),TEXT+(220,),-0.02*46)
    if eb=="TODAY'S CHALLENGE" and mode!='W': dtext(d,(90,380),'Fix the small fudge',F(FL,46),TEXT+(220,),-0.02*46)
    if mode=='G' and src!='END': rich(d,lay,t,a,b,src)
    if src.startswith('CARD:'): card(d,t)
    if 2.62<=t<4.5:
        q=ease((t-2.62)/0.3); dtext(d,(CXC,690),'TODAY’S VERSE',F(FM,34),ACC+(int(255*q),),0.08*34,'m')
    for ph in active_phrases(t):
        if src.startswith('CARD:') and ph[3]!='ref': continue
        if ph[3]=='ref' and t>=4.5: continue
        draw_phrase(d,t,*ph,mode)
    if src=='END':
        lt=t-42.4; q=ease(lt/0.45); s=0.92+0.08*q
        lg=logo.resize((int(logo.width*s),int(logo.height*s)),Image.LANCZOS); m=logo_mask.resize(lg.size).point(lambda v:int(v*q))
        lay.paste(lg,(int(CXC-lg.width/2),560+int(30*(1-q))),m)
        q2=ease((lt-0.25)/0.35); dtext(d,(CXC,900+int(24*(1-q2))),"Follow for tomorrow's challenge",F(FM,52),TEXT+(int(255*q2),),-0.52,'m')
        q3=ease((lt-0.45)/0.35); dtext(d,(CXC,990),'walksteadfast.com/daily',F(FR,38),DMUTE+(int(255*q3),),0,'m')
        d.line((CXC-int(160*q3),1070,CXC+int(160*q3),1070),fill=ACC+(200,),width=2)
    base.alpha_composite(lay); out=base.convert('RGB')
    if t>=DUR-0.33 and FIRST is not None: out=Image.blend(out,FIRST,ease((t-(DUR-0.33))/0.33))
    return out
FIRST=None; FIRST=frame(0)
if __name__=='__main__':
    if len(sys.argv)>1:
        for s in sys.argv[1:]: frame(int(float(s)*FPS)).save(f'qa_{s}.jpg',quality=88)
    else:
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','video.mp4'],stdin=subprocess.PIPE)
        for n in range(int(DUR*FPS)): p.stdin.write(frame(n).tobytes())
        p.stdin.close(); p.wait()
