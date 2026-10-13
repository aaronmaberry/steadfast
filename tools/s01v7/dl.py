import json,subprocess,os
for k,i in json.load(open('lsids7g.json')).items():
    f=f'clips/lsg_{k}.mp4'
    if os.path.exists(f) and os.path.getsize(f)>100000: continue
    r=subprocess.run(['curl','-s','-o',f,'-w','%{http_code}',f'https://resource2.heygen.ai/video_translate/{i}/original.mp4'],capture_output=True,text=True).stdout
    if r!='200' and os.path.exists(f): os.remove(f)
    print(k,r)
