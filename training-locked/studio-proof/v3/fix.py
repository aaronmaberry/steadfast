import cv2,numpy as np,subprocess,sys,json
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition']);app.prepare(ctx_id=-1,det_size=(640,640))
M=np.load('/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy');M=M/np.linalg.norm(M)
sc=lambda o:float(max(app.get(o),key=lambda z:z.bbox[2]-z.bbox[0]).normed_embedding@M)
for pid in sys.argv[1:]:
    S=json.load(open(pid+'-rest.json'))['s']
    A=cv2.VideoCapture(pid+'-raw.mp4');B=cv2.VideoCapture(pid+'-rest.mp4');F=[];W=[]
    p=subprocess.Popen(f"ffmpeg -v error -y -f rawvideo -pix_fmt bgr24 -s 1280x720 -r 24 -i - -c:v libx264 -crf 12 -pix_fmt yuv420p {pid}-fix.mp4".split(),stdin=subprocess.PIPE)
    for i,s in enumerate(S):
        _,a=A.read();_,b=B.read();w=1.0;o=b
        if s<0.86:
            for w in (0.75,0.5,0.25,0.0):
                o=np.clip(a+w*(b.astype(np.float32)-a),0,255).astype(np.uint8)
                if sc(o)>=0.86: break
        W.append(w);p.stdin.write(o.tobytes())
    p.stdin.close();p.wait();json.dump(W,open(pid+'-fixw.json','w'))
    print(pid,'reduced',sum(x<1 for x in W),'zero',sum(x==0 for x in W),flush=True)
