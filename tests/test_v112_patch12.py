"""Patch12: student reading text sizes, full ECG concept access and narrow viewport/keyboard."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/"preview-v112p12"
SHOTS.mkdir(exist_ok=True)
n=0
def ck(v,m):
 global n
 assert v,m
 n+=1
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={"width":1366,"height":768})
 errors=[]
 page.on("pageerror",lambda e:errors.append(str(e)))
 page.goto((ROOT/"index.html").as_uri())
 ck("Patch 12" in page.locator("h1").inner_text(),"version incorrect")
 ck(page.locator("#guidedV112Toggle").is_visible(),"guided start missing")
 ck(page.evaluate("CardiacDashboard.isReady"),"initial Ready state missing")
 page.locator("#guidedV112Toggle").click()
 ck(page.evaluate("CardiacGuidedLearning.selectedStageId")=="atrial_systole","first stage lost")
 ck(page.evaluate("CardiacMechanical.currentState.stage")=="atrial_systole","first observation lost")
 ck(page.locator("#guidedV112Tools").evaluate("e=>!e.open"),"optional controls open by default")
 ck(page.evaluate("""()=>parseFloat(getComputedStyle(document.querySelector('#guidedV112Gist')).fontSize)""")>=15,
    "gist remains small")
 ck(page.evaluate("""()=>parseFloat(getComputedStyle(document.querySelector('.guided-v112-summary dd')).fontSize)""")>=15,
    "original clinical summary too small")
 for width in (360,390,680,768,1024,1366,1440):
  page.set_viewport_size({"width":width,"height":800})
  ck(page.evaluate("document.documentElement.scrollWidth <= innerWidth+2"),f"horizontal overflow {width}")
  ck(page.locator("#guidedV112Gist").is_visible(),f"missing beginner reading {width}")
  ck(page.locator("#ecgCanvas").is_visible(),f"ECG canvas lost {width}")
  if width<=699:
   allButtons=page.locator(".ecg-interpretation .ecg-item")
   ck(allButtons.count()==5,f"five ECG buttons missing {width}")
   layout=page.evaluate("""()=>{let e=document.querySelector('.ecg-interpretation');
      return {outer:e.clientWidth,scroll:e.scrollWidth,items:Array.from(e.children).map(x=>{
      let r=x.getBoundingClientRect();return {width:r.width,height:r.height,tag:x.tagName,cls:x.className,
      minHeight:getComputedStyle(x).minHeight,display:getComputedStyle(x).display,
      matches:x.matches('.dashboard-active .dashboard-v111[data-density="compact"] .dashboard-primary>.ecg-panel .ecg-item'),
      density:x.closest('.dashboard-v111')?.dataset.density,
      rules:Array.from(document.styleSheets).flatMap(sh=>Array.from(sh.cssRules||[]))
       .filter(ru=>ru.conditionText?.includes('699')).flatMap(ru=>Array.from(ru.cssRules||[]))
       .filter(ru=>ru.selectorText?.includes('ecg-item')).map(ru=>({selector:ru.selectorText,
          min:ru.style.getPropertyValue('min-height'),prio:ru.style.getPropertyPriority('min-height'),
          matches:x.matches(ru.selectorText)})).slice(-5)}})}}""")
   ck(layout["scroll"]<=layout["outer"]+2,f"ECG still scrolls sideways {width}: {layout}")
   ck(all(item["height"]>=40 for item in layout["items"]),f"ECG tap target too small {width}: {layout}")
  if width in (390,1366):
   page.screenshot(path=str(SHOTS/f"{width}-guided-basic.png"),full_page=True,animations="disabled")
 # Native summary is accessible by keyboard; controls have no hidden simulation side effects.
 page.locator("#guidedV112Tools>summary").focus()
 page.keyboard.press("Enter")
 ck(page.locator("#guidedV112Tools").evaluate("e=>e.open"),"keyboard disclosure failed")
 previous=page.evaluate("""()=>({a:heartState.physiologicalTime,b:heartState.visualizationTime,
   p:heartState.playing})""")
 page.locator("#guidedV112Level").select_option("intermediate")
 ck(page.evaluate("""()=>({a:heartState.physiologicalTime,b:heartState.visualizationTime,
   p:heartState.playing})""")==previous,"learning level changed A/B clock")
 ck(page.locator("#guidedV112Nursing").is_visible(),"original nursing content inaccessible")
 ck(page.locator("#guidedV112Quiz").count()==1,"quiz lost")
 ck(page.evaluate("""()=>['atrial_systole','isovolumetric_contraction','ejection',
   'isovolumetric_relaxation','filling'].every(s=>['basic','advanced']
   .every(t=>CardiacGuidedQuestions.get(s,t)?.explanation?.length>12))"""),"ten original quiz explanations lost")
 ck(page.locator("#wiggersDeepDive").count()==1,"original long-form nursing lost")
 ck(page.locator("#ecgCanvas").count()==1,"duplicate ECG canvas")
 ck(not errors,f"JS page errors {errors}")
 b.close()
print(f"PASS {n} Patch12 readable student/mobile/keyboard assertions")
