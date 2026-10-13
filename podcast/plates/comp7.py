import sys;sys.argv=['x','0']
exec(open('comp.py').read().split("O=dict(")[0])
IC={k:Image.open(f'icons/{n}.png').convert('RGBA') for k,n in dict(yt='youtube',x='x',tt='tiktok',ig='instagram',fb='facebook').items()}
def icon(d,cx,cy,k,s):
    r=s/2;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=ACC+(160,),width=max(1,int(s*0.05)))
    g=int(s*0.5);im=IC[k].resize((g,g),Image.LANCZOS);d._image.paste(im,(int(cx-g/2),int(cy-g/2)),im)
def bar(c):
    m=S(56)
    y=H-S(150);panel(c,(m,y,W-m,H-S(40)),S(18),alpha=235,gl=False);d=ImageDraw.Draw(c,'RGBA')
    qf=F(22,500);sf=F(15,500);q='“'+QUOTE+'”';l2=URL+'   ·   @steadfastwalk   ·   '+TAG
    tw=max(d.textlength(q,font=qf),d.textlength(l2,font=sf));lw=S(220);gw=lw+S(60)+tw
    right0=W-m-S(480);gx=(m+right0)/2-gw/2;cy=y+S(55)
    logo(c,m+S(30)+lw/2,cy,lw);d=ImageDraw.Draw(c,'RGBA')
    d.text((W/2,y+S(40)),q,font=qf,fill=TXT,anchor='mm');d.text((W/2,y+S(74)),l2,font=sf,fill=MUT,anchor='mm')
    ks=['yt','x','tt','ig','fb']
    for i,k in enumerate(ks):icon(d,W-m-S(460)+i*S(40),cy,k,S(30))
    subscribe(c,W-m-S(24),y+S(77),0.9,'rb');return c
def full7():
    c=Image.new('RGB',(W,H),BG);board(c,(0,0,W,H-S(150)),True);return bar(c)
def split7():
    c=background();m=S(64);cw,ch=S(420),S(560);y=(H-ch)//2-S(40)
    cam(c,(m,y,m+cw,y+ch),WES,S(36),'WES');cam(c,(W-m-cw,y,W-m,y+ch),CO,S(36),'CO-HOST')
    bx=(m+cw+S(48),y,W-m-cw-S(48),y+ch);panel(c,bx,S(36));board(c,bx);return bar(c)
out='/workspace/tmp-send/podcast-plates/'
for st in('idle','split','full'):
    im={'full':full7,'split':split7}.get(st,lambda:opt1('idle'))()
    im.save(out+f'4k/opt7-hybrid-{st}-3840.jpg',quality=94);im.resize((1920,1080),Image.LANCZOS).save(out+f'opt7-hybrid-{st}.jpg',quality=93)
S3=Image.new('RGB',(3*960+40,540+60),BG);dd=ImageDraw.Draw(S3);ff=ImageFont.truetype(GE,22)
for j,st in enumerate(('idle','split','full')):
    S3.paste(Image.open(out+f'opt7-hybrid-{st}.jpg').resize((960,540),Image.LANCZOS),(10+j*970,50));dd.text((10+j*970,14),'OPTION 7 HYBRID — '+st,font=ff,fill=ACC)
S3.save(out+'opt7-hybrid-sheet.jpg',quality=92)
