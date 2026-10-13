import sys,os,json,subprocess,numpy as np,cv2
from PIL import Image
from rembg import remove,new_session
S=None
ANG={'a1':(0.80,0.22),}
def stats(src):
    im=np.array(Image.open(f'clips/idle{src}_f/00100.png').convert('RGB')).astype(np.float32)
    m=np.array(remove(Image.fromarray(im.astype(np.uint8)).resize((945,540)),session=sess(),only_mask=True).resize((im.shape[1],im.shape[0])))>128
    p=im[m]; return p.mean(0),p.std(0)
def sess():
    global S
    if S is None: S=new_session('u2net_human_seg')
    return S
def grade_params():
    if os.path.exists('grade.json'): return json.load(open('grade.json'))
    ref=stats('73'); G={}
    for s in ['73','72','80','89']:
        m,sd=stats(s); a=ref[1]/sd; b=ref[0]-a*m
        a=0.7*a+0.3; b=0.7*b  # partial match
        G[s]=[a.tolist(),b.tolist()]
    json.dump(G,open('grade.json','w')); return G
LET=None
def matte(frames):
    al=[]
    for f in frames:
        im=Image.fromarray(f); a=np.array(remove(im.resize((945,540)),session=sess(),only_mask=True)).astype(np.float32)/255
        if LET is not None: a[LET>0]=0
        al.append(a)
    al=np.array(al); sm=al.copy()
    for i in range(len(al)): sm[i]=al[max(0,i-1):i+2].mean(0)  # temporal smoothing
    return sm
def run(name,video,t0,dur,src,bg,cx,top,audio=None,fps=24,flip=False,x1=None,zoom=1.0,stab=0,stabkeep=0.35,dering=False):
    G=grade_params(); a,b=[np.array(x,np.float32) for x in G[src]]
    B=np.array(Image.open(f'v7/bg/A_{bg}.png').convert('RGB')).astype(np.float32); OH,OW=B.shape[:2]
    tmp=f'/tmp/_f_{name}'; os.makedirs(tmp,exist_ok=True); subprocess.run(f'rm -f {tmp}/*',shell=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t0),'-i',video,'-t',str(dur),'-r',str(fps),f'{tmp}/%05d.png'],check=True)
    fs=sorted(os.listdir(tmp))
    class LF(list):
        def __getitem__(s_,i):
            a_=np.array(Image.open(f'{tmp}/{fs[i]}').convert('RGB'))
            if dering:
                from dering import dering as DR
                a_=DR(a_[...,::-1].copy())[...,::-1].copy()
            return a_
        def __iter__(s_): return (s_[i] for i in range(len(fs)))
        def __len__(s_): return len(fs)
    frames=LF()
    if flip: frames=[f[:,::-1].copy() for f in frames]
    global LET
    idx=np.linspace(0,len(frames)-1,15).astype(int)
    med=np.median(np.stack([np.array(Image.fromarray(frames[i]).resize((945,540))).astype(np.int16) for i in idx]),0)
    Lm=med.mean(2); let=(Lm>110)&(med[...,2]>=med[...,0]+5); let[int(540*0.5):]=False
    LET=cv2.dilate(let.astype(np.uint8),np.ones((7,7),np.uint8))
    A=matte(frames); h,w=frames[0].shape[:2]
    a0=cv2.resize(A[len(A)//2],(w,h)); ys,xs=np.where(a0>0.5); ytop=ys.min()
    k=(OH*(1-top))/(h-ytop)*zoom; sw,sh=int(w*k),int(h*k)
    out=f'v7/shots/{name}.mp4'
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{OW}x{OH}','-r',str(fps),'-i','-']
    if audio: cmd+=['-i',audio,'-af',f'apad=whole_dur={dur}','-c:a','aac','-b:a','192k','-t',str(dur)]
    cmd+=['-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p',out]
    P=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    if x1 is not None or stab:
        TR=[]
        for a_ in A:
            m=(a_>0.5).astype(np.uint8); n,lab,st,cen=cv2.connectedComponentsWithStats(m)
            j=1+np.argmax(st[1:,4]); mm=lab==j; ys_=np.where(mm.any(1))[0]; yt=ys_.min(); yb=yt+(ys_.max()-yt)*0.3
            c_=np.where(mm[yt:int(yb)+1].any(0))[0]; TR.append((c_.min()+c_.max())/2*w/a_.shape[1])
            # also clean matte: keep only main component
            a_*=cv2.dilate(mm.astype(np.uint8),np.ones((7,7),np.uint8))
        TR=np.convolve(np.pad(TR,6,mode='edge'),np.ones(13)/13,'valid')
        if stab:
            W_=int(stab*fps)|1; SL=np.convolve(np.pad(TR,W_//2,mode='edge'),np.ones(W_)/W_,'valid')
            # keep 35% of slow drift so he still drifts a little; cancel the rest
            SL=SL-stabkeep*(SL-SL[len(SL)//2])
    for i,(f,al) in enumerate(zip(frames,A)):
        al=cv2.resize(al,(w,h)); al=cv2.erode(al,np.ones((3,3),np.uint8)); al=cv2.GaussianBlur(al,(5,5),0)
        g=np.clip(f.astype(np.float32)*a+b,0,255)
        gs=cv2.resize(g,(sw,sh),interpolation=cv2.INTER_AREA if k<1 else cv2.INTER_CUBIC); as_=cv2.resize(al,(sw,sh))
        if stab: c=cx; xc=SL[i]
        elif x1 is None: c=cx; xc=np.average(xs)
        else:
            u=i/max(1,len(frames)-1); c=cx+(x1-cx)*u
            xc=TR[i]
        px=int(c*OW - xc*k); py=int(top*OH-ytop*k)
        O=B.copy()
        qa_,qb_=max(0,px),min(OW,px+sw); y1=max(0,py); yb_=min(OH,py+sh)
        if qb_>qa_:
            sub_a=as_[y1-py:yb_-py, qa_-px:qb_-px,None]; sub=gs[y1-py:yb_-py, qa_-px:qb_-px]
            O[y1:yb_,qa_:qb_]=O[y1:yb_,qa_:qb_]*(1-sub_a)+sub*sub_a
        P.stdin.write(O.astype(np.uint8).tobytes())
    P.stdin.close(); P.wait(); subprocess.run(f'rm -rf {tmp}',shell=True); print('done',out)
if __name__=='__main__':
    j=json.loads(sys.argv[1]); run(**j)
