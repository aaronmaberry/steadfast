import sys,cv2,numpy as np
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/artifacts/training/w01-poc/poc4/lipsync-test/om3/v13ref/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
c=cv2.VideoCapture(sys.argv[1]);s=[]
while True:
    ok,f=c.read()
    if not ok:break
    r=app.get(f);s.append(float(max(r,key=lambda z:z.bbox[2]-z.bbox[0]).normed_embedding@M) if r else 0)
s=np.array(s);np.save(sys.argv[1]+'.scores.npy',s)
print(sys.argv[1],'n',len(s),'mean %.3f min %.3f at %.2fs'%(s.mean(),s.min(),s.argmin()/25),'below',[(round(i/25,2),round(s[i],3)) for i in np.where(s<0.85)[0]])
