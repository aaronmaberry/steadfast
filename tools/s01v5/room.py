import cv2,numpy as np
from rembg import remove,new_session
im=cv2.imread('/workspace/steadfast/training-locked/69-wes-screen-lock-plate.jpg'); im=cv2.resize(im,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
m=np.array(remove(im,session=new_session('u2net_human_seg'),only_mask=True))
m=(cv2.dilate((m>40).astype(np.uint8),np.ones((31,31)))*255)
cv2.imwrite('hi_m69.png',m)
small=cv2.resize(im,(480,270)); ms=cv2.resize(m,(480,270))
f=cv2.inpaint(small,(ms>0).astype(np.uint8),15,cv2.INPAINT_TELEA); f=cv2.resize(f,(1920,1080),interpolation=cv2.INTER_CUBIC)
f=f.astype(np.float32)+np.random.default_rng(2).normal(0,2.0,f.shape)
a=cv2.GaussianBlur(m.astype(np.float32)/255,(0,0),6)[...,None]
out=im*(1-a)+f*a; cv2.imwrite('room69.png',np.clip(out,0,255).astype(np.uint8))
