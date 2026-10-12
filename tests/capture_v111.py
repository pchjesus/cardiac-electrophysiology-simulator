"""Capture real v1.11 dashboard screens at desktop and mobile sizes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import base64

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"preview-v111"
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--disable-dev-shm-usage"])
 page=browser.new_page(viewport={"width":1366,"height":768},device_scale_factor=1)
 errors=[]
 page.on("pageerror",lambda e:errors.append(str(e)))
 page.goto((ROOT/"index.html").as_uri())
 page.wait_for_function("!!window.CardiacDashboard")
 page.locator("#playBtn").click()
 page.wait_for_timeout(280)
 page.locator("#pauseBtn").click()
 page.screenshot(path=str(OUT/"01-electrical-desktop.png"),full_page=True)
 page.locator("#mechanicalModeBtn").click()
 page.screenshot(path=str(OUT/"02-mechanical-desktop.png"),full_page=True)
 page.locator("#dashboardWiggersBtn").click()
 page.screenshot(path=str(OUT/"03-wiggers-desktop.png"),full_page=True)
 page.locator("#dashboardFocusBtn").click()
 page.screenshot(path=str(OUT/"08-wiggers-focus-desktop.png"),full_page=True)
 page.locator("#dashboardFocusBtn").click()
 page.locator("#wiggersDeepDive summary").click()
 page.screenshot(path=str(OUT/"04-wiggers-expanded.png"),full_page=True)
 page.set_viewport_size({"width":390,"height":844})
 page.locator("#electricalModeBtn").click()
 page.screenshot(path=str(OUT/"05-electrical-mobile.png"),full_page=True)
 page.locator("#dashboardWiggersBtn").click()
 page.screenshot(path=str(OUT/"06-wiggers-mobile.png"),full_page=True)
 page.locator("#userGuideBtn").click()
 page.screenshot(path=str(OUT/"07-guide-mobile.png"),full_page=True)
 assert not errors,errors
 browser.close()

W,H=735,660
pics=[
 ("1. Electrical desktop","01-electrical-desktop.png"),
 ("2. Mechanical desktop","02-mechanical-desktop.png"),
 ("3. Wiggers desktop","03-wiggers-desktop.png"),
 ("4. Extended learning desktop","04-wiggers-expanded.png"),
 ("5. Electrical mobile 390px","05-electrical-mobile.png"),
 ("6. Wiggers mobile 390px","06-wiggers-mobile.png")]
board=Image.new("RGB",(2*W,3*H),(235,241,247))
draw=ImageDraw.Draw(board)
try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",17)
except OSError:font=ImageFont.load_default()
for i,(label,fn) in enumerate(pics):
 im=Image.open(OUT/fn).convert("RGB")
 top=min(im.height,1180 if i<4 else 1400)
 im=im.crop((0,0,im.width,top))
 im.thumbnail((W-28,H-60),Image.Resampling.LANCZOS)
 x=(i%2)*W+(W-im.width)//2;y=(i//2)*H+40
 board.paste(im,(x,y))
 draw.text(((i%2)*W+14,(i//2)*H+11),label,fill=(29,53,75),font=font)
contact=OUT/"v111-dashboard-actual-contact.jpg"
board.save(contact,"JPEG",quality=72,optimize=True)
print("ACTUAL_SCREENSHOTS_OK",len(pics),"errors=0", "contact_size",contact.stat().st_size)
print("V111_CONTACT_BEGIN")
print(base64.b64encode(contact.read_bytes()).decode("ascii"))
print("V111_CONTACT_END")
