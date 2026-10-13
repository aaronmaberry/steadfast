import numpy as np,cv2
def dering(fr,y0=380,dbg=False):
    im=fr[y0:].astype(np.int16); B,G,R=im[...,0],im[...,1],im[...,2]
    mx=im.max(2); mn=im.min(2); sat=(mx-mn)/np.maximum(mx,1)
    skin=((R>80)&(R>G+8)&(G>=B-5)&(sat>0.22)).astype(np.uint8)
    skin=cv2.morphologyEx(skin,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
    inner=cv2.erode(skin,np.ones((3,3),np.uint8))
    L=im.mean(2)
    met=((sat<0.22)&(L>95)&(inner>0)).astype(np.uint8)
    met=cv2.dilate(met,np.ones((5,5),np.uint8))
    out=fr.copy(); sub=np.ascontiguousarray(fr[y0:])
    if met.any(): sub=cv2.inpaint(sub,met,5,cv2.INPAINT_TELEA)
    med=cv2.medianBlur(cv2.medianBlur(sub,9),7)
    k=cv2.GaussianBlur(cv2.erode(skin,np.ones((5,5),np.uint8)).astype(np.float32),(0,0),2)[...,None]
    out[y0:]=(sub*(1-k)+med*k).astype(np.uint8)
    return (out,met) if dbg else out
if __name__=='__main__':
    import sys
    fr=cv2.imread(sys.argv[1]); o,m=dering(fr,dbg=True); print(m.sum()//255 if m.max()>1 else m.sum())
    cv2.imwrite(sys.argv[2],np.hstack([fr[500:900,900:1500],o[500:900,900:1500]]))
