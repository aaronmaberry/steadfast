exec(open('fsc.py').read().split("a,b=int")[0])
import sys
a,b,step,name=float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
c=cv2.VideoCapture('studio-proof-L01-60s-v2.mp4');c.set(cv2.CAP_PROP_POS_FRAMES,int(a*24));T=[]
for n in range(int(a*24),int(b*24)):
    ok,f=c.read()
    if (n-int(a*24))%step: continue
    r=app.get(f);z=max(r,key=lambda z:z.bbox[2]-z.bbox[0]);L=z.landmark_2d_106[52:72]
    cx,cy=L.mean(0);w=(z.bbox[2]-z.bbox[0])*0.6
    T.append(cv2.resize(f[int(cy-w*0.4):int(cy+w*0.4),int(cx-w/2):int(cx+w/2)],(120,96)))
while len(T)%10: T.append(np.zeros_like(T[0]))
cv2.imwrite(name,np.vstack([np.hstack(T[i:i+10]) for i in range(0,len(T),10)]))
