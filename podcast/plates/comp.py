import os,sys
from PIL import Image,ImageDraw,ImageFilter,ImageFont,ImageChops,ImageOps
R='/workspace/steadfast/';K=2;W,H=1920*K,1080*K
GE='/usr/share/fonts/truetype/sand-box/google/Geist/Geist-VariableFont_wght.ttf'
def F(sz,w=500):
    f=ImageFont.truetype(GE,int(sz*K))
    try:f.set_variation_by_axes([w])
    except Exception:pass
    return f
ACC=(139,156,255);ACC2=(91,110,245);BG=(7,7,10);TXT=(244,244,245);MUT=(161,161,170)
src=Image.open(R+'img/LOCKED-podcast-table.jpg').convert('RGB')
def up(n,box):
    p=n+'4.png'
    if os.path.exists(p):return Image.open(p).convert('RGB')
    return src.crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.LANCZOS)
WES=(up('wes',(0,200,700,1080)),(0.43,0.29));CO=(up('co',(850,240,1408,1080)),(0.63,0.34))
LOGO=Image.open(R+'img/logo-lockup.jpg').convert('RGB')
def S(v):return int(v*K)
def cover(im,w,h,anchor,zoom=1.0,fy=0.36):
    iw,ih=im.size;s=max(w/iw,h/ih)*zoom;nw,nh=int(iw*s),int(ih*s);r=im.resize((nw,nh),Image.LANCZOS)
    x=int(anchor[0]*nw-w/2);y=int(anchor[1]*nh-fy*h);x=max(0,min(x,nw-w));y=max(0,min(y,nh-h));return r.crop((x,y,x+w,y+h))
def background(kind='foam'):
    if kind=='studio':
        b=cover(src,W,H,(0.5,0.4)).filter(ImageFilter.GaussianBlur(S(14)))
    else:
        fo=src.crop((560,0,1080,540));b=cover(fo,W,H,(0.5,0.5))
    b=ImageChops.multiply(b,Image.new('RGB',(W,H),(120,122,140)))
    g=Image.new('L',(W,H),0);d=ImageDraw.Draw(g);d.ellipse((W*0.2,-H*0.2,W*0.8,H*0.9),fill=70);g=g.filter(ImageFilter.GaussianBlur(S(220)))
    b=Image.composite(Image.new('RGB',(W,H),ACC2),b,g)
    v=Image.new('L',(W,H),0);ImageDraw.Draw(v).rectangle((0,0,W,H),fill=180);ImageDraw.Draw(v).ellipse((-W*0.1,-H*0.2,W*1.1,H*1.2),fill=0);v=v.filter(ImageFilter.GaussianBlur(S(200)))
    return Image.composite(Image.new('RGB',(W,H),BG),b,v)
def rmask(w,h,r):
    m=Image.new('L',(w*2,h*2),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w*2-1,h*2-1),r*2,fill=255);return m.resize((w,h),Image.LANCZOS)
def glow(c,box,r,col=ACC,a=150,bl=28,bw=2):
    x0,y0,x1,y1=box;g=Image.new('L',(W,H),0);ImageDraw.Draw(g).rounded_rectangle(box,r,outline=a,width=S(6));g=g.filter(ImageFilter.GaussianBlur(S(bl)))
    c.paste(Image.composite(Image.new('RGB',(W,H),col),c,g))
def panel(c,box,r=24,fill=(12,12,18),alpha=215,border=True,gl=True,blur=True):
    x0,y0,x1,y1=[int(v) for v in box];w,h=x1-x0,y1-y0
    if gl:glow(c,box,r,a=110)
    reg=c.crop((x0,y0,x1,y1))
    if blur:reg=reg.filter(ImageFilter.GaussianBlur(S(24)))
    reg=Image.blend(reg,Image.new('RGB',(w,h),fill),alpha/255)
    c.paste(reg,(x0,y0),rmask(w,h,r))
    if border:
        o=Image.new('RGBA',(W,H));ImageDraw.Draw(o).rounded_rectangle(box,r,outline=ACC+(150,),width=S(1.5));c.paste(o,(0,0),o)
def cam(c,box,who,r=28,label=None,zoom=1.0):
    x0,y0,x1,y1=[int(v) for v in box];w,h=x1-x0,y1-y0;im,a=who
    glow(c,box,r,a=170)
    c.paste(cover(im,w,h,a,zoom),(x0,y0),rmask(w,h,r))
    o=Image.new('RGBA',(W,H));d=ImageDraw.Draw(o);d.rounded_rectangle(box,r,outline=ACC+(230,),width=S(2.5))
    if label:
        f=F(15,600);tw=d.textlength(label,font=f);px,py=(x0+S(18),y1-S(18)-S(34)) if r<w//3 else ((x0+x1)/2-(tw+S(28))/2,y1+S(14))
        d.rounded_rectangle((px,py,px+tw+S(28),py+S(34)),S(17),fill=(7,7,10,200),outline=ACC+(180,),width=S(1))
        d.text((px+S(14),py+S(17)),label,font=f,fill=TXT,anchor='lm')
    c.paste(o,(0,0),o)
def spaced(d,xy,t,f,fill,sp=0.32,anchor='m'):
    sz=f.size;ws=[d.textlength(ch,font=f)+sz*sp for ch in t];tot=sum(ws)-sz*sp;x,y=xy
    if anchor=='m':x-=tot/2
    for ch,wd in zip(t,ws):d.text((x,y),ch,font=f,fill=fill,anchor='lm');x+=wd
    return tot
def logo(c,cx,cy,w):
    l=LOGO.resize((int(w),int(w*LOGO.height/LOGO.width)),Image.LANCZOS);x,y=int(cx-l.width/2),int(cy-l.height/2)
    c.paste(ImageChops.lighter(c.crop((x,y,x+l.width,y+l.height)),l),(x,y))
def icon(d,cx,cy,k,s):
    r=s/2;col=TXT;lw=max(2,int(s*0.08))
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=ACC+(160,),width=max(1,int(s*0.05)))
    q=s*0.26
    if k=='x':d.line((cx-q,cy-q,cx+q,cy+q),fill=col,width=lw);d.line((cx-q,cy+q,cx+q,cy-q),fill=col,width=int(lw*0.6))
    elif k=='yt':d.rounded_rectangle((cx-q*1.2,cy-q*0.85,cx+q*1.2,cy+q*0.85),q*0.4,fill=col);d.polygon([(cx-q*0.35,cy-q*0.45),(cx-q*0.35,cy+q*0.45),(cx+q*0.5,cy)],fill=BG)
    elif k=='ig':d.rounded_rectangle((cx-q,cy-q,cx+q,cy+q),q*0.45,outline=col,width=lw);d.ellipse((cx-q*0.45,cy-q*0.45,cx+q*0.45,cy+q*0.45),outline=col,width=lw);d.ellipse((cx+q*0.5,cy-q*0.75,cx+q*0.72,cy-q*0.53),fill=col)
    elif k=='fb':d.text((cx+q*0.1,cy+q*0.15),'f',font=ImageFont.truetype(GE,int(s*0.62)),fill=col,anchor='mm')
    elif k=='tt':d.ellipse((cx-q*0.9,cy+q*0.1,cx-q*0.05,cy+q*0.95),outline=col,width=lw);d.line((cx-q*0.1,cy+q*0.5,cx-q*0.1,cy-q*0.95),fill=col,width=lw);d.arc((cx-q*0.1,cy-q*1.6,cx+q*0.9,cy-q*0.3),90,180,fill=col,width=lw)
def subscribe(c,x,y,scale=1.0,anchor='lt'):
    o=Image.new('RGBA',(W,H));d=ImageDraw.Draw(o);f=F(16*scale,700);t='SUBSCRIBE';tw=d.textlength(t,font=f)
    w=tw+S(64*scale);h=S(44*scale)
    if anchor=='mt':x-=w/2
    if anchor=='rb':x-=w;y-=h
    d.rounded_rectangle((x,y,x+w,y+h),h/2,fill=(255,0,51,255))
    tx=x+S(22*scale);ty=y+h/2;q=S(7*scale);d.polygon([(tx,ty-q),(tx,ty+q),(tx+q*1.5,ty)],fill=TXT)
    d.text((tx+q*1.5+S(12*scale),ty),t,font=f,fill=TXT,anchor='lm');c.paste(o,(0,0),o)
QUOTE='A son should be able to copy your walk.';TAG='#WalkSteadfast';URL='walksteadfast.com'
def plate(c,box,compact=False):
    x0,y0,x1,y1=box;cx=(x0+x1)/2;w=x1-x0;h=y1-y0;d=ImageDraw.Draw(c,'RGBA')
    lw=min(w*0.78,S(420));logo(c,cx,y0+h*0.2,lw)
    f=F(13,500);spaced(d,(cx,y0+h*0.36),'THE STEADFAST MEN PODCAST',f,ACC,0.3)
    d.line((cx-S(40),y0+h*0.41,cx+S(40),y0+h*0.41),fill=ACC+(140,),width=S(1))
    qf=F(26 if not compact else 21,500);lines=wrap(d,'“'+QUOTE+'”',qf,w*0.82)
    for i,l in enumerate(lines):d.text((cx,y0+h*0.48+i*qf.size*1.25),l,font=qf,fill=TXT,anchor='mm')
    yy=y0+h*0.66;d.text((cx,yy),URL,font=F(20,600),fill=TXT,anchor='mm')
    s=S(30);ks=['yt','x','tt','ig','fb'];gap=S(12);tot=len(ks)*s+(len(ks)-1)*gap;sx=cx-tot/2+s/2
    for i,k in enumerate(ks):icon(d,sx+i*(s+gap),yy+S(46),k,s)
    d.text((cx,yy+S(84)),'@steadfastwalk   ·   '+TAG,font=F(15,500),fill=MUT,anchor='mm')
    subscribe(c,cx,y1-S(22)-S(44),1.0,'mt')
def wrap(d,t,f,mw):
    out=[];cur=''
    for wd in t.split():
        n=(cur+' '+wd).strip()
        if d.textlength(n,font=f)>mw and cur:out.append(cur);cur=wd
        else:cur=n
    return out+[cur]
VERSE='“Whoever can be trusted with very little can also be trusted with much.”'
def board(c,box,big=False):
    x0,y0,x1,y1=box;cx=(x0+x1)/2;cy=(y0+y1)/2;w=x1-x0;d=ImageDraw.Draw(c,'RGBA')
    g=Image.new('L',(W,H),0);ImageDraw.Draw(g).ellipse((cx-w*0.35,cy-w*0.18,cx+w*0.35,cy+w*0.18),fill=60);g=g.filter(ImageFilter.GaussianBlur(S(120)))
    c.paste(Image.composite(Image.new('RGB',(W,H),ACC2),c,g))
    d=ImageDraw.Draw(c,'RGBA');sz=56 if big else 36;f=F(sz,500);lines=wrap(d,VERSE,f,w*(0.7 if big else 0.8))
    lh=f.size*1.28;top=cy-lh*len(lines)/2+S(20)
    spaced(d,(cx,top-S(56 if big else 44)),'LUKE 16:10',F(18 if big else 15,600),ACC,0.42)
    for i,l in enumerate(lines):d.text((cx,top+lh*(i+0.5)),l,font=f,fill=TXT,anchor='mm')
def bug(c,x,y,w=200):logo(c,x+S(w)/2,y,S(w))
# ---------- layouts ----------
def opt1(st):  # floating glass bubbles
    c=background();m=S(64)
    if st=='full':
        c=Image.new('RGB',(W,H),BG);board(c,(0,0,W,H),True);bug(c,m,m+S(30));subscribe(c,W-m,H-m,1,'rb')
        cam(c,(W-m-S(260),m,W-m,m+S(146)),WES,S(18));cam(c,(W-m-S(260)*2-S(16),m,W-m-S(276),m+S(146)),CO,S(18));return c
    cw,ch=(S(500),S(640)) if st=='idle' else (S(420),S(560));y=(H-ch)//2
    cam(c,(m,y,m+cw,y+ch),WES,S(36),'WES');cam(c,(W-m-cw,y,W-m,y+ch),CO,S(36),'CO-HOST')
    bx=(m+cw+S(48),y,W-m-cw-S(48),y+ch);panel(c,bx,S(36))
    plate(c,bx) if st=='idle' else (board(c,bx),subscribe(c,(bx[0]+bx[2])/2,bx[3]-S(66),0.85,'mt'),bug(c,(bx[0]+bx[2])/2-S(90),bx[1]+S(50),180))
    return c
def opt2(st):  # edge-to-edge split, center rail
    c=Image.new('RGB',(W,H),BG)
    if st=='full':
        board(c,(0,0,W,H),True);d=ImageDraw.Draw(c);d.rectangle((0,H-S(90),W,H),fill=(12,12,18));d.line((0,H-S(90),W,H-S(90)),fill=ACC,width=S(2))
        logo(c,S(150),H-S(45),S(200));d.text((W/2,H-S(45)),URL+'   ·   '+TAG,font=F(18,500),fill=MUT,anchor='mm');subscribe(c,W-S(40),H-S(23),0.9,'rb');return c
    rw=S(520) if st=='idle' else S(860);cw=(W-rw)//2
    c.paste(cover(WES[0],cw,H,WES[1],1.0,0.3),(0,0));c.paste(cover(CO[0],cw,H,CO[1],1.0,0.3),(W-cw,0))
    rail=background().crop((cw,0,cw+rw,H));c.paste(rail,(cw,0));d=ImageDraw.Draw(c)
    for x in(cw,W-cw):d.line((x,0,x,H),fill=ACC,width=S(3))
    g=Image.new('L',(W,H),0);ImageDraw.Draw(g).rectangle((cw-S(3),0,cw+S(3),H),fill=200);ImageDraw.Draw(g).rectangle((W-cw-S(3),0,W-cw+S(3),H),fill=200);g=g.filter(ImageFilter.GaussianBlur(S(18)));c.paste(Image.composite(Image.new('RGB',(W,H),ACC),c,g))
    bx=(cw+S(30),S(110),W-cw-S(30),H-S(110))
    if st=='idle':plate(c,bx)
    else:board(c,bx);logo(c,W/2,S(90),S(200));subscribe(c,W/2,H-S(110),0.9,'mt')
    for t,x in(('WES',S(40)),('CO-HOST',W-cw+S(40))):
        d=ImageDraw.Draw(c,'RGBA');spaced(d,(x,H-S(50)),t,F(16,600),TXT,0.35,'l')
    return c
def opt3(st):  # Barstool 3-up
    c=background();m=S(40);g=S(24)
    if st=='full':
        board(c,(0,0,W,H),True);bug(c,m,m+S(30));subscribe(c,W-m,H-m,1,'rb');return c
    pw=(W-2*m-2*g)//3;y0,y1=S(150),H-S(150)
    if st=='split':pw2=int(pw*1.25);pw=(W-2*m-2*g-pw2)//2
    else:pw2=pw
    cam(c,(m,y0,m+pw,y1),WES,S(20),'WES');cam(c,(W-m-pw,y0,W-m,y1),CO,S(20),'CO-HOST')
    bx=(m+pw+g,y0,m+pw+g+pw2,y1);panel(c,bx,S(20),alpha=235)
    if st=='idle':plate(c,bx)
    else:board(c,bx);subscribe(c,(bx[0]+bx[2])/2,bx[3]-S(70),0.85,'mt')
    d=ImageDraw.Draw(c);logo(c,W/2,S(78),S(260));d.text((m,S(78)),'EP. 01',font=F(18,600),fill=ACC,anchor='lm');d.text((W-m,S(78)),URL,font=F(18,500),fill=MUT,anchor='rm')
    return c
def opt4(st):  # lower-third / ticker
    c=background();m=S(56);d=ImageDraw.Draw(c)
    def lower():
        y=H-S(150);panel(c,(m,y,W-m,H-S(40)),S(18),alpha=235,gl=False);logo(c,m+S(150),y+S(55),S(220))
        dd=ImageDraw.Draw(c,'RGBA');dd.line((m+S(290),y+S(25),m+S(290),y+S(85)),fill=ACC+(140,),width=S(1))
        dd.text((m+S(320),y+S(40)),'“'+QUOTE+'”',font=F(22,500),fill=TXT,anchor='lm');dd.text((m+S(320),y+S(74)),URL+'   ·   @steadfastwalk   ·   '+TAG,font=F(15,500),fill=MUT,anchor='lm')
        ks=['yt','x','tt','ig','fb']
        for i,k in enumerate(ks):icon(dd,W-m-S(300)-i*S(40),y+S(55),ks[::-1][i],S(30))
        subscribe(c,W-m-S(24),y+S(77),0.9,'rb')
    if st=='full':
        c=Image.new('RGB',(W,H),BG);board(c,(0,0,W,H-S(150)),True);lower();return c
    if st=='idle':
        cw=(W-2*m-S(40))//2;cam(c,(m,m,m+cw,H-S(190)),WES,S(28),'WES');cam(c,(W-m-cw,m,W-m,H-S(190)),CO,S(28),'CO-HOST')
    else:
        cw=S(470);cam(c,(m,m,m+cw,H-S(190)),WES,S(28),'WES');cam(c,(W-m-cw,m,W-m,H-S(190)),CO,S(28),'CO-HOST')
        bx=(m+cw+S(40),m,W-m-cw-S(40),H-S(190));panel(c,bx,S(28));board(c,bx)
    lower();return c
def opt5(st):  # cinematic letterbox
    c=background();bh=S(150);m=S(80)
    def bars():
        d=ImageDraw.Draw(c,'RGBA');d.rectangle((0,0,W,bh),fill=BG);d.rectangle((0,H-bh,W,H),fill=BG)
        logo(c,W/2,bh/2,S(240));spaced(d,(m,bh/2),'THE STEADFAST MEN PODCAST',F(14,500),ACC,0.35,'l');d.text((W-m,bh/2),URL,font=F(17,500),fill=MUT,anchor='rm')
        d.text((m,H-bh/2),'“'+QUOTE+'”',font=F(19,500),fill=TXT,anchor='lm')
        ks=['yt','x','tt','ig','fb']
        for i,k in enumerate(ks):icon(d,W/2-S(80)+i*S(40),H-bh/2,k,S(28))
        subscribe(c,W-m,H-bh/2+S(22),0.9,'rb')
    if st=='full':c=Image.new('RGB',(W,H),BG);board(c,(0,bh,W,H-bh),True);bars();return c
    ih=H-2*bh-S(80);y=bh+S(40)
    cw=S(720) if st=='idle' else S(540)
    cam(c,(m,y,m+cw,y+ih),WES,S(16),'WES',1.0);cam(c,(W-m-cw,y,W-m,y+ih),CO,S(16),'CO-HOST',1.0)
    bx=(m+cw+S(36),y,W-m-cw-S(36),y+ih)
    if st=='idle':
        d=ImageDraw.Draw(c,'RGBA');cx=W/2;spaced(d,(cx,y+ih*0.35),'EP.',F(14,500),ACC,0.4);d.text((cx,y+ih*0.47),'01',font=F(64,300),fill=TXT,anchor='mm')
        d.line((cx-S(30),y+ih*0.6,cx+S(30),y+ih*0.6),fill=ACC,width=S(1));d.text((cx,y+ih*0.68),TAG,font=F(16,500),fill=MUT,anchor='mm')
    else:panel(c,bx,S(16));board(c,bx)
    bars();return c
def opt6(st):  # studio desk
    c=background('studio');m=S(60)
    def desk():
        bx=(W/2-S(430),H-S(230),W/2+S(430),H-S(40));panel(c,bx,S(26),alpha=225)
        d=ImageDraw.Draw(c,'RGBA');logo(c,bx[0]+S(170),bx[1]+S(70),S(260));d.text((bx[0]+S(40),bx[1]+S(140)),URL,font=F(18,600),fill=TXT,anchor='lm')
        d.text((bx[2]-S(40),bx[1]+S(52)),'“'+QUOTE+'”',font=F(17,500),fill=TXT,anchor='rm')
        ks=['yt','x','tt','ig','fb']
        for i,k in enumerate(ks):icon(d,bx[2]-S(375)+i*S(38),bx[1]+S(100),k,S(28))
        d.text((bx[2]-S(180),bx[1]+S(100)),TAG,font=F(14,500),fill=MUT,anchor='lm')
        subscribe(c,bx[2]-S(40),bx[3]-S(24),0.85,'rb')
    if st=='full':
        c=Image.new('RGB',(W,H),BG);board(c,(0,0,W,H-S(240)),True);desk();return c
    cw,ch=(S(560),S(560)) if st=='idle' else (S(440),S(500));y=S(70)
    cam(c,(m+S(40),y,m+S(40)+cw,y+ch),WES,cw//2 if st=='idle' else S(40),'WES',1.0);cam(c,(W-m-S(40)-cw,y,W-m-S(40),y+ch),CO,cw//2 if st=='idle' else S(40),'CO-HOST',1.0)
    if st=='split':bx=(m+S(40)+cw+S(40),y,W-m-S(80)-cw,y+ch);panel(c,bx,S(40));board(c,bx)
    else:
        d=ImageDraw.Draw(c);spaced(d,(W/2,y+ch*0.45),'LIVE FROM THE TABLE',F(15,600),ACC,0.4);d.text((W/2,y+ch*0.56),'Steadfast Men',font=F(40,400),fill=TXT,anchor='mm')
    desk();return c
O=dict(enumerate([opt1,opt2,opt3,opt4,opt5,opt6],1))
out='/workspace/tmp-send/podcast-plates/';os.makedirs(out+'4k',exist_ok=True)
for n in map(int,sys.argv[1:] or O):
    for st in('idle','split','full'):
        im=O[n](st);im.save(out+f'4k/opt{n}-{st}-3840.jpg',quality=94);im.resize((1920,1080),Image.LANCZOS).save(out+f'opt{n}-{st}.jpg',quality=93);print(n,st,flush=True)
