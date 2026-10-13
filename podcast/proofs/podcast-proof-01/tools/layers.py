import os,sys,random
os.chdir('/workspace/tmp-send/podcast-plates')
src_txt=open('comp.py').read().split("O=dict(")[0].split('# ---------- layouts')[0].replace('K=2','K=1')
exec(src_txt)
IC={k:Image.open(f'/workspace/pp1/build/icons/{n}.png').convert('RGBA') for k,n in dict(yt='youtube',x='x',tt='tiktok',ig='instagram',fb='facebook').items()}
def icon(d,cx,cy,k,s):
    r=s/2;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=ACC+(160,),width=max(1,int(s*0.05)))
    g=int(s*0.5);im=IC[k].resize((g,g),Image.LANCZOS);d._image.paste(im,(int(cx-g/2),int(cy-g/2)),im)
def plate(c,box,compact=False):
    x0,y0,x1,y1=box;cx=(x0+x1)/2;w=x1-x0;h=y1-y0;d=ImageDraw.Draw(c,'RGBA')
    lw=min(w*0.78,S(420));logo(c,cx,y0+h*0.2,lw)
    f=F(13,500);spaced(d,(cx,y0+h*0.36),'THE STEADFAST MEN PODCAST',f,ACC,0.3)
    d.line((cx-S(40),y0+h*0.41,cx+S(40),y0+h*0.41),fill=ACC+(140,),width=S(1))
    qf=F(26,500);lines=wrap(d,'“'+QUOTE+'”',qf,w*0.82)
    for i,l in enumerate(lines):d.text((cx,y0+h*0.48+i*qf.size*1.25),l,font=qf,fill=TXT,anchor='mm')
    yy=y0+h*0.66;d.text((cx,yy),URL,font=F(20,600),fill=TXT,anchor='mm')
    s=S(30);ks=['yt','x','tt','ig','fb'];gap=S(12);tot=len(ks)*s+(len(ks)-1)*gap;sx=cx-tot/2+s/2
    for i,k in enumerate(ks):icon(d,sx+i*(s+gap),yy+S(46),k,s)
    d.text((cx,yy+S(84)),'@steadfastwalk   ·   '+TAG,font=F(15,500),fill=MUT,anchor='mm')
    subscribe(c,cx,y1-S(22)-S(44),1.0,'mt')
def bar(c):
    m=S(56);y=H-S(150);panel(c,(m,y,W-m,H-S(40)),S(18),alpha=235,gl=False);d=ImageDraw.Draw(c,'RGBA')
    qf=F(22,500);sf=F(15,500);q='“'+QUOTE+'”';l2=URL+'   ·   @steadfastwalk   ·   '+TAG
    lw=S(220);cy=y+S(55);logo(c,m+S(30)+lw/2,cy,lw);d=ImageDraw.Draw(c,'RGBA')
    d.text((W/2,y+S(40)),q,font=qf,fill=TXT,anchor='mm');d.text((W/2,y+S(74)),l2,font=sf,fill=MUT,anchor='mm')
    for i,k in enumerate(['yt','x','tt','ig','fb']):icon(d,W-m-S(460)+i*S(40),cy,k,S(30))
    subscribe(c,W-m-S(24),y+S(77),0.9,'rb');return c
def myboard(c,box,kicker,line,big=False):
    x0,y0,x1,y1=box;cx=(x0+x1)/2;cy=(y0+y1)/2;w=x1-x0
    g=Image.new('L',(W,H),0);ImageDraw.Draw(g).ellipse((cx-w*0.35,cy-w*0.18,cx+w*0.35,cy+w*0.18),fill=60);g=g.filter(ImageFilter.GaussianBlur(S(120)))
    c.paste(Image.composite(Image.new('RGB',(W,H),ACC2),c,g));d=ImageDraw.Draw(c,'RGBA')
    sz=56 if big else 36;f=F(sz,500);lines=wrap(d,line,f,w*(0.72 if big else 0.82))
    lh=f.size*1.28;top=cy-lh*len(lines)/2+S(20)
    spaced(d,(cx,top-S(56 if big else 44)),kicker,F(18 if big else 15,600),ACC,0.42)
    for i,l in enumerate(lines):d.text((cx,top+lh*(i+0.5)),l,font=f,fill=TXT,anchor='mm')
def label(o,box,txt):
    x0,y0,x1,y1=box;d=ImageDraw.Draw(o);f=F(15,600);tw=d.textlength(txt,font=f)
    px,py=x0+S(18),y1-S(18)-S(34)
    d.rounded_rectangle((px,py,px+tw+S(28),py+S(34)),S(17),fill=(7,7,10,200),outline=ACC+(180,),width=S(1))
    d.text((px+S(14),py+S(17)),txt,font=f,fill=TXT,anchor='lm')
def bubbles(c,cw,ch,y):
    m=S(64);bw=(m,y,m+cw,y+ch);bj=(W-m-cw,y,W-m,y+ch)
    for b in (bw,bj):glow(c,b,S(36),a=170)
    o=Image.new('RGBA',(W,H))
    for b,t in ((bw,'WES'),(bj,'JONATHON')):ImageDraw.Draw(o).rounded_rectangle(b,S(36),outline=ACC+(230,),width=3);label(o,b,t)
    return bw,bj,o
OUT='/workspace/pp1/build/L/';os.makedirs(OUT,exist_ok=True)
import pickle;meta={}
# idle
c=background();cw,ch=500,640;y=(H-ch)//2;bw,bj,o=bubbles(c,cw,ch,y);m=64
bx=(m+cw+48,y,W-m-cw-48,y+ch);panel(c,bx,36);plate(c,bx);c.save(OUT+'idle.png');o.save(OUT+'idle_o.png');meta['idle']=(bw,bj)
# splits
BOARDS={'b1':('MATTHEW 5:9','“Blessed are the peacemakers.”'),'b2':('THE FIRST MARK','Stop waiting.')}
for k,(ki,li) in BOARDS.items():
    c=background();cw,ch=420,560;y=(H-ch)//2-40;bw,bj,o=bubbles(c,cw,ch,y)
    bx=(m+cw+48,y,W-m-cw-48,y+ch);panel(c,bx,36);myboard(c,bx,ki,li);bar(c);c.save(OUT+k+'.png');o.save(OUT+k+'_o.png');meta[k]=(bw,bj)
FULL={'b3':('GALATIANS 6:2','“Carry each other’s burdens.”'),'b4':('JAMES 4:17','“If anyone, then, knows the good they ought to do and doesn’t do it, it is sin for them.”')}
for k,(ki,li) in FULL.items():
    c=Image.new('RGB',(W,H),BG);myboard(c,(0,0,W,H-150),ki,li,True);bar(c);c.save(OUT+k+'.png')
# bar overlay for fullhost
c=Image.new('RGB',(W,H),BG);bar(c);mk=Image.new('L',(W,H),0);ImageDraw.Draw(mk).rounded_rectangle((56,H-150,W-56,H-40),18,fill=255)
c.putalpha(mk);c.save(OUT+'bar_o.png')
# end card: idle + disclosure
c=Image.open(OUT+'idle.png');d=ImageDraw.Draw(c);d.text((W/2,H-34),'Produced with AI voice and video tools.',font=F(16,500),fill=MUT,anchor='mm');c.save(OUT+'end.png')
pickle.dump(meta,open(OUT+'meta.pkl','wb'));print(meta)
