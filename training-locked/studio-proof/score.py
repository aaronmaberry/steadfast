import cv2,numpy as np,json
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
c=cv2.VideoCapture('studio-proof-L01-60s-v1.mp4');s=[];i=0
while True:
    ok,f=c.read()
    if not ok:break
    r=app.get(f);s.append(float(max(r,key=lambda z:z.bbox[2]-z.bbox[0]).normed_embedding@M) if r else -1);i+=1
s=np.array(s);np.save('final.scores.npy',s)
def rep(a,b,name):
    x=s[int(a*24):int(b*24)];f=x[x>=0]
    print(name,a,b,'n',len(x),'face',len(f),'mean %.3f min %.3f'%(f.mean(),f.min()) if len(f) else '', 'below0.85',int((f<0.85).sum()))
for a,b,n in [(0.3,6.6,'X1 0-6.9'),(25.6,26.7,'S3'),(33.8,35.0,'X1 8.25-'),(42.3,46.9,'OM03'),(7,25,'pend W02'),(55,62.5,'pend full')]: rep(a,b,n)
