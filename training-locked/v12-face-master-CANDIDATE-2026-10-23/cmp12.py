import cv2,numpy as np,sys
from insightface.app import FaceAnalysis
import detail12 as d
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection']);app.prepare(ctx_id=-1,det_size=(640,640))
def crop(p):
  im=cv2.imread(p);f=max(app.get(im),key=lambda f:f.bbox[2]-f.bbox[0]);M,_=cv2.estimateAffinePartial2D(f.kps.astype(np.float32),d.FF)
  return cv2.warpAffine(im,M,(512,512),flags=cv2.INTER_AREA if np.linalg.norm(M[0,:2])<1 else cv2.INTER_CUBIC)[70:260,130:382]
n=sys.argv[1]
V='/workspace/steadfast-main/training-locked/v10-face-master-STUDIO-2026-10-22/'+n
cv2.imwrite(sys.argv[2],cv2.resize(np.hstack([crop(V),crop('v12/'+n),crop('ref_Ben_Affleck_by_Gage_Skidmore_3.jpg')]),None,fx=1.25,fy=1.25))
