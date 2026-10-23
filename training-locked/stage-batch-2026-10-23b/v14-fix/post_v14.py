# v14 (teeth only, no forehead overlay): detail12.enhance on the hq.fix w0.8 v10-swap frames (T03frames_w08). Smoother, coherent texture; teeth to off-white.
import sys,os,cv2,numpy as np
sys.path.insert(0,'work'); import detail13 as detail; detail.set_ref(np.load("work/ref_forehead_L512.npy"))
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection']);app.prepare(ctx_id=-1,det_size=(640,640))
KW=dict(brow=float(os.environ.get('BROW',1.2)),spec=float(os.environ.get('SPEC',0.8)),refw=float(os.environ.get('REFW',0.5)),teeth=float(os.environ.get('TEETH',1.8)),pore=float(os.environ.get('PORE',0.5)),crease=float(os.environ.get('CREASE',1.8)),tonal=float(os.environ.get('TONAL',0.6)))
fr=[int(x) for x in os.environ['FRAMES'].split(',')] if os.environ.get('FRAMES') else range(132)
od=os.environ.get('OD','work/T03frames_v14');os.makedirs(od,exist_ok=True)
for i in fr:
  im=cv2.imread(f'work/T03frames_w08/{i:05d}.png'); fs=app.get(im)
  if fs:
    kp=max(fs,key=lambda f:f.bbox[2]-f.bbox[0]).kps; o,_,_=detail.enhance(im,kp,**KW)
    # keep ONLY the mouth region change (no forehead/face change at all; avoids Lab round-trip drift elsewhere)
    m=np.zeros(im.shape[:2],np.float32); c=kp[3:5].mean(0); r=np.linalg.norm(kp[3]-kp[4])
    cv2.ellipse(m,(int(c[0]),int(c[1])),(int(r*0.9),int(r*0.6)),0,0,360,1,-1); m=cv2.GaussianBlur(m,(0,0),2)[...,None]
    im=np.clip(o*m+im*(1-m),0,255).astype(np.uint8)
  cv2.imwrite(f'{od}/{i:05d}.png',im)
