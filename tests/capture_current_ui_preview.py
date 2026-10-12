"""Capture the real deployed-source UI from v1.10 Patch 5 using Chromium.
Preview-only runner script; does not alter application code or production branch.
"""
from pathlib import Path
import base64
from PIL import Image,ImageOps,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"screen-captures"
OUT.mkdir(exist_ok=True)
errors=[]

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path="/usr/bin/chromium",
       args=["--no-sandbox","--disable-dev-shm-usage"])
    page=browser.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri(),wait_until="load")
    page.wait_for_function("typeof window.CardiacLearning !== 'undefined' && typeof window.CardiacWiggersView !== 'undefined'")
    assert "v1.10 Patch 5" in page.locator("h1").inner_text()
    page.locator("#playBtn").click()
    page.wait_for_timeout(850)
    page.locator("#pauseBtn").click()
    page.evaluate("window.scrollTo(0,0)")
    page.screenshot(path=str(OUT/"01-actual-main.png"),full_page=True,animations="disabled")
    page.locator("#wiggersToggle").click(position={"x":12,"y":12})
    page.wait_for_function("document.getElementById('wiggersDetails').open")
    page.locator('[data-learning-preset="normal"]').click()
    page.locator("#wiggersDeepDive summary").click()
    page.wait_for_function("document.getElementById('wiggersDeepDive').open")
    page.locator("#wiggersDetails").screenshot(path=str(OUT/"02-actual-wiggers-learning.png"),animations="disabled")
    page.evaluate("window.scrollTo(0,0)")
    page.locator("#patchNotesBtn").click()
    assert page.locator("#patchNotesPanel").is_visible()
    page.screenshot(path=str(OUT/"03-actual-patch-notes.png"),animations="disabled")
    page.locator("#userGuideBtn").click()
    assert page.locator("#userGuidePanel").is_visible()
    page.screenshot(path=str(OUT/"04-actual-user-guide.png"),animations="disabled")
    browser.close()

assert not errors,errors

files=[
  ("1. Current main screen", "01-actual-main.png"),
  ("2. Wiggers & medical learning", "02-actual-wiggers-learning.png"),
  ("3. Categorized patch history", "03-actual-patch-notes.png"),
  ("4. User guide popup", "04-actual-user-guide.png"),
]
W,H=760,690
board=Image.new("RGB",(W*2,H*2),(237,243,248))
draw=ImageDraw.Draw(board)
try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",19)
except OSError: font=ImageFont.load_default()
for k,(label,path) in enumerate(files):
    img=Image.open(OUT/path).convert("RGB")
    if k==0:
        # Top viewport: ECG monitor, controls and Electrical/Mechanical selection
        img=img.crop((0,0,img.width,min(1130,img.height)))
    if k==1:
        # Full optional Wiggers panel: SVG chart and extended nurse explanations
        img=img.crop((0,0,img.width,min(1400,img.height)))
    if k in (2,3): img=img.crop((0,0,img.width,min(900,img.height)))
    img.thumbnail((W-34,H-75),Image.Resampling.LANCZOS)
    x=(k%2)*W+(W-img.width)//2
    y=(k//2)*H+47
    board.paste(img,(x,y))
    draw.text(((k%2)*W+19,(k//2)*H+14),label,fill=(28,57,80),font=font)
    draw.rounded_rectangle((x-1,y-1,x+img.width+1,y+img.height+1),
       radius=2,outline=(163,185,204),width=2)
contact=OUT/"current-v110-patch5-preview.jpg"
board.save(contact,"JPEG",quality=66,optimize=True)
print("CAPTURE_OK:",len(files),"screens, page errors:",errors,"contact bytes:",contact.stat().st_size)
print("UI_SCREENSHOT_BASE64_BEGIN")
print(base64.b64encode(contact.read_bytes()).decode("ascii"))
print("UI_SCREENSHOT_BASE64_END")


# Keep readable individual captures alongside the contact sheet.
for label,filename in (
    ("MAIN","01-actual-main.png"),
    ("WIGGERS","02-actual-wiggers-learning.png"),
    ("PATCH_NOTES","03-actual-patch-notes.png"),
    ("USER_GUIDE","04-actual-user-guide.png"),
):
    shot=Image.open(OUT/filename).convert("RGB")
    shot.thumbnail((1440,2800),Image.Resampling.LANCZOS)
    from io import BytesIO
    buf=BytesIO()
    shot.save(buf,"JPEG",quality=76,optimize=True)
    (OUT/("hires-"+label.lower().replace("_","-")+".jpg")).write_bytes(buf.getvalue())
    print("UI_"+label+"_BASE64_BEGIN")
    print(base64.b64encode(buf.getvalue()).decode("ascii"))
    print("UI_"+label+"_BASE64_END")
