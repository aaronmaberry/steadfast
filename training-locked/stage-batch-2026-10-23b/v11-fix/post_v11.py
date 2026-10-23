# fast path: apply detail.enhance to the existing hq.fix w0.8 frames (identical swap output), source HF from trim plate
import sys,os,cv2,numpy as np
sys.path.insert(0,'work'); import detail
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection']);app.prepare(ctx_id=-1,det_size=(640,640))
cap=cv2.VideoCapture('trim/T03-talk-P03-trim0-5.5.mp4');os.makedirs('work/T03frames_v11',exist_ok=True)
for i in range(132):
  ok,src=cap.read(); im=cv2.imread(f'work/T03frames_w08/{i:05d}.png'); fs=app.get(im)
  if fs: im,_,_=detail.enhance(im,max(fs,key=lambda f:f.bbox[2]-f.bbox[0]).kps,amt=float(os.environ.get("FH_AMT",1.2)),teeth=1.25,src=src)
  cv2.imwrite(f'work/T03frames_v11/{i:05d}.png',im)
