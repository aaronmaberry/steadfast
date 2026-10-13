import cv2,numpy as np,sys,json,os
from rembg import remove,new_session
S=json.load(open('screens.json'))
logo=cv2.imread('/workspace/steadfast/training-locked/LOCKED-stage-screen.jpg').astype(np.float32)
L=logo[20:240,80:655]
g=cv2.cvtColor(L,cv2.COLOR_BGR2GRAY)
bg=cv2.medianBlur(g.astype(np.uint8),41).astype(np.float32)
a=np.clip((g-bg-12)/60,0,1)            # letter alpha from stamp
col=L  # original letter colors
sess=new_session('u2net_human_seg')
for n in sys.argv[1:]:
  src=f'hr/{n}.png' if os.path.exists(f'hr/{n}.png') else f'/workspace/s01v2/raw/{n}.png'
  im=cv2.imread(src).astype(np.float32);H,W=im.shape[:2]
  if src.startswith('hr/'):
    r=cv2.resize(cv2.imread(f'/workspace/s01v2/raw/{n}.png'),(W,H),interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    im=0.68*im+0.32*r+np.random.default_rng(1).normal(0,1.6,im.shape).astype(np.float32)
  x0,x1,y0,y1,sc,yc=S[n]
  sw=(x1-x0)*W; lw=min(sc*sw,0.5*W); lh=lw*L.shape[0]/L.shape[1]
  cx=(x0+x1)/2*W; cy=max(y0*H+yc*(y1-y0)*H, lh/2+0.03*H)
  CX=json.load(open('/workspace/s01v2/cx.json'))[n]
  ch=H*CX.get('h',0.8);cw=ch*16/9;cy0=H*CX.get('y',0.02);cx0=max(0,min(W-cw,W*CX['x']-cw/2))
  ux0=max(x0*W,cx0+0.03*W);ux1=min(x1*W,cx0+cw-0.03*W)
  lw=min(lw,0.36*cw,0.92*(ux1-ux0)); lh=lw*L.shape[0]/L.shape[1]
  cy=max(y0*H+yc*(y1-y0)*H,cy0+lh/2+0.06*H)
  small=cv2.resize(im.astype(np.uint8),(W//2,H//2))
  m=remove(small,session=sess,only_mask=True)
  m=cv2.resize(np.array(m),(W,H)).astype(np.float32)/255
  m=cv2.GaussianBlur(cv2.dilate(m,np.ones((5,5))),(0,0),2)
  lo=ux0+lw/2; hi=ux1-lw/2
  best=None
  for c in (np.linspace(lo,hi,25) if hi>lo else [cx]):
    M=np.float32([[lw/L.shape[1],0,c-lw/2],[0,lh/L.shape[0],cy-lh/2]])
    A=cv2.warpAffine(a,M,(W,H)); occ=(A*m).sum()/A.sum()+abs(c-cx)/W*0.3
    if best is None or occ<best[0]: best=(occ,M)
  M=best[1]
  A=cv2.warpAffine(a,M,(W,H)); C=cv2.warpAffine(col,M,(W,H))
  # match screen brightness: scale letter color relative to local screen level
  lvl=np.median(im[int(y0*H):int(y1*H),int(x0*W):int(x1*W)].reshape(-1,3),0)
  ref=np.median(L.reshape(-1,3),0)
  C=C*(lvl.mean()/ref.mean())**0.5*1.0
  A=cv2.GaussianBlur(A,(0,0),W/2752*1.6)
  A=A*(1-m)
  out=im*(1-A[...,None])+np.maximum(C,im)*A[...,None]
  os.makedirs('st',exist_ok=True)
  out=np.clip(out,0,255).astype(np.uint8)
  cv2.imwrite(f'st/{n}.png',out)
  os.makedirs('up',exist_ok=True)
  cr=out[int(cy0):int(cy0+ch),int(cx0):int(cx0+cw)]
  cv2.imwrite(f'up/{n}.jpg',cv2.resize(cr,(1920,1080),interpolation=cv2.INTER_AREA),[1,95]); print(n,src,flush=True)
