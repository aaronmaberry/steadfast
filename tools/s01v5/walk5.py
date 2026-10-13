# walk: matte Wes from HeyGen lip-sync render (plate 89) and composite onto locked plate-69 room (Wes 69 removed, logo intact); Wes travels left, camera half-follows
import cv2,numpy as np,os,sys
from rembg import remove,new_session
src=sys.argv[1]; dst=sys.argv[2]; os.makedirs(dst,exist_ok=True)
s=new_session('u2net_human_seg'); files=sorted(os.listdir(src)); N=len(files)
room=cv2.imread('room69.png').astype(np.float32); RW,RH=2112,1188; room=cv2.resize(room,(RW,RH),interpolation=cv2.INTER_CUBIC)
room=cv2.GaussianBlur(room,(0,0),1.0)
ease=lambda x:0.5-0.5*np.cos(np.pi*np.clip(x,0,1))
for i,f in enumerate(files):
    t=i/25; p=i/max(1,N-1)
    im=cv2.imread(f'{src}/{f}')
    m=np.array(remove(cv2.resize(im,(960,540)),session=s,only_mask=True)); m=cv2.resize(m,(1920,1080),interpolation=cv2.INTER_CUBIC)
    n,lab,st,_=cv2.connectedComponentsWithStats((m>60).astype(np.uint8)); k=1+np.argmax(st[1:,4])
    m=np.where(cv2.dilate((lab==k).astype(np.uint8),np.ones((15,15)))>0,m,0).astype(np.uint8); m=cv2.erode(m,np.ones((3,3)))
    a=cv2.GaussianBlur(m,(0,0),1.4).astype(np.float32)/255
    wx=190-260*ease(p)          # Wes travel in frame (px): right -> left, toward the screen he faces
    bob=4*np.sin(2*np.pi*1.6*t)
    sc=1.0+0.035*ease(p)
    M=np.float32([[sc,0,wx+(1-sc)*960],[0,sc,bob+(1-sc)*1080]])
    fw=cv2.warpAffine(im.astype(np.float32),M,(1920,1080),borderMode=cv2.BORDER_REPLICATE); aw=cv2.warpAffine(a,M,(1920,1080))
    pan=96-60*ease(p)           # camera half-follows: room drifts the other way
    bg=room[54:54+1080,int(pan):int(pan)+1920]
    # light wrap: soften matte edge with room colour
    edge=np.clip(aw*(1-aw)*4,0,1)[...,None]
    out=bg*(1-aw[...,None])+fw*0.96*aw[...,None]; out=out*(1-0.25*edge)+cv2.GaussianBlur(bg,(0,0),6)*0.25*edge
    cv2.imwrite(f'{dst}/%05d.png'%(i+1),np.clip(out,0,255).astype(np.uint8))
    if i%100==0: print(i,flush=True)
