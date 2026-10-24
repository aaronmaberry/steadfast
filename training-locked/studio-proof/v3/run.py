import json,subprocess,fal_client,urllib.request,os,sys
from concurrent.futures import ThreadPoolExecutor
SRC={'X1':'/workspace/artifacts/training/w01-poc/poc4/lipsync-test/t03ls/x1/x1-raw.mp4','W9':'../v2/w09cat.mp4'}
P=json.load(open('pieces.json'))
def one(p):
    i=p['id'];src=SRC.get(p['src'],'../v2/%s.mp4'%p['src']);n=p['f1']-p['f0']
    if os.path.exists(i+'-s3.mp4'): return i,'cached'
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vf',f"select='between(n,{p['f0']},{p['f1']-1})',setpts=N/24/TB",'-an','-r','24','-c:v','libx264','-crf','12','-pix_fmt','yuv420p',i+'-raw.mp4'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(p['t0']),'-t',str(n/24),'-i','../voice63.wav',i+'.wav'],check=True)
    r=fal_client.subscribe('fal-ai/sync-lipsync/v3',arguments=dict(video_url=fal_client.upload_file(i+'-raw.mp4'),audio_url=fal_client.upload_file(i+'.wav'),sync_mode='cut_off'))
    urllib.request.urlretrieve(r['video']['url'],i+'-s3.mp4');return i,r['video'].get('duration'),n/24
with ThreadPoolExecutor(6) as ex:
    for x in ex.map(one,P): print(x,flush=True)
