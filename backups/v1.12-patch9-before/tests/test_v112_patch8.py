"""Patch 8 guided-only automatic observation and stable reading during playback."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
STAGES=("atrial_systole","isovolumetric_contraction","ejection","isovolumetric_relaxation","filling")
checks=0
def ck(condition,message):
    global checks
    assert condition,message
    checks+=1
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    page=browser.new_page(viewport={"width":1366,"height":768})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    page.evaluate("""() => {window.__p8Events=0;document.getElementById('timeSlider')
      .addEventListener('input',()=>{window.__p8Events++})}""")
    before=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    page.locator("#guidedV112Toggle").click()
    ck(page.evaluate("heartState.physiologicalTime")==before["a"],"Course entry implicitly sought")
    ck(page.evaluate("heartState.visualizationTime")==before["b"],"Course entry changed B")
    last="atrial_systole"
    for hr in (30,50,59,60,72,80,100,101,120,180):
        page.locator("#heartRateSlider").evaluate("""(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}""",hr)
        for stage in STAGES:
            beforeEvents=page.evaluate("window.__p8Events")
            page.locator("#guidedV112Select").select_option(stage)
            actual=page.evaluate("""() => ({
                events:window.__p8Events,playing:heartState.playing,
                rr:getActiveTiming().rr,phase:getPhysiologicalCyclePhase(),
                a:heartState.physiologicalTime,b:heartState.visualizationTime,
                stage:CardiacMechanical.currentState?.stage
            })""")
            change=stage!=last
            ck(actual["events"]==beforeEvents+(1 if change else 0),f"seek count {hr}/{stage}/{actual}")
            if change:
                ck(actual["stage"]==stage,f"wrong guided observation {hr}/{stage}: {actual}")
                ck(not actual["playing"],f"not paused {hr}/{stage}")
                ck(abs(actual["a"]/actual["rr"]-actual["b"]/(60000/72))<.0012,
                    f"A/B phase mismatch {hr}/{stage}")
            last=stage
    page.locator("#guidedV112Select").select_option("ejection")
    chosen=page.locator("#guidedV112Gist").inner_text()
    title=page.locator("#guidedV112Title").inner_text()
    cnt=page.evaluate("window.__p8Events")
    page.locator("#guidedV112Level").select_option("intermediate")
    ck(page.evaluate("window.__p8Events")==cnt,"level switched model time")
    page.locator("#playBtn").click()
    page.wait_for_timeout(1100)
    ck(page.evaluate("heartState.playing"),"Play broken in guided mode")
    ck(page.locator("#guidedV112Gist").inner_text()==chosen,"chosen reading changed during Play")
    ck(page.locator("#guidedV112Title").inner_text()==title,"stage title auto-followed live playback")
    page.locator("#guidedV112Next").click()
    ck(not page.evaluate("heartState.playing"),"next did not Pause")
    ck(page.evaluate("window.__p8Events")==cnt+1,"next did not issue one native seek")
    nextStage=page.evaluate("CardiacGuidedLearning.selectedStageId")
    ck(nextStage=="isovolumetric_relaxation",f"next stage wrong {nextStage}")
    ck(page.evaluate("CardiacMechanical.currentState.stage")==nextStage,"mechanical seek out of sync")
    count=page.evaluate("window.__p8Events")
    page.locator("#guidedV112Toggle").click()
    ck(page.evaluate("window.__p8Events")==count,"course exit changed time")
    page.locator("#playBtn").click()
    page.wait_for_timeout(100)
    page.locator("#dashboardWiggersBtn").click()
    ck(page.evaluate("heartState.playing"),"free observation Wiggers switch paused")
    ck(page.evaluate("window.__p8Events")==count,"free view switched Timeline")
    page.locator("#pauseBtn").click()
    ck(not errors,f"Javascript: {errors}")
    browser.close()
print(f"PASS {checks} Patch8 guided navigation/reading assertions")
