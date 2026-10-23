import os,json,base64,time,urllib.request,sys
H={"Authorization":"Bearer "+os.environ["XAI_API_KEY"],"Content-Type":"application/json"}
tag,src,mode=sys.argv[1:4]
img={"url":"data:image/png;base64,"+base64.b64encode(open(src,'rb').read()).decode()}
G=("He talks warmly and plainly to a small room, mouth clearly and continuously moving with natural speech the whole clip, never pausing silent, "
"small natural head nods, slight torso sway, natural blinks, eyes mostly on camera. ")
if mode=='nohands': G+=("Tight chest-up framing, locked-off camera. His arms stay relaxed at his sides below the bottom edge of the frame the entire clip; hands, fingers, wrists and forearms never enter the frame. ")
else: G+=("Locked-off camera. Natural, varied, low conversational gestures near his waist with relaxed curled fingers, hands mostly low; no open palms facing camera, no thumbs-up, no pointing. ")
G+=("No watch, no jewelry, no seats or chairs, no props, no other people, no text or captions, no music. Same face, short dark-brown hair, short beard, brown eyes, charcoal henley, same deep navy studio backdrop and lighting. Photoreal, no morphing.")
body={"model":"grok-imagine-video-1.5","prompt":G,"image":img,"duration":10,"resolution":"720p"}
r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.x.ai/v1/videos/generations",json.dumps(body).encode(),H),timeout=180))
rid=r.get("request_id") or r.get("id");print(tag,"rid",rid,time.strftime('%H:%M'),flush=True)
while True:
    time.sleep(10)
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.x.ai/v1/videos/{rid}",headers=H),timeout=60))
    except Exception as e: continue
    if d.get("status") in ("done","failed","expired") or "video" in d: break
print(tag,"status",d.get("status"),"usage",d.get("usage"),flush=True)
v=d.get("video",{}).get("url")
if v: urllib.request.urlretrieve(v,tag+".mp4");print(tag,"ok")
