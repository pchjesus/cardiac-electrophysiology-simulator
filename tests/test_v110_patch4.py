"""v1.10 Patch 4 browser checks: help popover and event-sourced education."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
count=0
def check(ok,msg):
    global count
    count+=1
    assert ok,msg

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path="/usr/bin/chromium",
        args=["--no-sandbox","--disable-dev-shm-usage"])
    page=browser.new_page(viewport={"width":1366,"height":900})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.set_content((ROOT/"index.html").read_text(encoding="utf-8"))
    page.add_style_tag(content=(ROOT/"style.css").read_text(encoding="utf-8"))
    for f in ("script.js","mechanics.js","wiggers.js","wiggers-profile.js",
              "wiggers-view.js","wiggers-help.js"):
        page.add_script_tag(content=(ROOT/f).read_text(encoding="utf-8"))
    details=page.locator("#wiggersDetails")
    help=page.locator("#wiggersHelpButton")
    popup=page.locator("#wiggersHelp")
    close=page.locator("#wiggersHelpClose")
    check(not details.evaluate("(e)=>e.open"),"Disclosure initially expanded")
    check(popup.is_hidden(),"Help initially open")
    check(help.evaluate("(e)=>!e.closest('summary')"),"Help nested in native summary")
    saved=page.evaluate("""() => ({
       playing:heartState.playing,A:heartState.physiologicalTime,
       B:heartState.visualizationTime,mode:CardiacMechanical.mode
    })""")
    help.focus()
    page.keyboard.press("Enter")
    check(popup.is_visible(),"Enter did not open help")
    check(help.get_attribute("aria-expanded")=="true","aria-expanded incorrect")
    check(not details.evaluate("(e)=>e.open"),"Opening help toggled disclosure")
    check(close.evaluate("(e)=>document.activeElement===e"),"Focus did not enter help")
    check(saved==page.evaluate("""() => ({
       playing:heartState.playing,A:heartState.physiologicalTime,
       B:heartState.visualizationTime,mode:CardiacMechanical.mode
    })"""),"Opening help mutated simulator")
    popup.locator("li").first.click()
    check(popup.is_visible(),"Internal help click closed popup")
    page.keyboard.press("Escape")
    check(popup.is_hidden(),"Escape failed")
    check(help.evaluate("(e)=>document.activeElement===e"),"Escape did not restore focus")
    for _ in range(3):
        help.click()
        check(popup.is_visible(),"Help repeat opening failed")
        close.click()
        check(popup.is_hidden(),"Close button failed")
        check(help.evaluate("(e)=>document.activeElement===e"),"Close focus lost")
    help.click()
    page.locator("#phaseTitle").click()
    check(popup.is_hidden(),"Click outside did not dismiss")
    help.click()
    # Click the text/marker area, well away from the separately placed ? control.
    page.locator("#wiggersToggle").click(position={"x":12,"y":12})
    check(popup.is_hidden(),"Summary click did not dismiss help")
    page.wait_for_function("document.getElementById('wiggersDetails').open")
    check(details.evaluate("(e)=>e.open"),"Summary click stopped disclosure")
    page.wait_for_function("window.CardiacWiggersView.buildCount > 0")
    check(page.locator("#wiggersMarkers [data-event]").count()==4,"Marker count changed")

    event_map=[
      ("mitral-close","Mitral closes / S1","isovolumetric_contraction",False,False),
      ("aortic-open","Aortic opens","ejection",False,True),
      ("aortic-close","Aortic closes / S2","isovolumetric_relaxation",False,False),
      ("mitral-open","Mitral opens","filling",True,False)
    ]
    stage_words={
      "filling":"Ventricular filling",
      "atrial_systole":"Atrial systole",
      "isovolumetric_contraction":"Isovolumetric contraction",
      "ejection":"Ventricular ejection",
      "isovolumetric_relaxation":"Isovolumetric relaxation"
    }
    for hr in (30,50,80,120,180):
        page.locator("#heartRateSlider").evaluate("""(el,n)=>{
          el.value=n;el.dispatchEvent(new Event('input',{bubbles:true}));
        }""",hr)
        for eid,title,stage,mitral,aortic in event_map:
            actual=page.evaluate("""(id)=>{
              const t=getActiveTiming();
              const ev=CardiacWiggers.getValveEvents(t).find(e=>e.id===id);
              const snap=CardiacWiggersProfile.getSnapshot(ev.timeMs,t);
              heartState.physiologicalTime=ev.timeMs;
              heartState.cycleStartTime=0;
              CardiacWiggersView.sync();
              return {phase:snap.cycle.phaseMs,time:ev.timeMs,stage:snap.mechanical.stage,
                mitral:snap.valves.mitral,aortic:snap.valves.aortic,
                x:Number(document.getElementById('wiggersCursor').getAttribute('x1')),
                expected:64+891*ev.timeMs/t.rr,
                markerTitles:[...document.querySelectorAll('#wiggersMarkers title')].map(x=>x.textContent)};
            }""",eid)
            check(abs(actual["phase"]-actual["time"])<1e-7,f"Event phase HR={hr} {eid}")
            check(actual["stage"]==stage,f"Stage tie HR={hr} {eid}")
            check(actual["mitral"]==mitral and actual["aortic"]==aortic,
                  f"Valve tie HR={hr} {eid}")
            check(abs(actual["x"]-actual["expected"])<.02,f"Cursor HR={hr} {eid}")
            check(page.locator("#wiggersLearningEvent").text_content().startswith("At valve marker: "+title),
                  f"Event interpretation HR={hr} {eid}")
            check(stage_words[stage] in page.locator("#wiggersLearningStage").text_content(),
                  f"Phase explanation HR={hr} {eid}")
            check(any(title in x for x in actual["markerTitles"]),
                  f"Event SVG label HR={hr} {eid}")
        for stage,title in stage_words.items():
            actual=page.evaluate("""stage=>{
              const t=CardiacMechanical.getMechanicalTiming();
              const windows={
               filling:[t.relaxationEnd,t.rr],
               atrial_systole:[t.atrialStart,t.contractionStart],
               isovolumetric_contraction:[t.contractionStart,t.ejectionStart],
               ejection:[t.ejectionStart,t.ejectionEnd],
               isovolumetric_relaxation:[t.ejectionEnd,t.relaxationEnd]
              };
              const [a,b]=windows[stage];
              const phase=(a+b)/2;
              heartState.physiologicalTime=phase;
              heartState.cycleStartTime=0;
              CardiacWiggersView.sync();
              return CardiacWiggersProfile.getSnapshot(phase,getActiveTiming()).mechanical.stage;
            }""",stage)
            check(actual==stage,f"Mid-stage HR={hr} {stage}")
            check(title in page.locator("#wiggersLearningStage").text_content(),
                  f"Mid-stage lesson HR={hr} {stage}")
    help.click()
    page.locator("#resetBtn").click()
    check(popup.is_hidden(),"Outside Reset click did not close nonmodal help")
    check(details.evaluate("(e)=>e.open"),"Reset collapsed Wiggers")
    check(page.locator("#wiggersCurrentStage").text_content()=="Ready","Reset stage")
    check("심장주기 시간축" in page.locator("#wiggersLearningStage").text_content(),
          "Reset lesson stale")
    page.locator("#playBtn").click()
    page.wait_for_timeout(120)
    help.click()
    check(popup.is_visible() and page.evaluate("heartState.playing"),
          "Opening help interrupted running simulation")
    page.wait_for_timeout(100)
    page.locator("#pauseBtn").click()
    check(not page.evaluate("heartState.playing"),"Pause regression")
    check(page.evaluate("heartState.physiologicalTime")>0,"Play regression")
    check(popup.is_hidden(),"Outside Pause click did not dismiss help")
    help.click()
    page.locator("#mechanicalModeBtn").click()
    check(popup.is_hidden(),"Mode click failed to dismiss help")
    check(page.locator("#mechanicalView").is_visible(),"Mechanical mode regression")
    page.locator("#electricalModeBtn").click()
    check(page.locator("#heartSVG").is_visible(),"Electrical mode regression")
    for width in (1366,768,390,360):
        page.set_viewport_size({"width":width,"height":800})
        help.click()
        rect=popup.evaluate("""e=>{
          const r=e.getBoundingClientRect();
          return {left:r.left,right:r.right,w:innerWidth,h:e.clientHeight,vh:innerHeight};
        }""")
        check(rect["left"]>=-1 and rect["right"]<=rect["w"]+1,
              f"Help clipped at width {width}: {rect}")
        check(rect["h"]<rect["vh"],f"Help height not capped at {width}")
        page.keyboard.press("Escape")
        check(popup.is_hidden(),f"Mobile escape {width}")
    check(not errors,f"JS page errors: {errors}")
    print(f"PASS {count} v1.10 Patch 4 checks: independent popover, focus, "
          "model-aligned valve/S1/S2 boundaries across five HRs, stage lessons, "
          "play/pause/reset, modes and four viewports.")
    browser.close()
