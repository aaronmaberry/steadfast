import cv2,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
c=cv2.VideoCapture('studio-proof-L01-60s-v1.mp4');s=[]
while True:
    ok,f=c.read()
    if not ok:break
    t=len(s)/24
    if t<7 or 25<t<27.2 or 33<t<36:
        r=app.get(f);s.append(float(max(r,key=lambda z:z.bbox[2]-z.bbox[0]).normed_embedding@M) if r else -1)
    else: s.append(np.nan)
s=np.array(s);old=np.load('final.scores.npy');m=~np.isnan(s);old[m]=s[m];np.save('final.scores.npy',old)
print([(round(i/24,2),round(old[i],3)) for i in range(len(old)) if 0<=old[i]<0.85])
for a,b,n in [(0.4,5.6,'X1a'),(25.6,26.7,'S3'),(33.8,35.0,'X1b')]:
    x=old[int(a*24):int(b*24)];print(n,'mean %.3f min %.3f'%(x.mean(),x.min()))
