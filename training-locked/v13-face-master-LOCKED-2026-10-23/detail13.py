# v13 forehead pass: strong, frame-scale-visible creases with shading, brow-ridge definition, tone variation, specular breakup,
# + real skin high-frequency transplanted from a CC-licensed reference forehead. Delta is zero-mean over the forehead (no lightening).
import cv2,numpy as np
FF=np.array([[192.98,239.95],[318.90,240.19],[256.63,314.02],[201.26,371.41],[313.09,371.15]],np.float32)
_C={}
def _g(r,s): n=cv2.GaussianBlur(r.normal(0,1,(512,512)).astype(np.float32),(0,0),s); return n/n.std()
def _tex(k=1.0,seed=13,ref=None):
    r=np.random.default_rng(seed); yy,xx=np.mgrid[0:512,0:512].astype(np.float32)
    n=r.normal(0,1,(512,512)).astype(np.float32)
    pores=cv2.GaussianBlur(n,(0,0),0.7*k)-cv2.GaussianBlur(n,(0,0),1.6*k); pores/=pores.std(); pores*=np.clip(0.9+0.6*_g(r,18),0.2,1.8)
    val=np.zeros((512,512),np.float32); sh=np.zeros_like(val); wob=_g(r,30)
    for y0,a,x0,x1 in [(122,1.0,165,350),(145,0.9,155,360),(168,0.7,180,335)]:
        yc=y0-0.0006*(xx-256)**2+3*wob
        win=np.clip((xx-x0)/35,0,1)*np.clip((x1-xx)/35,0,1)*(0.7+0.3*_g(r,10))
        val+=a*win*np.exp(-((yy-yc)**2)/(2*(4.5*k)**2))
        sh+=a*win*np.exp(-((yy-(yc+9*k))**2)/(2*(5.5*k)**2))
    # brow ridge: light band just above brows, shadow in the dip above it
    ridge=np.exp(-((yy-192)**2)/(2*9.0**2))-0.8*np.exp(-((yy-178)**2)/(2*8.0**2))
    tone=_g(r,12*k); spec=_g(r,5*k)
    rhf=0
    if ref is not None:
        R=ref.astype(np.float32); rhf=R-cv2.GaussianBlur(R,(0,0),7*k); rhf=cv2.GaussianBlur(rhf,(0,0),0.5*k); rhf/=rhf[100:200,180:330].std()+1e-6
    return pores,val,sh,ridge,tone,spec,rhf
REF=None
def set_ref(L512): global REF; REF=L512; _C.clear()
def enhance(img,kps,teeth=1.0,pore=1.0,crease=1.0,brow=1.0,tonal=1.0,spec=1.0,refw=1.0):
    M,_=cv2.estimateAffinePartial2D(kps.astype(np.float32),FF); s=np.linalg.norm(M[0,:2])
    c=cv2.warpAffine(img,M,(512,512),flags=cv2.INTER_CUBIC)
    lab=cv2.cvtColor(c,cv2.COLOR_BGR2LAB).astype(np.float32); L=lab[...,0].copy()
    e=np.zeros((512,512),np.float32); cv2.ellipse(e,(256,160),(104,62),0,0,360,1,-1)
    core=np.zeros((512,512),np.float32); cv2.ellipse(core,(256,165),(50,30),0,0,360,1,-1)
    ref=np.median(lab[core>0],0); d=np.sqrt((((lab-ref)*[0.6,1.6,1.6])**2).sum(-1))
    fm=cv2.GaussianBlur(e*np.clip(1-(d-22)/16,0,1),(0,0),6)
    k=1.0 if s<1.6 else round(s/1.6,1)
    if k not in _C: _C[k]=_tex(k,ref=REF)
    P,V,SH,BR,T,SP,RH=_C[k]
    Ls=L/170.0
    hi=np.clip((L-np.percentile(L[core>0],60))/25,0,1)       # existing shine areas
    delta=(pore*2.2*P/k**0.5 + crease*(-22.0*V+7.0*SH) + brow*6.0*BR + tonal*4.0*T + refw*3.0*RH)*Ls - spec*7.0*hi*np.clip(SP,0,None)
    w=fm*(fm>0.05); delta-= (delta*w).sum()/(w.sum()+1e-6)     # zero-mean: keep v10 forehead tone
    lab[...,0]=L+delta*fm
    mo=np.zeros((512,512),np.float32); cv2.ellipse(mo,(257,373),(54,22),0,0,360,1,-1)
    ch=np.sqrt((lab[...,1]-128)**2+(lab[...,2]-128)**2)
    tm=mo*np.clip((L-135)/30,0,1)*np.clip(1-(ch-14)/14,0,1); tm=cv2.GaussianBlur(tm,(0,0),1.2)
    lab[...,0]-=teeth*0.15*(L-110).clip(0)*tm; lab[...,2]+=teeth*7.0*tm; lab[...,1]+=teeth*1.2*tm
    out=cv2.cvtColor(np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
    H,W=img.shape[:2]; db=cv2.warpAffine(out-c.astype(np.float32),cv2.invertAffineTransform(M),(W,H),flags=cv2.INTER_AREA)
    return np.clip(img.astype(np.float32)+db,0,255).astype(np.uint8),fm,tm
