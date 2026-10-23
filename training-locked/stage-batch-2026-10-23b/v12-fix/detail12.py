# v12 forehead texture + teeth pass. 512 FFHQ-aligned crop (hq.py template); delta pasted back.
# Creases: 3 wide, soft, uneven-length horizontal folds (dark valley + highlight shoulder). Pores: fine, density-modulated (no orange peel). Tone: soft mottling.
import cv2,numpy as np
FF=np.array([[192.98,239.95],[318.90,240.19],[256.63,314.02],[201.26,371.41],[313.09,371.15]],np.float32)
_C={}
def _tex(k=1.0,seed=12):
    r=np.random.default_rng(seed); g=lambda s:(lambda n:n/n.std())(cv2.GaussianBlur(r.normal(0,1,(512,512)).astype(np.float32),(0,0),s))
    n=r.normal(0,1,(512,512)).astype(np.float32)
    pores=cv2.GaussianBlur(n,(0,0),0.6*k)-cv2.GaussianBlur(n,(0,0),1.4*k); pores/=pores.std()
    dens=np.clip(0.9+0.6*g(18),0.2,1.8)                      # uneven pore density
    sp=(r.random((512,512))<0.004/k**2).astype(np.float32); sp=cv2.GaussianBlur(sp,(0,0),0.8*k); sp/=sp.max()+1e-6
    yy,xx=np.mgrid[0:512,0:512].astype(np.float32); val=np.zeros((512,512),np.float32); sh=np.zeros_like(val)
    wob=g(30)
    for y0,a,x0,x1 in [(126,1.0,170,345),(147,0.85,160,355),(169,0.6,185,330)]:
        yc=y0-0.0005*(xx-256)**2+2.5*wob
        win=np.clip((xx-x0)/30,0,1)*np.clip((x1-xx)/30,0,1)*(0.75+0.25*g(12))
        val+=a*win*np.exp(-((yy-yc)**2)/(2*(3.2*k)**2))
        sh+=a*win*np.exp(-((yy-(yc+6.5*k))**2)/(2*(4.0*k)**2))
    tone=g(14*k)
    return pores*dens,sp,val,sh,tone
def enhance(img,kps,amt=1.0,teeth=1.0,src=None,pore=1.0,crease=1.0,tonal=1.0,srchf=0.0):
    M,_=cv2.estimateAffinePartial2D(kps.astype(np.float32),FF); s=np.linalg.norm(M[0,:2])
    c=cv2.warpAffine(img,M,(512,512),flags=cv2.INTER_CUBIC)
    lab=cv2.cvtColor(c,cv2.COLOR_BGR2LAB).astype(np.float32); L=lab[...,0].copy()
    e=np.zeros((512,512),np.float32); cv2.ellipse(e,(256,158),(100,58),0,0,360,1,-1)
    core=np.zeros((512,512),np.float32); cv2.ellipse(core,(256,165),(50,30),0,0,360,1,-1)
    ref=np.median(lab[core>0],0); d=np.sqrt((((lab-ref)*[0.6,1.6,1.6])**2).sum(-1))
    fm=cv2.GaussianBlur(e*np.clip(1-(d-20)/16,0,1),(0,0),7)
    k=1.0 if s<1.6 else round(s/1.6,1)
    if k not in _C: _C[k]=_tex(k)
    P,SP,V,SH,T=_C[k]
    hf=0
    if src is not None and srchf>0:
        so=cv2.cvtColor(cv2.warpAffine(src,M,(512,512),flags=cv2.INTER_CUBIC),cv2.COLOR_BGR2LAB)[...,0].astype(np.float32)
        hf=cv2.GaussianBlur(so,(0,0),0.8*k)-cv2.GaussianBlur(so,(0,0),3.0*k)
    delta=amt*(pore*(2.6*P-6.0*SP)/k**0.5+crease*(-11.0*V+4.0*SH)+tonal*2.2*T)*(L/180.0)+srchf*hf
    lab[...,0]=L+delta*fm
    mo=np.zeros((512,512),np.float32); cv2.ellipse(mo,(257,373),(54,22),0,0,360,1,-1)
    ch=np.sqrt((lab[...,1]-128)**2+(lab[...,2]-128)**2)
    tm=mo*np.clip((L-135)/30,0,1)*np.clip(1-(ch-14)/14,0,1); tm=cv2.GaussianBlur(tm,(0,0),1.2)
    lab[...,0]-=teeth*0.15*(L-110).clip(0)*tm; lab[...,2]+=teeth*7.0*tm; lab[...,1]+=teeth*1.2*tm
    out=cv2.cvtColor(np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
    H,W=img.shape[:2]; db=cv2.warpAffine(out-c.astype(np.float32),cv2.invertAffineTransform(M),(W,H),flags=cv2.INTER_AREA)
    return np.clip(img.astype(np.float32)+db,0,255).astype(np.uint8),fm,tm
