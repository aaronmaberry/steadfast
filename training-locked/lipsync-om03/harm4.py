import cv2,numpy as np,subprocess,sys
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider'],allowed_modules=['detection','recognition','landmark_2d_106']);app.prepare(ctx_id=-1,det_size=(640,640))
Mn=np.load('v13ref/mean_arcface_embedding.npy');Mn=Mn/np.linalg.norm(Mn)
OUT=sys.argv[1];CW=float(sys.argv[2]);GR=float(sys.argv[3]);NF=int(sys.argv[4]);T0=int(sys.argv[5]) if len(sys.argv)>5 else 0
R=cv2.VideoCapture('om3-raw.mp4');S=cv2.VideoCapture('om3-v13m2.mp4');W,H=1248,704
for _ in range(T0): R.read();S.read()
p=subprocess.Popen(f"ffmpeg -v error -y -f rawvideo -pix_fmt bgr24 -s {W}x{H} -r 25 -i - -ss {T0/25} -i om3-raw.mp4 -map 0:v -map 1:a -t {NF/25} -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac {OUT}".split(),stdin=subprocess.PIPE)
cs=None;sc=[];yy,xx=np.mgrid[0:H,0:W]
for i in range(NF):
    _,r=R.read();_,s=S.read()
    L=max(app.get(r),key=lambda z:z.bbox[2]-z.bbox[0]).landmark_2d_106;fw=L[:,0].max()-L[:,0].min()
    m=np.zeros((H,W),np.uint8);cv2.fillConvexPoly(m,cv2.convexHull(L.astype(np.int32)),1)
    inner=cv2.erode(m,np.ones((9,9),np.uint8))>0
    Rl=cv2.cvtColor(r,cv2.COLOR_BGR2LAB).astype(np.float32);Sl=cv2.cvtColor(s,cv2.COLOR_BGR2LAB).astype(np.float32)
    st=np.concatenate([Sl[inner].mean(0),Sl[inner].std(0),Rl[inner].mean(0),Rl[inner].std(0)])
    cs=st if cs is None else 0.7*cs+0.3*st
    d=cs[0:3]-cs[6:9]                       # swap minus raw (face)
    # face: move CW of the way toward raw stats
    Sm=(Sl-cs[0:3])*(1+CW*(cs[9:12]/(cs[3:6]+1e-3)-1))+cs[0:3]-CW*d
    # surround skin: shift by (1-CW)*d with distance falloff from face
    dist=cv2.distanceTransform((1-m).astype(np.uint8),cv2.DIST_L2,5)
    fall=np.exp(-(dist/(0.45*fw))**2)
    ch=np.hypot(Rl[...,1]-128,Rl[...,2]-128);skin=((Rl[...,1]>134)&(ch>8)&(Rl[...,0]>40)).astype(np.float32)
    skin=cv2.GaussianBlur(skin,(0,0),3)
    wout=fall*skin
    fm=cv2.GaussianBlur(m.astype(np.float32),(0,0),fw*0.05)
    Out=Sm*fm[...,None]+(Sl+(1-CW)*d*wout[...,None])*(1-fm[...,None])
    o=cv2.cvtColor(np.clip(Out,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR).astype(np.float32)
    # grain: add raw high-frequency onto face
    rf=r.astype(np.float32);hi=rf-cv2.GaussianBlur(rf,(0,0),1.2)
    o=o+GR*hi*fm[...,None]+0.7*(o-cv2.GaussianBlur(o,(0,0),2.2))*fm[...,None]
    out=np.clip(o,0,255).astype(np.uint8)
    e=app.get(out);sc.append(float(max(e,key=lambda z:z.bbox[2]-z.bbox[0]).normed_embedding@Mn) if e else 0)
    p.stdin.write(out.tobytes())
p.stdin.close();p.wait();sc=np.array(sc);np.save(OUT+'.scores.npy',sc)
print(OUT,'n',NF,'mean %.3f min %.3f at %.2fs nbelow %d'%(sc.mean(),sc.min(),(sc.argmin()+T0)/25,(sc<0.85).sum()))
