# v12: detail12.enhance on the hq.fix w0.8 v10-swap frames (T03frames_w08). Smoother, coherent texture; teeth to off-white.
import sys,os,cv2,numpy as np
sys.path.insert(0,'work'); import detail12 as detail
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection']);app.prepare(ctx_id=-1,det_size=(640,640))
KW=dict(amt=1.0,teeth=float(os.environ.get('TEETH',1.8)),pore=float(os.environ.get('PORE',0.6)),crease=float(os.environ.get('CREASE',1.6)),tonal=float(os.environ.get('TONAL',0.7)))
fr=[int(x) for x in os.environ['FRAMES'].split(',')] if os.environ.get('FRAMES') else range(132)
od=os.environ.get('OD','work/T03frames_v12');os.makedirs(od,exist_ok=True)
for i in fr:
  im=cv2.imread(f'work/T03frames_w08/{i:05d}.png'); fs=app.get(im)
  if fs: im,_,_=detail.enhance(im,max(fs,key=lambda f:f.bbox[2]-f.bbox[0]).kps,**KW)
  cv2.imwrite(f'{od}/{i:05d}.png',im)
