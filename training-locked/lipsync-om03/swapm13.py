import cv2,numpy as np,insightface,subprocess
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition','landmark_2d_106']);app.prepare(ctx_id=-1,det_size=(640,640))
sw=insightface.model_zoo.get_model('/workspace/tools/swap-models/inswapper_128.onnx',providers=['CPUExecutionProvider'])
D='v13ref/'
src=max(app.get(cv2.imread(D+'M1-front-0019.png')),key=lambda f:f.bbox[2])
M=np.load(D+'mean_arcface_embedding.npy').astype(np.float32);Mn=M/np.linalg.norm(M);src.embedding=Mn*np.linalg.norm(src.embedding)
cap=cv2.VideoCapture('om3-raw.mp4');W,H=int(cap.get(3)),int(cap.get(4))
p=subprocess.Popen(f"ffmpeg -v error -y -f rawvideo -pix_fmt bgr24 -s {W}x{H} -r 25 -i - -i om3-raw.mp4 -map 0:v -map 1:a -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac om3-v13m.mp4".split(),stdin=subprocess.PIPE)
log=open('swapm13.log','w');i=0;tl=[]
while True:
    ok,f=cap.read()
    if not ok:break
    fs=app.get(f)
    if fs:
        t=max(fs,key=lambda z:z.bbox[2]-z.bbox[0]);L=t.landmark_2d_106;g=f
        for k in range(4):
            g=sw.get(g,t,src,paste_back=True); t2=app.get(g)
            if not t2: break
            t=max(t2,key=lambda z:z.bbox[2]-z.bbox[0])
            if k>=1 and t.normed_embedding@Mn>=0.88: break
        mo=L[52:72];c=mo.mean(0);r=mo.max(0)-mo.min(0)
        m=np.ones((H,W),np.float32)
        cv2.ellipse(m,(int(c[0]),int(c[1])),(int(r[0]*0.62+4),int(r[1]*0.62+4)),0,0,360,0,-1)
        m=cv2.GaussianBlur(m,(0,0),max(3,r[0]*0.08))[...,None]
        out=np.clip(g*m+f*(1-m),0,255)
        # gentle teeth: only very bright low-chroma pixels inside mouth, -6% L, slight warm; never below L 175
        lab=cv2.cvtColor(out.astype(np.uint8),cv2.COLOR_BGR2LAB).astype(np.float32)
        tm=np.zeros((H,W),np.uint8);cv2.fillConvexPoly(tm,cv2.convexHull(mo.astype(np.int32)),1)
        ch=np.hypot(lab[...,1]-128,lab[...,2]-128);t_=(tm>0)&(lab[...,0]>200)&(ch<20)
        tf=cv2.GaussianBlur(t_.astype(np.float32),(0,0),1.0)
        lab[...,0]=np.maximum(lab[...,0]*(1-0.06*tf),np.minimum(lab[...,0],175));lab[...,2]+=3*tf
        f=cv2.cvtColor(np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR);tl.append(int(t_.sum()))
    p.stdin.write(f.tobytes());i+=1
p.stdin.close();p.wait();print('frames',i,'teeth px mean',np.mean(tl),file=log)
