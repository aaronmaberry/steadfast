import cv2,numpy as np,sys,json
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition','landmark_2d_106']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
a,b=int(sys.argv[1]),int(sys.argv[2]);c=cv2.VideoCapture('studio-proof-L01-60s-v2.mp4');c.set(cv2.CAP_PROP_POS_FRAMES,a);R=[]
for n in range(a,b):
    ok,f=c.read()
    if not ok:break
    r=app.get(f)
    if not r: R.append(None);continue
    t=n/24
    if t<35.3: r=[z for z in r if (z.bbox[0]+z.bbox[2])/2>880 and (z.bbox[1]+z.bbox[3])/2>300]
    elif t<52.4: r=[z for z in r if (z.bbox[0]+z.bbox[2])/2<640]
    if not r: R.append(None);continue
    z=max(r,key=lambda z:z.bbox[2]-z.bbox[0]);L=z.landmark_2d_106
    R.append(dict(n=n,s=float(z.normed_embedding@M),mo=float(np.linalg.norm(L[71]-L[53])/(z.bbox[3]-z.bbox[1]))))
json.dump(R,open(f'f{a}.json','w'))
