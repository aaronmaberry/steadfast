import cv2,numpy as np,json,os,glob
from insightface.app import FaceAnalysis
import detail12 as detail
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition']);app.prepare(ctx_id=-1,det_size=(640,640))
V10='/workspace/steadfast-main/training-locked/v10-face-master-STUDIO-2026-10-22'; OD='/workspace/scratch/v12'; os.makedirs(OD,exist_ok=True)
M=np.load(V10+'/mean_arcface_embedding.npy').ravel();M/=np.linalg.norm(M)
big=lambda im:max(app.get(im),key=lambda f:f.bbox[2]-f.bbox[0])
embs=[];rows=[]
for p in sorted(glob.glob(V10+'/M*.png')):
  im=cv2.imread(p);f=big(im)
  o,fm,tm=detail.enhance(im,f.kps,amt=1.0,teeth=1.0,crease=2.2,pore=1.2)
  n=os.path.basename(p);cv2.imwrite(f'{OD}/{n}',o)
  g=big(o);e=g.normed_embedding;embs.append(e)
  rows.append(dict(file=n,cos_v11_vs_v10mean=round(float(e@M),4),cos_v11_vs_v10frame=round(float(e@f.normed_embedding),4),cos_v10frame_vs_v10mean=round(float(f.normed_embedding@M),4)))
  print(rows[-1],flush=True)
mm=np.mean(embs,0);mm/=np.linalg.norm(mm);np.save(OD+'/mean_arcface_embedding.npy',mm.astype(np.float32))
print('v11mean vs v10mean',float(mm@M))
json.dump(dict(frames=rows,v11mean_vs_v10mean=round(float(mm@M),4)),open(OD+'/v12-scores.json','w'),indent=1)
