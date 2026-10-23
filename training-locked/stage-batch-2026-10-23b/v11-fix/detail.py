# v11 forehead texture + teeth tone pass. Works in the 512 FFHQ-aligned crop (same template as hq.py), pastes a delta back.
import cv2,numpy as np
FF=np.array([[192.98,239.95],[318.90,240.19],[256.63,314.02],[201.26,371.41],[313.09,371.15]],np.float32)
_C={}
def _tex(seed=11,k=1.0):
    r=np.random.default_rng(seed)
    n=r.normal(0,1,(512,512)).astype(np.float32)
    pores=cv2.GaussianBlur(n,(0,0),0.9*k)-cv2.GaussianBlur(n,(0,0),2.2*k); pores/=pores.std()
    # sparse darker pores
    sp=(r.random((512,512))<0.012/k**2).astype(np.float32); sp=cv2.GaussianBlur(sp,(0,0),1.0*k); sp/=sp.max()
    # faint horizontal forehead lines (mid-40s): 3 wavy lines
    yy,xx=np.mgrid[0:512,0:512].astype(np.float32); lines=np.zeros((512,512),np.float32)
    wob=cv2.GaussianBlur(r.normal(0,1,(512,512)).astype(np.float32),(0,0),25); wob/=wob.std()
    for y0,a in [(128,1.0),(150,0.8),(172,0.6)]:
        yc=y0+6*np.sin((xx-256)/70.0)*0+0.0006*(xx-256)**2*-1+3*wob
        lines+=a*np.exp(-((yy-yc)**2)/(2*(2.0*k)**2))*(0.6+0.4*np.cos((xx-256)/120.0))
    low=cv2.GaussianBlur(r.normal(0,1,(512,512)).astype(np.float32),(0,0),8); low/=low.std()
    return pores,sp,lines,low
P,SP,LN,LOW=_tex()
def enhance(img,kps,amt=1.0,teeth=1.0,src=None):
    M,_=cv2.estimateAffinePartial2D(kps.astype(np.float32),FF); s=np.linalg.norm(M[0,:2])
    c=cv2.warpAffine(img,M,(512,512),flags=cv2.INTER_CUBIC)
    lab=cv2.cvtColor(c,cv2.COLOR_BGR2LAB).astype(np.float32)
    # forehead mask: ellipse gated by skin colour (excludes hair/brows)
    e=np.zeros((512,512),np.float32); cv2.ellipse(e,(256,158),(100,58),0,0,360,1,-1)
    core=np.zeros((512,512),np.float32); cv2.ellipse(core,(256,165),(50,30),0,0,360,1,-1)
    ref=np.median(lab[core>0],0); d=np.sqrt(((lab-ref)*[1.0,1.6,1.6])**2).sum(-1)**0.5 if False else np.sqrt((((lab-ref)*[0.6,1.6,1.6])**2).sum(-1))
    skin=np.clip(1-(d-20)/16,0,1)
    fm=cv2.GaussianBlur(e*skin,(0,0),6)
    L=lab[...,0]
    # optional: re-inject source plate forehead high-frequency (sharpness the restore smoothed out)
    hf=0
    if src is not None:
        so=cv2.cvtColor(cv2.warpAffine(src,M,(512,512),flags=cv2.INTER_CUBIC),cv2.COLOR_BGR2LAB)[...,0].astype(np.float32)
        hf=so-cv2.GaussianBlur(so,(0,0),2.5)
    # scale-aware: pores fade when the face is small (crop upsampled by s)
    pw=float(__import__("os").environ.get("PW",1.0/max(1.0,s/2.0)))
    k=1.0 if s<1.6 else round(s/1.6,1)
    if k not in _C: _C[k]=_tex(k=k)
    tP,tSP,tLN,tLOW=_C[k]; ridge=np.roll(tLN,-int(3*k),0)
    delta=amt*(pw*(5.0*tP-9.0*tSP/k)-13.0*tLN+5.0*ridge+4.0*tLOW)*(L/180.0)+1.0*hf
    lab[...,0]=L+delta*fm
    # teeth: bright, low-chroma pixels inside the mouth -> one step down (darker, a touch warmer/less blue-white)
    mo=np.zeros((512,512),np.float32); cv2.ellipse(mo,(257,373),(52,20),0,0,360,1,-1)
    ch=np.sqrt((lab[...,1]-128)**2+(lab[...,2]-128)**2)
    tm=mo*np.clip((L-150)/30,0,1)*np.clip(1-(ch-12)/14,0,1); tm=cv2.GaussianBlur(tm,(0,0),1.2)
    lab[...,0]-=teeth*0.08*(L-120).clip(0)*tm
    lab[...,2]+=teeth*4.0*tm; lab[...,1]+=teeth*0.8*tm
    out=cv2.cvtColor(np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
    dlt=out-c.astype(np.float32)
    H,W=img.shape[:2]; Mi=cv2.invertAffineTransform(M)
    db=cv2.warpAffine(dlt,Mi,(W,H),flags=cv2.INTER_AREA)
    return np.clip(img.astype(np.float32)+db,0,255).astype(np.uint8),fm,tm
