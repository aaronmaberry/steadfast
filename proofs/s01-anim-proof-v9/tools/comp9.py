import cv2,numpy as np,glob,json,os,subprocess,sys,insightface
from PIL import Image
from rembg import remove,new_session
from insightface.app import FaceAnalysis
app=FaceAnalysis(name='buffalo_l',providers=['CPUExecutionProvider']);app.prepare(ctx_id=-1,det_size=(640,640))
SW=insightface.model_zoo.get_model('/workspace/tools/swap-models/inswapper_128.onnx',providers=['CPUExecutionProvider'])
SES=new_session('u2net_human_seg')
big=lambda fs:max(fs,key=lambda f:(f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1])) if fs else None
MASTER=big(app.get(cv2.imread('/workspace/s01v9/w1/master_wes.png')))
BGMAP={'S1-wide':'a1','S2-medium':'a2','S3-medcloseup':'a4','S4-34left':'a3','S5-34right':'a5','S6-walk':'a6','S7-gesture':'a8'}
def plate(still):
    P=np.asarray(Image.open(f'/workspace/s01v7/v7/bg/A_{BGMAP[still]}.png').convert('RGB').resize((1280,720),Image.LANCZOS)).astype(np.float32)
    L=P.mean(2)>190; L[410:]=False; return P,L
def hair(im,f):
    x0,y0,x1,y1=f.bbox.astype(int);h=y1-y0
    c=im[max(0,y0-int(.45*h)):max(1,y0+int(.1*h)),max(0,x0):x1]
    c=cv2.cvtColor(c,cv2.COLOR_BGR2GRAY);c=cv2.resize(c,(128,max(8,int(128*c.shape[0]/c.shape[1]))))
    return float(np.abs(cv2.Laplacian(c,cv2.CV_64F)).mean())
def hairm(im,bb,a):
    x0,y0,x1,y1=bb;h=y1-y0; ya,yb=max(0,y0-int(.45*h)),max(1,y0+int(.1*h)); xa=max(0,x0)
    c=cv2.cvtColor(im[ya:yb,xa:x1],cv2.COLOR_BGR2GRAY).astype(np.float64); m=a[ya:yb,xa:x1]>0.9
    sc=128/max(1,c.shape[1]); c=cv2.resize(c,(128,max(8,int(c.shape[0]*sc)))); m=cv2.resize(m.astype(np.uint8),(c.shape[1],c.shape[0]),interpolation=cv2.INTER_NEAREST)>0
    m=cv2.erode(m.astype(np.uint8),np.ones((3,3),np.uint8))>0; Lp=np.abs(cv2.Laplacian(c,cv2.CV_64F))
    return float(Lp[m].mean()) if m.sum()>50 else None
def shiftx(x,dx):
    if dx==0: return x
    y=np.roll(x,dx,1)
    if dx>0: y[:,:dx]=0
    else: y[:,dx:]=0
    return y
def run(name,video,still,walk_dx=0,outdir='/workspace/s01v9/p9/shots'):
    os.makedirs(outdir,exist_ok=True); W=f'/workspace/s01v9/p9/work/{name}'; os.makedirs(W+'/fr',exist_ok=True)
    subprocess.run(f'rm -f {W}/fr/*',shell=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',video,f'{W}/fr/%04d.png'],check=True)
    fs=sorted(glob.glob(f'{W}/fr/*.png')); P,L=plate(still); n=len(fs)
    frames=[];masks=[];boxes=[]
    for p in fs:
        im=cv2.imread(p); f=big(app.get(im))
        if f is not None: im=SW.get(im,f,MASTER,paste_back=True)
        boxes.append(None if f is None else f.bbox.astype(int))
        rgb=np.ascontiguousarray(im[...,::-1]); frames.append(rgb)
        masks.append(np.asarray(remove(Image.fromarray(rgb),session=SES,only_mask=True)).astype(np.uint8))
    M=np.array(masks,np.uint8); del masks[:]; Ms=np.empty_like(M)
    for i in range(n): Ms[i]=np.median(M[max(0,i-2):i+3],0).astype(np.uint8)   # temporal median kills topology flicker
    k9=np.ones((9,9),np.uint8); k25=np.ones((25,25),np.uint8)
    # per-shot colour match of HeyGen frame to plate, measured on clear background
    outside=np.ones((720,1280),bool)
    for i in range(0,n,max(1,n//10)): outside&=cv2.dilate((Ms[i]>51).astype(np.uint8),k25)==0
    outside&=~L
    med=np.median(np.array(frames[::max(1,n//10)]),0).astype(np.float32)
    gain=np.array([np.median(P[...,c][outside]+1)/np.median(med[...,c][outside]+1) for c in range(3)]); gain=np.clip(gain,0.9,1.1)
    S=cv2.resize(cv2.imread(f'/workspace/steadfast/training-locked/v9-face-master/{still}.png'),(1280,720),interpolation=cv2.INTER_AREA)
    sf=big(app.get(S)); sm=np.asarray(remove(Image.fromarray(S[...,::-1].copy()),session=SES,only_mask=True)).astype(np.float32)/255
    href=hairm(S,sf.bbox.astype(int),sm); hlog=[]
    enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','25','-i','-','-i',video,'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',f'{outdir}/{name}.mp4'],stdin=subprocess.PIPE)
    def bgish(rgb):
        r,g,b=[rgb[...,c].astype(np.float32) for c in range(3)]
        return ((b-np.maximum(r,g)>10)&((r+g+b)/3<170)).astype(np.float32)
    del M; BK=np.array([bgish(f) for f in frames],np.uint8); bgk=np.empty((n,720,1280),np.uint8)
    for i in range(n):
        x=np.median(BK[max(0,i-2):i+3],0).astype(np.float32)
        x=cv2.morphologyEx(x,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); bgk[i]=(cv2.GaussianBlur(x,(7,7),0)*255).round().astype(np.uint8)
    del BK; alphas=np.empty((n,720,1280),np.float16);Fcs=[]
    prev_band=None
    for i in range(n):
        Fc=np.clip(frames[i].astype(np.float32)*gain,0,255); m=Ms[i].astype(np.float32)/255
        core=cv2.erode((m>0.5).astype(np.uint8),k9).astype(np.float32)
        band=(cv2.dilate((m>0.5).astype(np.uint8),np.ones((15,15),np.uint8))>0).astype(np.float32)-core
        d=np.abs(Fc-P).mean(2); ab=np.clip((d-6)/14,0,1)*band
        if prev_band is not None: ab=0.5*ab+0.5*prev_band
        prev_band=ab
        a=np.maximum(core,ab)
        # kill generator floor/backdrop carried inside the matte (purple-blue, dark) -> was the W1 arm-gap patch
        a=a*(1-bgk[i].astype(np.float32)/255); a=cv2.GaussianBlur(a,(5,5),0); a[L]=0
        if boxes[i] is not None and href:
            bb=boxes[i]; bgr=np.ascontiguousarray(Fc[...,::-1]).astype(np.uint8); h0=hairm(bgr,bb,a)
            used=0
            if h0 and h0>1.05*href:
                x0,y0,x1,y1=bb; h=y1-y0; w=x1-x0
                z=np.zeros((720,1280),np.float32); z[max(0,y0-int(.6*h)):max(1,y0+int(.15*h)),max(0,x0-int(.2*w)):min(1280,x1+int(.2*w))]=1
                z=cv2.GaussianBlur(z,(31,31),0)*np.clip(a,0,1)
                for sg in (0.6,0.8,1.0,1.3,1.6,2.0):
                    Fb=cv2.GaussianBlur(Fc,(0,0),sg); Ft=Fc*(1-z[...,None])+Fb*z[...,None]
                    h1=hairm(np.ascontiguousarray(Ft[...,::-1]).astype(np.uint8),bb,a); used=sg
                    if h1 is None or h1<=1.05*href: break
                Fc=Ft; h0=h1
            hlog.append([i,used,h0])
        dx=int(round(walk_dx*i/max(1,n-1)))
        if dx: Fc=shiftx(Fc,dx); a=shiftx(a,dx)
        out=Fc*a[...,None]+P*(1-a[...,None])
        enc.stdin.write(out.clip(0,255).astype(np.uint8).tobytes()); alphas[i]=a
    enc.stdin.close(); enc.wait()
    np.save(f'{W}/alpha.npy',alphas)
    json.dump({'href':href,'hair_soften':hlog,'gain':gain.tolist(),'still':still,'walk_dx':walk_dx},open(f'{W}/meta.json','w'))
    print('done',name,flush=True)
if __name__=='__main__':
    j=json.loads(sys.argv[1]); run(**j)
