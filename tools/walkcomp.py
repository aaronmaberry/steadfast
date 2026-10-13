import cv2,numpy as np
bg0=cv2.imread('hi/r69L.png'); H0,W0=bg0.shape[:2]
src=bg0[600:,1100-(W0-1100)*2:1100-(W0-1100)][:, ::-1]  # mirrored dark stage from left of the ghost region
src=cv2.resize(src,(W0-1100,H0-600))
fm=np.zeros((H0,W0),np.float32); fm[600:,1100:]=1; fm=cv2.GaussianBlur(fm,(0,0),25)[...,None]
fm[600:,1180:]=1
fill=bg0.astype(np.float32).copy(); fill[600:,1100:]=src
bg0=(bg0*(1-fm)+fill*fm).astype(np.uint8); cv2.imwrite('hi/room_clean.png',bg0); s=0.8; bg0=cv2.resize(bg0,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
bh,bw=bg0.shape[:2]
# measure Wes centroid per frame (smoothed) -> camera tracks him, room drifts opposite
cx=[]
for i in range(1,203):
  m=cv2.imread('wm/%04d.png'%i,0); ys,xs=np.where(m>128); cx.append(xs.mean())
cx=np.convolve(np.pad(cx,12,mode='edge'),np.ones(25)/25,'valid')
rng=np.random.default_rng(3)
for i in range(1,203):
  f=cv2.imread('wf/%04d.png'%i).astype(np.float32); f=cv2.resize(f,(1920,1080))
  m=cv2.imread('wm/%04d.png'%i,0); m=cv2.resize(m,(1920,1080))
  n,lab,st,_=cv2.connectedComponentsWithStats((m>60).astype(np.uint8)); k=1+np.argmax(st[1:,4]); m=np.where(cv2.dilate((lab==k).astype(np.uint8),np.ones((15,15)))>0,m,0).astype(np.uint8); m=cv2.erode(m,np.ones((3,3)));a=cv2.GaussianBlur(m,(0,0),1.6).astype(np.float32)/255
  # shift Wes so his centroid sits at x=1070 (right of panel centre)
  dx=1070-cx[i-1]*1920/1890; M=np.float32([[1,0,dx],[0,1,0]])
  f=cv2.warpAffine(f,M,(1920,1080),borderMode=cv2.BORDER_REPLICATE); a=cv2.warpAffine(a,M,(1920,1080))
  pan=(cx[i-1]-cx[0])*0.35
  x0=int(np.clip(150+pan,0,bw-960)); y0=40
  canvas=np.zeros((1080,1920,3),np.float32); canvas[:,480:1440]=bg0[y0:y0+1080,x0:x0+960]
  canvas=cv2.GaussianBlur(canvas,(0,0),1.2)  # shallow depth of field behind him
  # match Wes to room: slight cool/dim
  out=canvas*(1-a[...,None])+f*0.97*a[...,None]
  cv2.imwrite('/workspace/s01v3/clips/walk46c_f/%05d.png'%i,np.clip(out,0,255).astype(np.uint8))
print('ok',cx[0],cx[-1])
