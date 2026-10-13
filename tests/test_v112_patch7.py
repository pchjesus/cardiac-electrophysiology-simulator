"""Patch 7: real-browser ECG-first workbench geometry and responsive behavior."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
cnt=0
def ck(v,m):
    global cnt
    assert v,m
    cnt+=1
with sync_playwright() as pw:
    b=pw.chromium.launch()
    page=b.new_page(viewport={"width":1366,"height":768})
    errs=[]
    page.on("pageerror",lambda e:errs.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    geo=page.evaluate("""()=>{
      const rect=s=>{const r=document.querySelector(s).getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}};
      return {ecg:rect('.dashboard-v111 .dashboard-primary>.ecg-panel'),guide:rect('.dashboard-v111>.dashboard-inspector'),
        visual:rect('.dashboard-v111 .dashboard-primary>.dashboard-workspace'),
        detail:rect('.dashboard-v111>.dashboard-resources')}
    }""")
    ck(abs(geo["ecg"]["y"]-geo["guide"]["y"])<10,f"ECG+guide not aligned {geo}")
    ck(geo["ecg"]["x"]+geo["ecg"]["w"]<=geo["guide"]["x"]+12,f"Not side-by-side {geo}")
    ck(geo["visual"]["y"]>geo["ecg"]["y"],"Visualization not below ECG")
    ck(geo["detail"]["y"]>=geo["visual"]["y"],"Resources not below visual")
    ck(page.locator("#wiggersDeepDive").count()==1,"Original source duplicated")
    ck(page.locator(".phase-panel").count()==1,"Original phases duplicated")
    ck(page.locator("#ecgCanvas").count()==1,"ECG Canvas duplicated")
    ck(page.locator("#guidedV112Panel").is_hidden(),"Study mode not opt-in")
    page.locator("#guidedV112Toggle").click()
    page.locator("#guidedV112Tools").evaluate("(e)=>e.open=true")
    for st in ("atrial_systole","ejection","isovolumetric_relaxation","filling"):
        page.locator("#guidedV112Select").select_option(st)
        ck(page.locator("#guidedV112Title").is_visible(),f"Study title missing {st}")
    page.locator("#guidedV112Toggle").click()
    page.locator("#dashboardDensityBtn").click()
    ck(page.locator("#dashboardResources").evaluate("(e)=>e.open"),"Source index unavailable")
    ck(not page.locator(".dashboard-phase-details").evaluate("(e)=>e.open"),
       "Source index must not bulk-open phase")
    ck(not page.locator(".dashboard-event-details").evaluate("(e)=>e.open"),
       "Source index must not bulk-open events")
    page.locator(".dashboard-phase-details>summary").click()
    ck(page.locator("#phaseDescription").is_visible(),"Original phase info not accessible")
    page.locator("#dashboardDensityBtn").click()
    page.locator("#dashboardWiggersBtn").click()
    ck(page.locator("#wiggersChart").is_visible(),"Wiggers view missing")
    page.locator("#dashboardFocusBtn").click()
    ck(page.evaluate("document.getElementById('dashboardV111').dataset.wiggersFocus")=="true","focus state lost")
    page.locator("#dashboardFocusBtn").click()
    for width in (360,390,768,1024,1366,1440):
        page.set_viewport_size({"width":width,"height":800})
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),f"Horizontal overflow at {width}")
        if width>=1200:
            g=page.evaluate("""()=>{
              const a=document.querySelector('.dashboard-v111 .dashboard-primary>.ecg-panel').getBoundingClientRect();
              const b=document.querySelector('.dashboard-v111>.dashboard-inspector').getBoundingClientRect();
              return {ay:a.y,by:b.y,ax:a.x,bx:b.x}
            }""")
            ck(abs(g["ay"]-g["by"])<10 and g["bx"]>g["ax"],f"Desktop reflow broken at {width}: {g}")
    ck(not errs,f"JavaScript: {errs}")
    b.close()
print(f"PASS {cnt} Patch7 workbench and six-width checks")
