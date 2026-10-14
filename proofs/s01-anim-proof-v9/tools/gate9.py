import cv2,numpy as np,json,sys,subprocess,glob
from PIL import Image
sys.argv_=sys.argv
from comp9 import app,big,MASTER,hair,plate,BGMAP
def frames(v):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(1280*720*3)
        if len(b)<1280*720*3: break
        yield np.frombuffer(b,np.uint8).reshape(720,1280,3)
def patches(rgb,a):
    """odd shading/colour patches inside body (lower 65% of figure): Lab deviation vs 31px median"""
    m=a>0.95; ys=np.where(m.any(1))[0]
    if len(ys)==0: return 0,0
    y0=ys.min()+int(0.35*(ys.max()-ys.min()))
    lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.int16); med=cv2.medianBlur(cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB),31).astype(np.int16)
    d=lab-med; odd=((np.abs(d[...,1])>10)|(np.abs(d[...,2])>10)|(d[...,0]<-28))&m; odd[:y0]=False
    odd=cv2.morphologyEx(odd.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab_,st,_=cv2.connectedComponentsWithStats(odd); areas=[s[4] for s in st[1:] if s[4]>=150]
    return int(len(areas)),int(max(areas) if areas else 0)
def hairm(im,f,a):
    x0,y0,x1,y1=(f.bbox.astype(int) if hasattr(f,'bbox') else f);h=y1-y0; ya,yb=max(0,y0-int(.45*h)),max(1,y0+int(.1*h)); xa=max(0,x0)
    c=cv2.cvtColor(im[ya:yb,xa:x1],cv2.COLOR_BGR2GRAY).astype(np.float64); m=a[ya:yb,xa:x1]>0.9
    sc=128/c.shape[1]; c=cv2.resize(c,(128,max(8,int(c.shape[0]*sc)))); m=cv2.resize(m.astype(np.uint8),(c.shape[1],c.shape[0]),interpolation=cv2.INTER_NEAREST)>0
    m=cv2.erode(m.astype(np.uint8),np.ones((3,3),np.uint8))>0; Lp=np.abs(cv2.Laplacian(c,cv2.CV_64F))
    return float(Lp[m].mean()) if m.sum()>50 else None
def gate(name,still):
    W=f'/workspace/s01v9/p9/work/{name}'; A=np.load(f'{W}/alpha.npy').astype(np.float32); P,L=plate(still)
    S=cv2.imread(f'/workspace/steadfast/training-locked/v9-face-master/{still}.png'); S=cv2.resize(S,(1280,720),interpolation=cv2.INTER_AREA)
    sf=big(app.get(S))
    # baseline patch count on the locked still itself
    from rembg import remove,new_session
    sa=np.asarray(remove(Image.fromarray(S[...,::-1]),session=new_session('u2net_human_seg'),only_mask=True)).astype(np.float32)/255
    bn,ba=patches(np.ascontiguousarray(S[...,::-1]),sa); sh=hairm(S,sf,sa)
    Sr=S[...,::-1].astype(np.float32); sl=((Sr[...,2]-np.maximum(Sr[...,0],Sr[...,1])>10)&(Sr.mean(2)<170)&(cv2.erode((sa>0.5).astype(np.uint8),np.ones((7,7),np.uint8))>0)).astype(np.uint8)
    _,_,st0,_=cv2.connectedComponentsWithStats(cv2.morphologyEx(sl,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))); sleak=int(max([x[4] for x in st0[1:]],default=0))
    R=[];prev=None
    for i,fr in enumerate(frames(f'/workspace/s01v9/p9/shots/{name}.mp4')):
        if i>=len(A): break
        a=A[i]; bgr=fr[...,::-1].copy(); f=big(app.get(bgr))
        sim=float(np.dot(MASTER.normed_embedding,f.normed_embedding)) if f is not None else None
        hr=hairm(bgr,f,a) if f is not None else None
        hard=a>0.5; ring=(cv2.dilate(hard.astype(np.uint8),np.ones((9,9),np.uint8))>0)&~(cv2.dilate(hard.astype(np.uint8),np.ones((3,3),np.uint8))>0)
        edge=float(np.abs(fr.astype(np.float32)-P).mean(2)[ring&(a<0.05)].mean()) if (ring&(a<0.05)).any() else 0.0
        flick=0.0;fblob=0
        if 0<i<len(A)-1:
            dd=np.abs(a-(A[i-1]+A[i+1])/2); act=(a>0.02)|(A[i-1]>0.02); flick=float(dd[act].mean())
            n_,_,st,_=cv2.connectedComponentsWithStats(cv2.erode((dd>0.5).astype(np.uint8),np.ones((5,5),np.uint8))); fblob=int(max([s[4] for s in st[1:]],default=0))
        rr,gg_,bb=[fr[...,c].astype(np.float32) for c in range(3)]
        leak=((bb-np.maximum(rr,gg_)>10)&((rr+gg_+bb)/3<170)&(cv2.erode((a>0.5).astype(np.uint8),np.ones((7,7),np.uint8))>0)).astype(np.uint8)
        leak=cv2.morphologyEx(leak,cv2.MORPH_OPEN,np.ones((3,3),np.uint8)); _,_,stl,_=cv2.connectedComponentsWithStats(leak); lk=int(max([s_[4] for s_ in stl[1:]],default=0))
        pn,pa=patches(np.ascontiguousarray(fr),a) if i%5==0 else (None,None)
        logo=bool((a[L]==0).all()) and float(np.abs(fr.astype(np.float32)-P).mean(2)[L].mean())<3.0  # composite writes plate px on logo; encoded mean diff = h264 only
        R.append(dict(i=i,leak=lk,sim=sim,hair=hr,edge=edge,flick=flick,fblob=fblob,pn=pn,pa=pa,logo=logo,face_on_logo=bool(f is not None and L[int(f.bbox[1]):int(f.bbox[3]),max(0,int(f.bbox[0])):int(f.bbox[2])].any())))
    sims=[r['sim'] for r in R if r['sim'] is not None]; hs=[r['hair'] for r in R if r['hair']]; hs=[float(np.median(hs[max(0,j-2):j+3])) for j in range(len(hs))]
    pns=[r['pn'] for r in R if r['pn'] is not None]; pas=[r['pa'] for r in R if r['pa'] is not None]
    s=dict(name=name,still=still,frames=len(R),face_missing=sum(r['sim'] is None for r in R),sim_min=min(sims),sim_mean=float(np.mean(sims)),
        still_hair=sh,hair_max=max(hs),hair_rise_pct=100*(max(hs)/sh-1),edge_max=max(r['edge'] for r in R),flick_max=max(r['flick'] for r in R),
        flick_blob_max=max(r['fblob'] for r in R),patch_baseline=[bn,ba],patch_max_n=max(pns),patch_max_area=max(pas),
        leak_max=max(r['leak'] for r in R),leak_still=sleak,logo_ok=all(r['logo'] for r in R),face_on_logo=any(r['face_on_logo'] for r in R))
    s['pass_face']=s['sim_min']>=0.85 and s['face_missing']==0
    s['pass_hair']=s['hair_rise_pct']<=15
    s['pass_edge']=s['leak_max']<=max(150,1.5*sleak) and s['edge_max']<=8 and s['flick_max']<=0.05 and s['flick_blob_max']<=900 and s['patch_max_n']<=bn+2 and s['patch_max_area']<=max(600,1.5*ba)
    s['pass_logo']=s['logo_ok'] and not s['face_on_logo']
    json.dump({'summary':s,'frames':R},open(f'{W}/gate.json','w'),indent=0)
    # visual edge/arm sheet: 8 frames, left+right body edge crops
    cap=cv2.VideoCapture(f'/workspace/s01v9/p9/shots/{name}.mp4'); idx=np.linspace(0,len(R)-1,8).astype(int); tiles=[]
    for j in idx:
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(j)); ok,im=cap.read(); a=A[j]; ys,xs=np.where(a>0.5)
        y0=ys.min()+int(0.3*(ys.max()-ys.min()))
        for x in (xs.min(),xs.max()):
            c=im[y0:720,max(0,x-90):min(1280,x+90)]; c=cv2.resize(c,(180,300)); tiles.append(c)
    rows=[np.hstack(tiles[k:k+8]) for k in range(0,16,8)]; cv2.imwrite(f'/workspace/s01v9/p9/qa/{name}_edges.jpg',np.vstack(rows))
    print(json.dumps(s)); return s
if __name__=='__main__':
    import os; os.makedirs('/workspace/s01v9/p9/qa',exist_ok=True); gate(sys.argv[1],sys.argv[2])
