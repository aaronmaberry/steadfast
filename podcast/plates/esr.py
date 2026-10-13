import torch,torch.nn as nn,torch.nn.functional as F,numpy as np
from PIL import Image
class RDB(nn.Module):
    def __init__(s,nf=64,gc=32):
        super().__init__()
        s.conv1=nn.Conv2d(nf,gc,3,1,1);s.conv2=nn.Conv2d(nf+gc,gc,3,1,1);s.conv3=nn.Conv2d(nf+2*gc,gc,3,1,1);s.conv4=nn.Conv2d(nf+3*gc,gc,3,1,1);s.conv5=nn.Conv2d(nf+4*gc,nf,3,1,1);s.l=nn.LeakyReLU(0.2,True)
    def forward(s,x):
        x1=s.l(s.conv1(x));x2=s.l(s.conv2(torch.cat((x,x1),1)));x3=s.l(s.conv3(torch.cat((x,x1,x2),1)));x4=s.l(s.conv4(torch.cat((x,x1,x2,x3),1)));return s.conv5(torch.cat((x,x1,x2,x3,x4),1))*0.2+x
class RRDB(nn.Module):
    def __init__(s):super().__init__();s.rdb1=RDB();s.rdb2=RDB();s.rdb3=RDB()
    def forward(s,x):return s.rdb3(s.rdb2(s.rdb1(x)))*0.2+x
class Net(nn.Module):
    def __init__(s):
        super().__init__();s.conv_first=nn.Conv2d(3,64,3,1,1);s.body=nn.Sequential(*[RRDB() for _ in range(23)]);s.conv_body=nn.Conv2d(64,64,3,1,1);s.conv_up1=nn.Conv2d(64,64,3,1,1);s.conv_up2=nn.Conv2d(64,64,3,1,1);s.conv_hr=nn.Conv2d(64,64,3,1,1);s.conv_last=nn.Conv2d(64,3,3,1,1);s.l=nn.LeakyReLU(0.2,True)
    def forward(s,x):
        f=s.conv_first(x);f=f+s.conv_body(s.body(f));f=s.l(s.conv_up1(F.interpolate(f,scale_factor=2,mode='nearest')));f=s.l(s.conv_up2(F.interpolate(f,scale_factor=2,mode='nearest')));return s.conv_last(s.l(s.conv_hr(f)))
m=Net();sd=torch.load('x4.pth',map_location='cpu');m.load_state_dict(sd.get('params_ema',sd));m.eval()
im=Image.open('/workspace/steadfast/img/LOCKED-podcast-table.jpg').convert('RGB')
for n,b in [('wes',(0,200,700,1080)),('co',(850,240,1408,1080)),('bg',(380,0,1100,560))]:
    c=im.crop(b);W,H=c.size;a=torch.from_numpy(np.array(c)).permute(2,0,1)[None].float()/255
    out=torch.zeros(1,3,H*4,W*4);T=160;P=12
    for y in range(0,H,T):
      for x in range(0,W,T):
        x0,y0=max(x-P,0),max(y-P,0);x1,y1=min(x+T+P,W),min(y+T+P,H)
        with torch.no_grad(): o=m(a[:,:,y0:y1,x0:x1])
        tw,th=min(T,W-x),min(T,H-y)
        out[:,:,y*4:(y+th)*4,x*4:(x+tw)*4]=o[:,:,(y-y0)*4:(y-y0+th)*4,(x-x0)*4:(x-x0+tw)*4]
    o=Image.fromarray((out[0].permute(1,2,0).clamp(0,1).numpy()*255).astype('uint8'))
    # blend 70% ESRGAN with 30% lanczos to avoid plastic look
    l=im.crop(b).resize(o.size,Image.LANCZOS);Image.blend(l,o,0.7).save(n+'4.png');print(n,o.size,flush=True)
