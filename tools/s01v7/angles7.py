import json
from PIL import Image
R=Image.open('v7/bg/room69_clean_v7.png').convert('RGB'); W,H=R.size
A={
 'a1':dict(crop=(0,0,1.0)),
 'a2':dict(crop=(0.05,0.0,0.85)),
 'a3':dict(crop=(0.10,0.0,0.75)),
 'a4':dict(crop=(0.0,0.06,0.80)),
 'a5':dict(crop=(0.15,0.02,0.68)),
 'a6':dict(crop=(0.0,0.0,0.92)),
 'a7':dict(crop=(0.14,0.0,0.66)),
 'a8':dict(crop=(0.12,0.0,0.80)),
 'sp':dict(crop=(0.13,0.0,0.50),out=(960,1080)),
}
for n,a in A.items():
    x0,y0,w=a['crop']; ow,oh=a.get('out',(1920,1080))
    cw=w*W; ch=cw*oh/ow; box=(int(x0*W),int(y0*H),int(x0*W+cw),min(H,int(y0*H+ch)))
    assert box[3]<=H, (n,box)
    R.crop(box).resize((ow,oh),Image.LANCZOS).save(f'v7/bg/A_{n}.png'); print(n,box)
