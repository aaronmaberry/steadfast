import cv2,json
P=json.load(open('../plan8.json'));cas2=cv2.CascadeClassifier('/workspace/cvenv/lib/python3.13/site-packages/cv2/data/haarcascade_profileface.xml');cas=cv2.CascadeClassifier('/workspace/cvenv/lib/python3.13/site-packages/cv2/data/haarcascade_frontalface_default.xml')
def face(i):
    g=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY);f=list(cas.detectMultiScale(g,1.05,3,minSize=(60,60)))
    if not f: f=list(cas2.detectMultiScale(g,1.05,3,minSize=(60,60)))+[(g.shape[1]-a-c,b,c,d) for a,b,c,d in cas2.detectMultiScale(cv2.flip(g,1),1.05,3,minSize=(60,60))]
    return max(f,key=lambda r:r[2]*r[3])
x,y,w,h=918,128,229,229
# W1 crop: [0:740,460:1776] -> relative
k=740/h; cx=(460+658-(x+w/2))/w; ty=(y-0)/h
print('ref',x,y,w,h,k,cx,ty)
out={}
for s,v in P.items():
    if s=='W1':continue
    im=cv2.imread(f"../src/start{v['start']:02d}.jpg");H,W=im.shape[:2]
    x,y,w,h=face(im);ch=min(H,int(k*h));cw=min(W,int(ch*1316/740));ch=int(cw*740/1316)
    X=int(x+w/2+cx*w-cw/2);Y=int(y-ty*h);X=max(0,min(W-cw,X));Y=max(0,min(H-ch,Y))
    c=im[Y:Y+ch,X:X+cw];cv2.imwrite(f'{s}chest.jpg',c,[1,95]);out[s]=(X,Y,cw,ch)
print(out)
