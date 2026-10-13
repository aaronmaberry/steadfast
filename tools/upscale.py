import sys,torch,numpy as np,cv2,time,rrdb
torch.set_num_threads(8)
m=rrdb.load()
def up(img):
    x=torch.from_numpy(img[:,:,::-1].copy()).permute(2,0,1).float().div(255)[None]
    H,W=img.shape[:2];T=256;P=16;out=np.zeros((H*4,W*4,3),np.float32)
    for y in range(0,H,T):
        for xx in range(0,W,T):
            y0,x0=max(0,y-P),max(0,xx-P);y1,x1=min(H,y+T+P),min(W,xx+T+P)
            with torch.no_grad(): o=m(x[:,:,y0:y1,x0:x1])[0].permute(1,2,0).numpy()
            oy,ox=(y-y0)*4,(xx-x0)*4;h,w=min(T,H-y)*4,min(T,W-xx)*4
            out[y*4:y*4+h,xx*4:xx*4+w]=o[oy:oy+h,ox:ox+w]
    return (np.clip(out,0,1)*255).astype(np.uint8)[:,:,::-1]
for n in sys.argv[1:]:
    t=time.time();im=cv2.imread(f'/workspace/s01v2/raw/{n}.png');o=up(im)
    o=cv2.resize(o,(im.shape[1]*2,im.shape[0]*2),interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'hr/{n}.png',o);print(n,o.shape,round(time.time()-t),flush=True)
