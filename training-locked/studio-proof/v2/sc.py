import cv2,numpy as np,sys,json
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition','landmark_2d_106']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
for t in sys.argv[1:]:
    c=cv2.VideoCapture(t+'.mp4');R=[]
    while True:
        ok,f=c.read()
        if not ok:break
        r=app.get(f)
        if not r: R.append(None);continue
        z=max(r,key=lambda z:z.bbox[2]-z.bbox[0]);L=z.landmark_2d_106
        # inner lips: use 106 idx 52-71 mouth; opening = dist upper/lower inner lip
        mo=float(np.linalg.norm(L[71]-L[53])/(z.bbox[3]-z.bbox[1]))
        R.append(dict(s=float(z.normed_embedding@M),b=[float(x) for x in z.bbox],mo=mo))
    json.dump(R,open(t+'.sc.json','w'));s=[x['s'] for x in R if x]
    print(t,len(R),'noface',sum(x is None for x in R),'mean %.3f min %.3f <.85: %d'%(np.mean(s),np.min(s),sum(v<.85 for v in s)),flush=True)
