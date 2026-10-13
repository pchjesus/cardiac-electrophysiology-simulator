"""Patch 6: ECG seek reconstruction and compact UI stability."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
STAGES=("atrial_systole","isovolumetric_contraction","ejection","isovolumetric_relaxation","filling")
count=0
def ck(ok,msg):
    global count
    assert ok,msg
    count+=1
with sync_playwright() as p:
    b=p.chromium.launch()
    page=b.new_page(viewport={"width":1366,"height":768})
    errs=[]
    page.on("pageerror",lambda e:errs.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    page.locator("#guidedV112Toggle").click()
    for hr in (30,50,59,60,72,80,100,101,120,180):
        page.locator("#heartRateSlider").evaluate("""(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}""",hr)
        for st in STAGES:
            page.locator("#guidedV112Select").select_option(st)
            page.locator("#guidedV112Seek").click()
            result=page.evaluate("""() => {
                const t=getPhysiologicalCyclePhase();
                const last=ecgPoints[ecgPoints.length-1];
                return {playing:heartState.playing,stage:CardiacMechanical.currentState.stage,
                    deviation:Math.abs(last.y-(canvas.height*.58-ecgValue(t))),
                    signal:ecgPoints.filter(pt=>Math.abs(pt.y-canvas.height*.58)>2).length}
            }""")
            ck(not result["playing"],f"Seek playback {hr} {st}")
            ck(result["stage"]==st,f"Stage wrong {hr} {st}: {result}")
            ck(result["deviation"]<1,f"Seek ECG last sample wrong {hr} {st}: {result}")
            ck(result["signal"]>2,f"Seek ECG unexpectedly flat {hr} {st}: {result}")
    page.locator("#guidedV112Toggle").click()
    # Panel-height stability is measured after the Patch 7 workbench reflow.
    page.locator("#playBtn").click()
    page.wait_for_timeout(120)
    ck(page.evaluate("heartState.playing"),"Play regression")
    page.locator("#pauseBtn").click()
    ck(not page.evaluate("heartState.playing"),"Pause regression")
    page.locator("#resetBtn").click()
    ck(page.evaluate("CardiacDashboard.isReady"),"Reset regression")
    ck(not errs,f"Javascript: {errs}")
    b.close()
print(f"PASS {count} Patch6 Seek ECG canvas and stable UI checks")
