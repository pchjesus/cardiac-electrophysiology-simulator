"""Patch 9: complete source-category and guided workbench acceptance."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/"preview-v112p9"
SHOTS.mkdir(exist_ok=True)
checks=0
def ck(v,m):
    global checks
    assert v,m
    checks+=1

with sync_playwright() as pw:
    browser=pw.chromium.launch()
    page=browser.new_page(viewport={"width":1366,"height":768})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    page.wait_for_function('window.CardiacGuidedLearning?.version==="v1.12 Patch 9"')
    ck("Patch 9" in page.locator("h1").inner_text(),"version wrong")
    ck(page.locator("#dashboardResources").count()==1,"missing index")
    ck(page.locator("#ecgCanvas").count()==1,"duplicate ECG")
    ck(page.locator("#wiggersDeepDive").count()==1,"missing nursing long form")
    ck(page.locator("#dashboardDensityBtn").get_attribute("aria-controls")=="dashboardResources",
        "header controls wrong section")
    ck(not page.locator("#dashboardResources").evaluate("e=>e.open"),"resources unexpectedly open")
    ck(page.locator("#dashboardDensityBtn").inner_text()=="자료 목록 보기","bulk-info label retained")
    ck(page.locator("#userGuidePanel").inner_text().find("자동 Pause")>=0,
        "current guided automatic seek missing from help")

    pos=page.evaluate("""()=>{
      const rect=q=>{const b=document.querySelector(q).getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height}};
      return {ecg:rect('.dashboard-v111>.ecg-panel'),
          heart:rect('.dashboard-v111>.dashboard-workspace'),
          inspector:rect('.dashboard-v111>.dashboard-inspector')}
    }""")
    ck(abs(pos["ecg"]["y"]-pos["inspector"]["y"])<10,"ECG/study start not aligned")
    ck(abs(pos["ecg"]["x"]-pos["heart"]["x"])<10,"ECG and heart not aligned left")
    ck(pos["heart"]["y"]>=pos["ecg"]["y"]+pos["ecg"]["h"],
       "Heart visual overlaps the ECG")
    ck(pos["heart"]["y"]-(pos["ecg"]["y"]+pos["ecg"]["h"])<35,
       f"Large blank gap below ECG: {pos}")
    page.screenshot(path=str(SHOTS/"01-default-desktop-1366.png"),
                    full_page=True,animations="disabled")
    state=page.evaluate("""()=>({
      a:heartState.physiologicalTime,b:heartState.visualizationTime,
      cycle:heartState.cycleStartTime,playing:heartState.playing,
      hr:heartRate,view:CardiacDashboard.view
    })""")
    page.locator("#dashboardDensityBtn").click()
    page.wait_for_function("document.getElementById('dashboardResources').open")
    ck(page.evaluate("CardiacDashboard.density")=="expanded","index state not expanded")
    ck(page.locator("#dashboardDensityBtn").get_attribute("aria-expanded")=="true","header aria stale")
    ck(page.locator("#dashboardDensityBtn").get_attribute("aria-pressed")=="true","header pressed stale")
    for sel in (".dashboard-phase-details",".dashboard-event-details","#wiggersDeepDive"):
        ck(not page.locator(sel).evaluate("e=>e.open"),f"forced source opened {sel}")
    ck(page.locator("#dashboardResources .dashboard-resources-hint").is_visible(),
        "categorized reading hint missing")
    ck(page.evaluate("""()=>Array.from(document.querySelectorAll(
      '#dashboardResources .dashboard-disclosure')).length""")==2,"original phase/event panels lost")

    page.locator(".dashboard-phase-details>summary").click()
    ck(page.locator("#phaseDescription").is_visible(),"phase description unavailable")
    page.locator(".dashboard-event-details>summary").click()
    ck(page.locator("#eventSyncStatus").is_visible(),"ECG event detail unavailable")
    page.locator("#wiggersDeepDive summary").click()
    ck(page.locator("#learningNursing").is_visible(),"six-part nursing unavailable")
    ck(len(page.locator("#learningNursing").inner_text())>70,
       "clinical source was shortened or deleted")
    page.screenshot(path=str(SHOTS/"02-selected-source-desktop-1366.png"),
                    full_page=True,animations="disabled")
    ck(page.evaluate("""()=>({
      a:heartState.physiologicalTime,b:heartState.visualizationTime,
      cycle:heartState.cycleStartTime,playing:heartState.playing,
      hr:heartRate,view:CardiacDashboard.view
    })""")==state,"source navigation moved A/B")

    page.locator("#dashboardDensityBtn").click()
    page.wait_for_function("!document.getElementById('dashboardResources').open")
    ck(page.evaluate("CardiacDashboard.density")=="compact","compact not restored")
    ck(not page.locator(".dashboard-phase-details").evaluate("e=>e.open"),"phase not folded")
    ck(not page.locator(".dashboard-event-details").evaluate("e=>e.open"),"event not folded")
    ck(page.locator("#wiggersDeepDive").evaluate("e=>e.open"),"nursing preference lost")
    ck(page.locator("#dashboardDensityBtn").get_attribute("aria-expanded")=="false",
        "collapsed header aria stale")
    # Native summary must also synchronize the external menu/button.
    page.locator("#dashboardResources>summary").focus()
    page.keyboard.press("Enter")
    page.wait_for_function("document.getElementById('dashboardResources').open")
    page.wait_for_function("document.getElementById('dashboardDensityBtn').getAttribute('aria-pressed')==='true'")
    ck(page.locator("#dashboardDensityBtn").get_attribute("aria-pressed")=="true",
        "keyboard resource open not reflected in header")
    page.keyboard.press("Enter")
    page.wait_for_function("!document.getElementById('dashboardResources').open")
    page.wait_for_function("document.getElementById('dashboardDensityBtn').getAttribute('aria-pressed')==='false'")
    ck(page.locator("#dashboardDensityBtn").get_attribute("aria-pressed")=="false",
        "keyboard resource close not reflected in header")
    ck(page.evaluate("""()=>({
      a:heartState.physiologicalTime,b:heartState.visualizationTime,
      cycle:heartState.cycleStartTime,playing:heartState.playing,
      hr:heartRate,view:CardiacDashboard.view
    })""")==state,"native source toggle mutated simulation")

    page.locator("[data-ecg-component='QRS']").click()
    ck(page.locator(".dashboard-ecg-details").evaluate("e=>e.open"),
       "manual QRS explanation lost")
    ck("QRS" in page.locator("#ecgExplanationTitle").inner_text(),
       "QRS explanation inaccurate")
    page.locator("#guidedV112Toggle").click()
    ck(page.locator("#guidedV112Panel").is_visible(),"guided mode unavailable")
    for st in ("atrial_systole","isovolumetric_contraction","ejection","isovolumetric_relaxation","filling"):
        page.locator("#guidedV112Select").select_option(st)
        ck(page.evaluate("CardiacGuidedLearning.selectedStageId")==st,f"study stage lost {st}")
        ck(page.evaluate("CardiacMechanical.currentState.stage")==st,f"guided observation mismatch {st}")
        ck(not page.evaluate("heartState.playing"),f"guided observation not paused {st}")
        for level in ("basic","advanced"):
            q=page.evaluate("""(args)=>CardiacGuidedQuestions.get(args[0],args[1])""",[st,level])
            ck(bool(q and len(q["options"])==3 and q["explanation"]),f"quiz bank lost {st}/{level}")
    guidedPos=page.evaluate("""()=>{
      const a=document.querySelector('.dashboard-v111>.ecg-panel').getBoundingClientRect();
      const b=document.querySelector('.dashboard-v111>.dashboard-workspace').getBoundingClientRect();
      return {gap:b.top-a.bottom,alignment:b.x-a.x}
    }""")
    ck(guidedPos["gap"]<35 and abs(guidedPos["alignment"])<10,
       f"Guided lessons left huge empty ECG area: {guidedPos}")
    page.locator("#guidedV112Level").select_option("advanced")
    page.locator("#guidedV112Advanced summary").click()
    for st in ("atrial_systole","ejection","filling"):
        page.locator("#guidedV112Select").select_option(st)
        for field,key in (("Electrical","electrical"),("Hemodynamics","hemodynamics"),
                          ("Volume","volume"),("Nursing","nursing"),("Caution","caution"),
                          ("Comparison","comparison")):
            expected=page.evaluate("""(s)=>CardiacLearning.getStageNarrative(s[0])[s[1]]""",[st,key])
            ck(page.locator("#guidedV112Full"+field).inner_text()==expected,
               f"original six-part source changed {st}/{field}")
    page.locator("#guidedV112Quiz summary").click()
    ck(page.locator("#guidedV112BasicQuestion").is_visible(),"basic question inaccessible")
    ck(page.locator("#guidedV112AdvancedQuestion").is_visible(),"advanced question inaccessible")
    page.screenshot(path=str(SHOTS/"03-guided-advanced-desktop-1366.png"),
                    full_page=True,animations="disabled")
    page.locator("#guidedV112Level").select_option("basic")
    gist=page.locator("#guidedV112Gist").inner_text()
    page.locator("#playBtn").click()
    page.wait_for_timeout(900)
    ck(page.evaluate("heartState.playing"),"Play broken")
    ck(page.locator("#guidedV112Gist").inner_text()==gist,"reading changed with fast HR")
    page.locator("#pauseBtn").click()
    for width in (360,390,768,1024,1366,1440):
        page.set_viewport_size({"width":width,"height":800})
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           f"global horizontal overflow at {width}")
        ck(page.locator("#guidedV112Gist").is_visible(),
           f"guided text missing {width}")
        ck(page.locator("#ecgCanvas").is_visible(),f"ECG hidden {width}")
        if width in (360,390):
            page.screenshot(path=str(SHOTS/f"04-guided-mobile-{width}.png"),
                            full_page=True,animations="disabled")
    page.locator("#guidedV112Toggle").click()
    page.locator("#dashboardWiggersBtn").click()
    ck(page.locator("#wiggersChart").is_visible(),"Wiggers lost")
    ck(page.locator("#wiggersMarkers [data-event]").count()==4,"valve events lost")
    page.locator("#resetBtn").click()
    ck(page.evaluate("CardiacDashboard.isReady"),"Reset not ready")
    ck(not errors,f"Javascript errors {errors}")
    browser.close()
print(f"PASS {checks} Patch 9 source/category/UX checks; 5 screenshots")
