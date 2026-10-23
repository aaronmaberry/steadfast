# v11 fix of vswap_chunk.py: same hq.fix (inswapper -> CodeFormer w, v10 mean latent), then detail.enhance:
# forehead high-frequency pass (source-plate forehead HF + face-locked pore/line texture) and teeth one step down. Low-mem, frames [a,b) -> PNGs
import sys,os,json
import onnxruntime as ort
_IS=ort.InferenceSession
class _LM(_IS):
    def __init__(self,*a,**k):
        so=ort.SessionOptions();so.enable_cpu_mem_arena=False;so.intra_op_num_threads=2;so.inter_op_num_threads=1
        k['sess_options']=so;super().__init__(*a,**k)
ort.InferenceSession=_LM
# Face master: v13 (LOCKED 2026-10-23) by default; pass --master v10 (or set MASTER_MEAN) for the historical v10 master.
_MASTERS={'v13':'/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy',
          'v10':'/workspace/steadfast-main/training-locked/v10-face-master-STUDIO-2026-10-22/mean_arcface_embedding.npy'}
_m='v13'
if '--master' in sys.argv:
    _i=sys.argv.index('--master'); _m=sys.argv[_i+1]; del sys.argv[_i:_i+2]
if _m!='v13' or not os.environ.get('MASTER_MEAN'): os.environ['MASTER_MEAN']=_MASTERS.get(_m,_m)
import cv2,numpy as np
sys.path.insert(0,'work'); import hq,detail
M=np.load(os.environ['MASTER_MEAN']).ravel();M/=np.linalg.norm(M)
src,od,a,b,w=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
amt=float(os.environ.get('FH_AMT',1.2)); th=float(os.environ.get('TEETH',1.25))
os.makedirs(od,exist_ok=True)
cap=cv2.VideoCapture(src); ok,f0=cap.read(); g=hq.noise_level(f0)*0.5
cap.set(cv2.CAP_PROP_POS_FRAMES,a); sc={}
for i in range(a,b):
  ok,fr=cap.read()
  if not ok: break
  o,done=hq.fix(fr,True,w,grain=g)
  f=hq.big(o)
  if f is not None: o,_,_=detail.enhance(o,f.kps,amt=amt,teeth=th,src=fr); f=hq.big(o)
  sc[i]=float(f.normed_embedding@M) if f is not None else None
  cv2.imwrite(f'{od}/{i:05d}.png',o)
json.dump(sc,open(f'{od}/sc_{a:05d}.json','w')); print(a,b,min(v for v in sc.values() if v is not None),flush=True)
