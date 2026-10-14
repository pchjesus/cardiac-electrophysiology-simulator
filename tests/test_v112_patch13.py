"""Patch 13: same original mechanical SVG+readout in desktop row, model notes on-demand."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/"preview-v112p13"
SHOTS.mkdir(exist_ok=True)
n=0
def ck(x,msg):
    global n
    assert x,msg
    n+=1
with sync_playwright() as p:
    b=p.chromium.launch()
    page=b.new_page(viewport={"width":1366,"height":768})
    errs=[]
    page.on("pageerror",lambda e:errs.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    ck("v1.12 Patch " in page.locator("h1").inner_text(),"active version wrong")
    ck(page.locator("#mechanicalSVG").count()==1,"original mechanical SVG duplicated")
    ck(page.locator("#mechanicalPhase").count()==1,"original mechanical phase duplicated")
    ck(page.locator("#mechanicalModelInfo").count()==1,"source info missing")
    page.locator("#mechanicalModeBtn").click()
    ck(page.locator("#mechanicalView").is_visible(),"Mechanical mode missing")
    ck(not page.locator("#mechanicalModelInfo").evaluate("e=>e.open"),"long-form note open by default")
    ck(not page.locator(".mechanical-model-info-body").is_visible(),"long note takes default space")
    ck(not page.locator("#mechanicalSVG .model-caption").first.is_visible(),"repeated drawing warning visible")
    for width in (360,390,768,899,900,1024,1366,1440):
        page.set_viewport_size({"width":width,"height":800})
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),f"horizontal overflow {width}")
        geo=page.evaluate("""()=>{const svg=document.querySelector('#mechanicalSVG').getBoundingClientRect();
           const text=document.querySelector('.mechanical-readout').getBoundingClientRect();
           return {sx:svg.x,sy:svg.y,sw:svg.width,sh:svg.height,tx:text.x,ty:text.y,tw:text.width}}""")
        if width>=900:
            ck(geo["tx"]>=geo["sx"]+geo["sw"]-12,f"not side-by-side {width}: {geo}")
            ck(abs(geo["sy"]-geo["ty"])<140,f"mechanical diagram/readout not aligned {width}: {geo}")
        else:
            ck(geo["ty"]>=geo["sy"]+geo["sh"]-8,f"mobile not stacked {width}: {geo}")
        if width in (390,900,1366):
            page.screenshot(path=str(SHOTS/f"{width}-mechanical-compact.png"),full_page=True,animations="disabled")
    page.set_viewport_size({"width":1366,"height":768})
    page.locator("#mechanicalModelInfo>summary").focus()
    before=page.evaluate("""()=>({a:heartState.physiologicalTime,b:heartState.visualizationTime,
      hr:heartRate,playing:heartState.playing})""")
    page.keyboard.press("Enter")
    ck(page.locator("#mechanicalModelInfo").evaluate("e=>e.open"),"keyboard note not open")
    ck("0.88" in page.locator(".mechanical-model-info-body").inner_text(),"RR modelling caveat lost")
    ck("환자" in page.locator(".mechanical-model-info-body").inner_text(),"patient-related caution lost")
    ck(page.evaluate("""()=>({a:heartState.physiologicalTime,b:heartState.visualizationTime,
      hr:heartRate,playing:heartState.playing})""")==before,"info toggling changed A/B clock")
    page.keyboard.press("Enter")
    ck(not page.locator("#mechanicalModelInfo").evaluate("e=>e.open"),"keyboard note cannot close")
    for hr in (30,80,180):
        page.locator("#heartRateSlider").evaluate("""(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}""",hr)
        page.locator("#timeSlider").evaluate("""e=>{e.value=55;e.dispatchEvent(new Event('input',{bubbles:true}))}""")
        ck("Ready" not in page.locator("#mechanicalPhase").inner_text(),f"Seek mechanical failed HR {hr}")
        ck("혈류:" in page.locator("#flowState").inner_text(),f"Flow label missing HR {hr}")
    page.locator("#playBtn").click()
    page.wait_for_timeout(200)
    ck(page.evaluate("heartState.playing"),"Play failed")
    page.locator("#pauseBtn").click()
    ck(not page.evaluate("heartState.playing"),"Pause failed")
    page.locator("#resetBtn").click()
    ck(page.locator("#mechanicalPhase").inner_text()=="Ready","Mechanical Reset failed")
    page.locator("#dashboardWiggersBtn").click()
    ck(page.locator("#wiggersChart").is_visible(),"Wiggers tab regressed")
    page.locator("#guidedV112Toggle").click()
    ck(page.locator("#guidedV112Assumptions").count()==1,"student modeling note missing")
    ck(not page.locator("#guidedV112Assumptions").evaluate("e=>e.open"),"student modeling note expanded automatically")
    page.locator("#guidedV112Select").select_option("filling")
    page.locator("#guidedV112Assumptions>summary").click()
    ck("RR" in page.locator("#guidedV112Limits").inner_text(),"original filling note lost")
    ck(page.locator("#guidedV112Quiz").count()==1,"quizzes lost")
    ck(page.evaluate("""()=>['atrial_systole','isovolumetric_contraction','ejection','isovolumetric_relaxation','filling'].every(s=>['basic','advanced'].every(l=>CardiacGuidedQuestions.get(s,l)?.explanation?.length>12))"""),"ten questions lost")
    ck(not errs,f"JavaScript errors {errs}")
    b.close()
print(f"PASS {n} Patch13 mechanics info/side-by-side regression")
