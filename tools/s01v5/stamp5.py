# v5 stamp: lift STEADFAST MEN letters from LOCKED-stage-screen.jpg (never redrawn), place on plate screen, occlude behind Wes, dim ~78% + light blur
import cv2,numpy as np,sys,json,os
from rembg import remove,new_session
POS={'80-wes-work-room':(0.27,0.17,0.30),'81-wes-close-smile':(0.22,0.17,0.30),'72-wes-three-quarter-palms':(0.28,0.16,0.28),
     '73-wes-side-close':(0.72,0.17,0.20),'81-wes-close-smile@s':(0.735,0.13,0.14),'72-wes-three-quarter-palms@s':(0.535,0.10,0.13),'77-wes-medium-wide':(0.345,0.14,0.15)}
logo=cv2.imread('/workspace/steadfast/training-locked/LOCKED-stage-screen.jpg').astype(np.float32)
L=logo[20:240,80:655]; g=cv2.cvtColor(L,cv2.COLOR_BGR2GRAY)
bg=cv2.medianBlur(g.astype(np.uint8),41).astype(np.float32); a=np.clip((g-bg-12)/60,0,1)
sess=new_session('u2net_human_seg')
for n in sys.argv[1:]:
  b=n.split('@')[0]; orig=cv2.imread(f'/workspace/steadfast/training-locked/{b}.jpg')
  if os.path.exists(f'hr/{b}.png'):
    im=cv2.imread(f'hr/{b}.png').astype(np.float32); H,W=im.shape[:2]
    im=0.68*im+0.32*cv2.resize(orig,(W,H),interpolation=cv2.INTER_LANCZOS4)+np.random.default_rng(1).normal(0,1.6,im.shape)
  else:
    im=cv2.resize(orig,(orig.shape[1]*2,orig.shape[0]*2),interpolation=cv2.INTER_LANCZOS4).astype(np.float32); H,W=im.shape[:2]
  cx,cy,wf=POS[n]; lw=wf*W; lh=lw*L.shape[0]/L.shape[1]
  m=remove(cv2.resize(orig,(W//2,H//2)),session=sess,only_mask=True)
  m=cv2.resize(np.array(m),(W,H)).astype(np.float32)/255; m=cv2.GaussianBlur(cv2.dilate(m,np.ones((5,5))),(0,0),2)
  M=np.float32([[lw/L.shape[1],0,cx*W-lw/2],[0,lh/L.shape[0],cy*H-lh/2]])
  A=cv2.warpAffine(a,M,(W,H)); C=cv2.warpAffine(L,M,(W,H))
  occ=(A*m).sum()/A.sum(); print(n,'occluded frac',round(float(occ),3))
  y0,y1=int(cy*H-lh),int(cy*H+lh); x0,x1=int(cx*W-lw/2),int(cx*W+lw/2)
  lvl=np.median(im[max(0,y0):y1,max(0,x0):x1].reshape(-1,3),0); ref=np.median(L.reshape(-1,3),0)
  C=C*(max(lvl.mean(),20)/ref.mean())**0.5
  A=cv2.GaussianBlur(A,(0,0),W/2752*1.8)*0.78*(1-m)
  out=im*(1-A[...,None])+np.maximum(C,im)*A[...,None]
  out=np.clip(out,0,255).astype(np.uint8); cv2.imwrite(f'st/{n}.png',out)
  r=cv2.resize(out,(1934,1080),interpolation=cv2.INTER_AREA)[:,7:1927]; cv2.imwrite(f'up/{n}.jpg',r,[1,95])
