import json,subprocess,random,pickle,sys,os,numpy as np
from PIL import Image,ImageDraw
random.seed(7)
FPS=24;T0=5.0;TOTAL=174.0;NF=int(TOTAL*FPS);SW,SH=1344,768;W,H=1920,1080
P='/workspace/pp1/';L=P+'build/L/'
tl=json.load(open(P+'audio/timeline.json'))
LS={'W':sys.argv[1] if len(sys.argv)>1 else P+'ls/W_base.mp4','J':sys.argv[2] if len(sys.argv)>2 else P+'ls/J_base.mp4'}
OUTF=sys.argv[3] if len(sys.argv)>3 else P+'out/test.mp4'
LIMIT=float(sys.argv[4]) if len(sys.argv)>4 else TOTAL
POOL={'W':['wes_listen1_f','wes_listen1_r','wes_sip_f','wes_listen1_f','wes_listen1_r','wes_listen1_f'],
      'J':['jon_listen1_f','jon_listen1_r','jon_listen1_f','jon_sip_f','jon_listen1_f','jon_listen1_r']}
for h in 'WJ':
    for n in set(POOL[h]):
        b=n[:-2]
        if not os.path.exists(P+f'ls/{b}_f.mp4'):
            subprocess.run(f'ffmpeg -v error -y -i {P}clips/{b}.mp4 -vf "scale={SW}:{SH},fps=24,format=yuv420p" -an {P}ls/{b}_f.mp4 && ffmpeg -v error -y -i {P}ls/{b}_f.mp4 -vf reverse {P}ls/{b}_r.mp4',shell=True)
# ---- host tracks
def track(h):
    pieces=[];cuts=[];t=0.0;lsoff=0.0;pi=0;pc=0.0
    spk=[(T0+x['t'],x['d']) for x in tl if x['h']==h]
    def listen(dur):
        nonlocal pi,pc,t
        while dur>1e-3:
            n=POOL[h][pi%len(POOL[h])];take=min(dur,10.0-pc)
            pieces.append((P+f'ls/{n}.mp4',pc,take));
            if pc==0.0 and t>0 and ('sip' in n or 'sip' in POOL[h][(pi-1)%len(POOL[h])]):cuts.append(t)
            t+=take;dur-=take;pc+=take
            if pc>=10.0-1e-3:pi+=1;pc=0.0
    for s,d in spk:
        if s>t:listen(s-t)
        if not cuts or abs(cuts[-1]-t)>0.3:cuts.append(t)
        pieces.append((LS[h],lsoff,d));lsoff+=d;t+=d;cuts.append(t)
    listen(TOTAL-t+0.5)
    lst=P+f'build/{h}_pieces.txt';os.makedirs(P+'build/pc',exist_ok=True)
    with open(lst,'w') as f:
        for i,(fn,a,d) in enumerate(pieces):
            o=P+f'build/pc/{h}{i:03d}.mp4'
            subprocess.run(f'ffmpeg -v error -y -ss {a:.3f} -i {fn} -t {d:.3f} -vf "scale={SW}:{SH},fps=24,format=yuv420p" -an -c:v libx264 -crf 14 -preset veryfast {o}',shell=True)
            f.write(f"file '{o}'\n")
    subprocess.run(f'ffmpeg -v error -y -f concat -safe 0 -i {lst} -c:v libx264 -crf 14 -preset veryfast -r 24 {P}build/{h}_track.mp4',shell=True)
    return sorted(set(round(c,2) for c in cuts))
CUTS={h:track(h) for h in 'WJ'}
json.dump(CUTS,open(P+'build/cuts.json','w'))
# ---- layout schedule
SCHED=[(0,5,'idle'),(T0+33,T0+41,'fhW'),(T0+62,T0+78,'b1'),(T0+93,T0+100,'fhW'),(T0+114,T0+123,'b2'),(T0+125,T0+131.5,'fhJ'),(T0+138,T0+147,'b3'),(T0+152.3,T0+163,'b4'),(T0+163,TOTAL+1,'end')]
def state(t):
    for a,b,s in SCHED:
        if a<=t<b:return s
    return 'idle'
meta=pickle.load(open(L+'meta.pkl','rb'));meta['end']=meta['idle']
LAY={k:Image.open(L+k+'.png').convert('RGB') for k in ['idle','b1','b2','b3','b4','end']}
OV={k:Image.open(L+k+'_o.png') for k in ['idle','b1','b2']};OV['end']=OV['idle'];BAR=Image.open(L+'bar_o.png')
FACE={'W':(420,250),'J':(700,245)}
FR={'W':[(450,768),(425,620),(420,470),(500,700)],'J':[(680,768),(700,620),(700,470),(640,700)]}
def plan(h):
    cs=[0.0]+[c for c in CUTS[h] if c>0.5]+[TOTAL]
    # split long spans
    out=[]
    for a,b in zip(cs,cs[1:]):
        n=max(1,int((b-a)//6.5));out+=[a+(b-a)*i/n for i in range(n)]
    segs=[];prev=-1
    for a,b in zip(out,out[1:]+[TOTAL]):
        k=random.choice([i for i in range(4) if i!=prev]);prev=k;segs.append((a,b,k))
    return segs
PL={h:plan(h) for h in 'WJ'}
def frm(h,t):
    for a,b,k in PL[h]:
        if a<=t<b:return k,(t-a)/max(b-a,0.1)
    return 0,0
MASK={}
def rmask(w,h,r=36):
    if (w,h) not in MASK:
        m=Image.new('L',(w*2,h*2),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w*2-1,h*2-1),r*2,fill=255);MASK[(w,h)]=m.resize((w,h),Image.LANCZOS)
    return MASK[(w,h)]
def crop(im,h,t,bw,bh):
    k,p=frm(h,t);cx,hh=FR[h][k];hh=hh*(1-0.04*p)  # slow push-in
    ww=hh*bw/bh;fx,fy=FACE[h];top=fy-0.38*hh;top=max(0,min(top,SH-hh));x0=max(0,min(cx-ww/2,SW-ww))
    return im.resize((bw,bh),Image.LANCZOS,box=(x0,top,x0+ww,top+hh))
def compose(s,t,fw,fj):
    if s in('b3','b4'):return LAY[s].copy()
    if s.startswith('fh'):
        h=s[2];im=fw if h=='W' else fj;hh=690*(1-0.05*((t*0.1)%1));ww=hh*16/9;cx={'W':520,'J':640}[h]
        x0=max(0,min(cx-ww/2,SW-ww));top=max(0,min(FACE[h][1]-0.36*hh,SH-hh))
        c=im.resize((W,H),Image.LANCZOS,box=(x0,top,x0+ww,top+hh));c.paste(BAR,(0,0),BAR);return c
    c=LAY[s].copy();bw,bj=meta[s]
    for b,h,im in((bw,'W',fw),(bj,'J',fj)):
        w,hgt=b[2]-b[0],b[3]-b[1];c.paste(crop(im,h,t,w,hgt),(b[0],b[1]),rmask(w,hgt))
    c.paste(OV[s],(0,0),OV[s]);return c
def reader(f):return subprocess.Popen(['ffmpeg','-v','error','-i',f,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,bufsize=10**8)
rw,rj=reader(P+'build/W_track.mp4'),reader(P+'build/J_track.mp4')
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',P+'build/video_noaudio.mp4'],stdin=subprocess.PIPE)
fsz=SW*SH*3;last=None;prevs=None;xf=0
nf=int(min(LIMIT,TOTAL)*FPS)
for i in range(nf):
    t=i/FPS;a=rw.stdout.read(fsz);b=rj.stdout.read(fsz)
    fw=Image.frombytes('RGB',(SW,SH),a) if len(a)==fsz else fw
    fj=Image.frombytes('RGB',(SW,SH),b) if len(b)==fsz else fj
    s=state(t);c=compose(s,t,fw,fj)
    if prevs is not None and s!=prevs:xf=8;oldst=prevs
    if xf>0:
        o=compose(oldst,t,fw,fj);c=Image.blend(c,o,xf/9);xf-=1
    if i<12:c=Image.blend(Image.new('RGB',(W,H)),c,i/12)
    if i>nf-18:c=Image.blend(Image.new('RGB',(W,H)),c,max(0,(nf-i)/18))
    prevs=s;enc.stdin.write(c.tobytes())
    if i%480==0:print('frame',i,flush=True)
    if i in (int(12*24),int((T0+70)*24),int((T0+36)*24),int((T0+142)*24)):c.save(P+f'build/still_{i}.jpg',quality=92)
enc.stdin.close();enc.wait();print('done')
