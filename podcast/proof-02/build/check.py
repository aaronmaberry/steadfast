import sys,cv2,numpy as np
sys.path.insert(0,'/workspace/pp2/tools');import mouth as M
for n in sys.argv[1:]:
    v=f'av/{n}.mp4';cap=cv2.VideoCapture(v);W=int(cap.get(3));H=int(cap.get(4))
    det=cv2.FaceDetectorYN.create('/workspace/pp2/tools/yunet.onnx','',(W,H),0.6);ref=None;d=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        _,fs=det.detect(f)
        if fs is None:continue
        x=fs[0];rx,ry,lx,ly=x[10:14];w=abs(lx-rx);cx=(rx+lx)/2;cy=(ry+ly)/2
        g=cv2.cvtColor(f[int(cy-w*.4):int(cy+w*.6),int(cx-w*.8):int(cx+w*.8)],cv2.COLOR_BGR2GRAY);g=cv2.resize(g,(64,40)).astype(float)
        if ref is None:ref=g
        d.append(np.abs(g-ref).mean())
    d=np.array(d);m,fps=M.mouth_series(v);e=M.audio_env(f'audio/n/{n}.mp3',fps);k,c,c0=M.lag(m,e,6)
    print(n,W,H,f'mouthdiff mean={d.mean():.1f} p90={np.percentile(d,90):.1f} corr0={c0:.2f} best={c:.2f}@{k}', 'PASS' if d.mean()>3 and np.percentile(d,90)>6 else 'FAIL')
