import os,json,base64,time,urllib.request
H={"Authorization":"Bearer "+os.environ["XAI_API_KEY"],"Content-Type":"application/json"}
img={"url":"data:image/png;base64,"+base64.b64encode(open('../../om3/src13-blend.png','rb').read()).decode()}
P=("Medium close-up, locked-off camera. He stands facing the camera and talks warmly and plainly to a small room, mouth clearly moving with natural speech, "
"small natural head nods and slight torso sway, relaxed shoulders, natural blinks, eyes on the camera and occasionally glancing just off camera. "
"His hands stay down at his sides and completely out of frame the entire clip; no hands, fingers, wrists or arms ever enter the frame. "
"No open palms, no pointing, no gestures in frame, no seats or chairs, no watch, no props, no other people, no text or captions. "
"Same face, short dark-brown hair, short beard, brown eyes, charcoal henley, same deep navy studio backdrop and lighting. Photoreal, no morphing.")
body={"model":"grok-imagine-video-1.5","prompt":P,"image":img,"duration":10,"resolution":"720p"}
r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.x.ai/v1/videos/generations",json.dumps(body).encode(),H),timeout=180))
rid=r.get("request_id") or r.get("id");print("rid",rid,flush=True)
while True:
    time.sleep(10)
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.x.ai/v1/videos/{rid}",headers=H),timeout=60))
    except Exception as e: continue
    if d.get("status") not in ("pending","queued","processing","in_progress",None) or "video" in d: break
print("status",d.get("status"),"usage",d.get("usage"),flush=True)
v=d.get("video",{}).get("url")
if v: urllib.request.urlretrieve(v,"x1-raw.mp4");print("ok")
