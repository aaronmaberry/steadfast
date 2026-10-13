import cv2,numpy as np,sys,subprocess
p=sys.argv[1];c=cv2.VideoCapture(p);fps=c.get(5);F=[]
while True:
    r,f=c.read()
    if not r:break
    F.append(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY))
cas=cv2.CascadeClassifier('/workspace/cvenv/lib/python3.13/site-packages/cv2/data/haarcascade_frontalface_default.xml')
M=[];last=None;heads=[]
for g in F:
    fs=cas.detectMultiScale(g,1.1,5,minSize=(60,60))
    if len(fs): last=max(fs,key=lambda r:r[2]*r[3])
    x,y,w,h=last;heads.append((x+w/2,y+h/2))
    m=cv2.resize(g[y+int(.62*h):y+int(1.0*h),x+int(.25*w):x+int(.75*w)],(60,40)).astype(float)
    M.append(m)
D=np.array([np.abs(M[i]-M[i-1]).mean() for i in range(1,len(M))])
open_=np.array([m[15:35].std() for m in M])
au=subprocess.run(['ffmpeg','-loglevel','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
s=np.frombuffer(au,np.int16).astype(float);hop=int(16000/fps)
env=np.array([np.abs(s[i*hop:(i+1)*hop]).mean() for i in range(len(M))])
o=(open_-open_.mean())/open_.std();e=(env-env.mean())/env.std()
lags=range(-8,9);cc=[np.mean(o[max(0,L):len(o)+min(0,L)]*e[max(0,-L):len(e)-max(0,L)]) for L in lags]
b=list(lags)[int(np.argmax(cc))]
H=np.array(heads);hs=np.abs(np.diff(H,axis=0)).sum(1)
print(f'{p} mouthmotion={D.mean():.1f} open~audio r={max(cc):.2f} offset={b*1000/fps:.0f}ms headspeed_mean={hs.mean():.1f}px/f p95={np.percentile(hs,95):.1f} headrange_x={np.ptp(H[:,0]):.0f}')
