import numpy as np,cv2
from PIL import Image
R=np.array(Image.open('bg/room69_clean.png').convert('RGB')).astype(np.float32)
H,W=R.shape[:2]
L=R.mean(2)
# letters: bright pixels inside logo box (plus underline), dilated
lb=[540,221,1170,464]
let=np.zeros((H,W),np.uint8)
x0,y0,x1,y1=600-80,180,2500,720
bgL=cv2.medianBlur(L.astype(np.uint8),51).astype(np.float32); sub=(L-bgL)[y0:y1,x0:x1]; let[y0:y1,x0:x1]=(sub>14).astype(np.uint8)
let=cv2.dilate(let,np.ones((7,7),np.uint8)); prot=np.zeros((H,W),np.float32); prot[230:670,560:2440]=1; letf=np.maximum(prot,cv2.GaussianBlur(cv2.dilate(prot,np.ones((61,61),np.uint8)),(0,0),25))
# region to clean: upper-left screen area
reg=np.zeros((H,W),np.float32); reg[20:560,0:1900]=1
reg=cv2.GaussianBlur(reg,(0,0),60)
m=np.clip(reg*(1-letf),0,1)[...,None]
# clean sky: large blur, then match chroma to neutral blue-grey sky (kill brown cast)
k=(1-prot)[...,None]; bl=cv2.GaussianBlur(R*k,(0,0),28)/np.maximum(cv2.GaussianBlur(k[...,0],(0,0),28)[...,None],1e-3)
g=bl.mean(2,keepdims=True); ref=np.array([0.92,0.98,1.12],np.float32)  # cool tint like rest of sky
bl=0.5*bl+0.5*g*ref
rng=np.random.default_rng(1); grain=cv2.GaussianBlur(rng.normal(0,2.2,(H,W)).astype(np.float32),(0,0),0.8)[...,None]
O=R*(1-m)+(bl+grain)*m
O=np.clip(O,0,255).astype(np.uint8)
# guarantee letter pixels identical
O[prot>0]=R.astype(np.uint8)[prot>0]
Image.fromarray(O).save('v7/bg/room69_clean_v7.png')
d=np.abs(O.astype(int)-R.astype(int)).max(2); print('letter px changed:',int((d[let>0]>0).sum()), 'of', int(let.sum()))
Image.fromarray(O[0:700,0:1500]).save('v7/qa/bg7_ul.png')
