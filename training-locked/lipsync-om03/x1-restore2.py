import cv2,numpy as np,subprocess,sys
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition','landmark_2d_106']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('../../om3/v13ref/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
SX,SY,FE=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]);OUT=sys.argv[4]
A=cv2.VideoCapture('x1-win.mp4');B=cv2.VideoCapture('x1-sync3.mp4')
p=subprocess.Popen(f"ffmpeg -v error -y -f rawvideo -pix_fmt bgr24 -s 1280x720 -r 24 -i - -i line-thatcounts.wav -map 0:v -map 1:a -t 1.333 -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac {OUT}".split(),stdin=subprocess.PIPE)
sc=[];sh=[]
for i in range(32):
    _,a=A.read();_,b=B.read()
    la=max(app.get(a),key=lambda z:z.bbox[2]-z.bbox[0]).landmark_2d_106;lb=max(app.get(b),key=lambda z:z.bbox[2]-z.bbox[0]).landmark_2d_106
    mo=np.vstack([la[52:72],lb[52:72]]);c=mo.mean(0);r=mo.max(0)-mo.min(0)
    m=np.zeros((720,1280),np.float32)
    cv2.ellipse(m,(int(c[0]),int(c[1]+r[1]*0.35)),(int(r[0]*SX),int(r[1]*SY)),0,0,360,1,-1)
    m=cv2.GaussianBlur(m,(0,0),r[0]*FE)[...,None]
    sel=m[...,0]>0.5
    ga=cv2.cvtColor(a,6).astype(np.float32);bf=b.astype(np.float32)
    ra=(ga-cv2.GaussianBlur(ga,(0,0),1.0))[sel].std()
    best=bf
    for k in np.arange(0,2.01,0.1):
        t=bf+k*(bf-cv2.GaussianBlur(bf,(0,0),1.0));g=cv2.cvtColor(np.clip(t,0,255).astype(np.uint8),6).astype(np.float32)
        best=t
        if (g-cv2.GaussianBlur(g,(0,0),1.0))[sel].std()>=ra: break
    o=np.clip(best*m+a*(1-m),0,255).astype(np.uint8)
    f=max(app.get(o),key=lambda z:z.bbox[2]-z.bbox[0]);sc.append(float(f.normed_embedding@M))
    x0,y0,x1,y1=f.bbox.astype(int);sh.append(cv2.Laplacian(cv2.cvtColor(o[y0:y1,x0:x1],6),cv2.CV_64F).var())
    p.stdin.write(o.tobytes())
p.stdin.close();p.wait();sc=np.array(sc)
print(OUT,'arc mean %.3f min %.3f nbelow %d sharp %.0f'%(sc.mean(),sc.min(),(sc<0.85).sum(),np.mean(sh)))
