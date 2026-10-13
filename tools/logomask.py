import cv2,numpy as np,json,sys
CXA=json.load(open('/workspace/s01v2/cx.json'))
for n in sys.argv[1:]:
  st=cv2.imread(f'/workspace/s01v3/st/{n}.png').astype(np.float32);H,W=st.shape[:2]
  im=cv2.imread(f'/workspace/s01v3/hr/{n}.png').astype(np.float32)
  r=cv2.resize(cv2.imread(f'/workspace/s01v2/raw/{n}.png'),(W,H),interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
  im=0.68*im+0.32*r+np.random.default_rng(1).normal(0,1.6,im.shape).astype(np.float32)
  d=np.clip((st-np.clip(im,0,255)).max(2)/40,0,1)
  CX=CXA[n];ch=H*CX.get('h',0.8);cw=ch*16/9;cy0=H*CX.get('y',0.02);cx0=max(0,min(W-cw,W*CX['x']-cw/2))
  m=cv2.resize(d[int(cy0):int(cy0+ch),int(cx0):int(cx0+cw)],(1920,1080),interpolation=cv2.INTER_AREA)
  cv2.imwrite(f'mask/{n}.png',(m*255).astype(np.uint8)); print(n,m.max(),(m>0.2).sum())
