import cv2,numpy as np
from insightface.app import FaceAnalysis
import detail13 as d
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection']);app.prepare(ctx_id=-1,det_size=(640,640))
im=cv2.imread('ref_Ben_Affleck_by_Gage_Skidmore_3.jpg');f=max(app.get(im),key=lambda f:f.bbox[2]-f.bbox[0])
M,_=cv2.estimateAffinePartial2D(f.kps.astype(np.float32),d.FF);c=cv2.warpAffine(im,M,(512,512),flags=cv2.INTER_AREA)
np.save('ref_forehead_L512.npy',cv2.cvtColor(c,cv2.COLOR_BGR2LAB)[...,0])
