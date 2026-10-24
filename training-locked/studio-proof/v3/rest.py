import cv2,numpy as np,subprocess,sys,json
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition','landmark_2d_106']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
SX,SY,FE=0.85,1.6,0.12
for pid in sys.argv[1:]:
    A=cv2.VideoCapture(pid+'-raw.mp4');B=cv2.VideoCapture(pid+'-s3.mp4')
    p=subprocess.Popen(f"ffmpeg -v error -y -f rawvideo -pix_fmt bgr24 -s 1280x720 -r 24 -i - -c:v libx264 -crf 12 -pix_fmt yuv420p {pid}-rest.mp4".split(),stdin=subprocess.PIPE)
    sc=[];shr=[];shs=[];sho=[]
    big=lambda r:max(r,key=lambda z:z.bbox[2]-z.bbox[0])
    while True:
        ok,a=A.read();ok2,b=B.read()
        if not(ok and ok2):break
        fa=big(app.get(a));fb=big(app.get(b));la,lb=fa.landmark_2d_106,fb.landmark_2d_106
        mo=np.vstack([la[52:72],lb[52:72]]);c=mo.mean(0);r=mo.max(0)-mo.min(0)
        m=np.zeros((720,1280),np.float32)
        cv2.ellipse(m,(int(c[0]),int(c[1]+r[1]*0.35)),(int(r[0]*SX),int(r[1]*SY)),0,0,360,1,-1)
        m=cv2.GaussianBlur(m,(0,0),r[0]*FE)[...,None];sel=m[...,0]>0.5
        ga=cv2.cvtColor(a,6).astype(np.float32);bf=b.astype(np.float32)
        ra=(ga-cv2.GaussianBlur(ga,(0,0),1.0))[sel].std()
        for k in np.arange(0,2.01,0.1):
            t=bf+k*(bf-cv2.GaussianBlur(bf,(0,0),1.0));g=cv2.cvtColor(np.clip(t,0,255).astype(np.uint8),6).astype(np.float32)
            if (g-cv2.GaussianBlur(g,(0,0),1.0))[sel].std()>=ra: break
        o=np.clip(t*m+a*(1-m),0,255).astype(np.uint8)
        f=big(app.get(o));sc.append(float(f.normed_embedding@M))
        x0,y0,x1,y1=np.clip(f.bbox.astype(int),0,None)
        L=lambda im:cv2.Laplacian(cv2.cvtColor(im[y0:y1,x0:x1],6),cv2.CV_64F).var()
        shr.append(L(a));shs.append(L(b));sho.append(L(o))
        p.stdin.write(o.tobytes())
    p.stdin.close();p.wait();sc=np.array(sc)
    json.dump(dict(s=sc.tolist(),sharp=[np.mean(shr),np.mean(shs),np.mean(sho)]),open(pid+'-rest.json','w'))
    print(pid,'n%d arc mean %.3f min %.3f nbelow %d sharp raw/s3/rest %.0f/%.0f/%.0f'%(len(sc),sc.mean(),sc.min(),(sc<0.85).sum(),np.mean(shr),np.mean(shs),np.mean(sho)),flush=True)
