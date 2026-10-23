import sys,os,cv2,numpy as np,json,subprocess
# Face master: v13 (LOCKED 2026-10-23) by default; pass --master v10 (or set MASTER_MEAN) for the historical v10 master.
_MASTERS={'v13':'/workspace/steadfast-main/training-locked/v13-face-master-LOCKED-2026-10-23/mean_arcface_embedding.npy',
          'v10':'/workspace/steadfast-main/training-locked/v10-face-master-STUDIO-2026-10-22/mean_arcface_embedding.npy'}
_m='v13'
if '--master' in sys.argv:
    _i=sys.argv.index('--master'); _m=sys.argv[_i+1]; del sys.argv[_i:_i+2]
if _m!='v13' or not os.environ.get('MASTER_MEAN'): os.environ['MASTER_MEAN']=_MASTERS.get(_m,_m)
sys.path.insert(0,'work'); import hq
M=np.load(os.environ['MASTER_MEAN']).ravel();M/=np.linalg.norm(M)
src,dst=sys.argv[1],sys.argv[2]
cap=cv2.VideoCapture(src);fps=cap.get(5);W=int(cap.get(3));H=int(cap.get(4))
p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-i',src,'-map','0:v','-map','1:a?','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','copy',dst],stdin=subprocess.PIPE)
sc=[];g=None;miss=0
while True:
  ok,fr=cap.read()
  if not ok: break
  if g is None: g=hq.noise_level(fr)*0.5
  o,done=hq.fix(fr,True,0.8,grain=g)
  f=hq.big(o)
  sc.append(float(f.normed_embedding@M) if f is not None else None)
  if f is None: miss+=1
  p.stdin.write(o.tobytes())
p.stdin.close();p.wait()
v=[s for s in sc if s is not None]
r={"clip":os.path.basename(dst),"frames":len(sc),"noface":miss,"mean":round(np.mean(v),3),"min":round(min(v),3),"below085":sum(s<0.85 for s in v)}
json.dump({"summary":r,"per_frame":sc},open(dst+'.scores.json','w'));print(json.dumps(r),flush=True)
