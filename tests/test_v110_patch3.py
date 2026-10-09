"""v1.10 Patch 3: native disclosure, SVG, A-clock sync, regression + mobile."""
from pathlib import Path
import math
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"backups"/"v1.9"/"FINAL"
checks=0

def ck(value,msg):
    global checks
    checks+=1
    assert value,msg

def install(page, folder, new):
    page.set_content((folder/"index.html").read_text(encoding="utf-8"))
    page.add_style_tag(content=(folder/"style.css").read_text(encoding="utf-8"))
    files=["script.js","mechanics.js"]
    if new:
        files+=["wiggers.js","wiggers-profile.js","wiggers-view.js"]
    for filename in files:
        page.add_script_tag(content=(folder/filename).read_text(encoding="utf-8"))

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path="/usr/bin/chromium",
        args=["--no-sandbox","--disable-dev-shm-usage"])
    page=browser.new_page(viewport={"width":1366,"height":900})
    old=browser.new_page(viewport={"width":1366,"height":900})
    errors={"current":[],"baseline":[]}
    page.on("pageerror",lambda e:errors["current"].append(str(e)))
    old.on("pageerror",lambda e:errors["baseline"].append(str(e)))
    install(page,ROOT,True)
    install(old,BASE,False)
    view="window.CardiacWiggersView"
    ck(page.evaluate(f"typeof {view}?.sync")== "function","View adapter missing")
    ck(page.locator("#wiggersDetails").count()==1,"Wiggers details missing")
    ck(not page.evaluate("document.getElementById('wiggersDetails').open"),
       "Wiggers must be collapsed by default")
    ck(page.locator("#wiggersChart").is_hidden(),"Chart visible while collapsed")
    ck(page.evaluate(f"{view}.buildCount")==0,"Chart built while collapsed")
    ck(page.locator("#heartSVG").is_visible(),"Legacy Electrical view not visible")
    ck(not page.locator("#mechanicalView").is_visible(),"Mechanical view unexpectedly visible")
    ck(page.locator("#timeSlider").count()==1 and
       page.locator("#heartRateSlider").count()==1,
       "Existing controls duplicated")
    ck(page.evaluate("document.querySelectorAll('#wiggersChart').length")==1,
       "Chart ID duplicated")
    # Native details: Enter toggles; focus is visible/keyboard-compatible.
    page.locator("#wiggersToggle").focus()
    page.keyboard.press("Enter")
    page.wait_for_function("document.getElementById('wiggersDetails').open")
    ck(page.locator("#wiggersChart").is_visible(),"Keyboard disclosure does not show chart")
    ck(page.evaluate(f"{view}.buildCount")==1,"Chart failed to build on first open")
    ck(page.locator("#wiggersMarkers [data-event]").count()==4,
       "Expected four separate valve event markers")
    ck(page.locator("#wiggersMarkers title").count()==4,
       "SVG event titles missing")
    ck(page.locator("#wiggersCurrentTime").text_content().startswith(
       "Physiological phase"),"A-clock status missing")
    ck("not mmHg" in page.locator(".wiggers-disclaimer").text_content() or
       "not mmHg" in page.locator(".wiggers-disclaimer").text_content().lower(),
       "Nonclinical unit disclaimer missing")
    ck("S1" in page.locator(".wiggers-event-key").text_content() and
       "S2" in page.locator(".wiggers-event-key").text_content(),
       "Sound markers not visible in legend")

    # Validate geometry is backed directly by the same active ECG and Patch 2
    # profiles, not a disconnected cartoon or B presentation time.
    geometry_js="""() => {
        const ids=['wiggersPathECG','wiggersPathLA','wiggersPathLV',
                   'wiggersPathAorta','wiggersPathVolume'];
        const timing=getActiveTiming(),sample=128,at=sample/480*timing.rr;
        const snap=window.CardiacWiggersProfile.getSnapshot(at,timing);
        const curves=ids.map(id=>{
            const text=document.getElementById(id).getAttribute('d');
            const pair=text.split('L')[sample].replace(/^M/,'').trim().split(/\\s+/);
            return {id,x:Number(pair[0]),y:Number(pair[1]),count:text.split('L').length};
        });
        return {
            sample, phase:at,curve:curves,
            expected:[
                267-ecgValue(at,timing)*.37,
                200-1.23*snap.pressure.leftAtrial,
                200-1.23*snap.pressure.leftVentricular,
                200-1.23*snap.pressure.aortic,
                408-(snap.ventricularVolume.relativeValue-.45)*132
            ],
            markers:window.CardiacWiggersProfile.getSnapshot(0,timing)
                .valveEvents.map(e=>e.id),
            actualMarkers:[...document.querySelectorAll('#wiggersMarkers [data-event]')]
                .map(n=>n.dataset.event)
        };
    }"""
    for hr in (30,33,50,59,72,80,100,120,150,180):
        page.locator("#heartRateSlider").evaluate(
            """(el,hr)=>{el.value=hr;el.dispatchEvent(new Event('input',{bubbles:true}));}""",hr)
        info=page.evaluate(geometry_js)
        for i,item in enumerate(info["curve"]):
            ck(item["count"]==481,f"Curves not sampled at 481 points HR={hr}: {item['id']}")
            ck(abs(item["y"]-info["expected"][i])<=.012,
               f"SVG trace differs from source profile HR={hr} curve={item['id']}")
            ck(abs(item["x"]-(64+891*info["sample"]/480))<.012,
               f"Incorrect physiological x at HR={hr}")
        ck(info["actualMarkers"]==info["markers"],f"Valve marker mismatch HR={hr}")
        ck(page.locator("#wiggersCurrentTime").text_content().endswith(f"{hr} bpm"),
           f"HR not applied to graph legend: {hr}")
        drawn=page.evaluate(f"{view}.buildCount")
        page.evaluate(f"{view}.sync();{view}.sync();{view}.sync();")
        ck(page.evaluate(f"{view}.buildCount")==drawn,
           "Graph rebuilt unnecessarily on unchanged HR")
        # Timeline seek pauses animation and should update the SAME cursor.
        for percent in (0,8,34,67,99.5,100):
            page.locator("#timeSlider").evaluate("""(el,n)=>{
               el.value=n;el.dispatchEvent(new Event('input',{bubbles:true}));
            }""",percent)
            result=page.evaluate("""() => {
                const line=document.getElementById('wiggersCursor');
                const rr=getActiveTiming().rr;
                const phase=window.CardiacWiggersView.currentPhaseMs;
                return {actual:Number(line.getAttribute('x1')),
                        expected:64+891*phase/rr,playing:heartState.playing,
                        phase:phase, A:getPhysiologicalCyclePhase(),rr};
            }""")
            ck(abs(result["actual"]-result["expected"])<.015,
               f"Cursor out of sync after seek HR={hr} percent={percent}")
            ck(abs(result["phase"]-result["A"])<1e-5,
               f"Cursor uses wrong clock HR={hr} percent={percent}")
            ck(not result["playing"],"Timeline seek did not pause")

    # Closing the panel stops all graph DOM updates and rendering. It does not
    # alter simulation/playback/model state or the selected heart mode.
    before_close=page.evaluate(f"{view}.buildCount")
    page.locator("#wiggersToggle").focus()
    page.keyboard.press("Enter")
    page.wait_for_function("!document.getElementById('wiggersDetails').open")
    ck(page.locator("#wiggersChart").is_hidden(),"Chart failed to collapse")
    page.locator("#heartRateSlider").evaluate("""el=>{
        el.value=65;el.dispatchEvent(new Event('input',{bubbles:true}));
    }""")
    page.evaluate("updateSimulation(23)")
    ck(page.evaluate(f"{view}.buildCount")==before_close,
       "Collapsed diagram recomputed trace")
    ck(page.evaluate("!document.getElementById('wiggersDetails').open"),
       "Collapsed diagram reopened by simulation updates")
    page.locator("#wiggersToggle").click()
    page.wait_for_function("document.getElementById('wiggersDetails').open")
    # <details> 'toggle' is queued asynchronously after 'open' flips.
    # Assert redraw after the browser has dispatched that event.
    page.wait_for_function(
        "(count) => window.CardiacWiggersView.buildCount > count",
        arg=before_close)
    ck(page.evaluate(f"{view}.buildCount")==before_close+1,
       "Reopen failed to apply changed HR")
    ck("65 bpm" in page.locator("#wiggersCurrentTime").text_content(),
       "Reopened panel did not show updated HR")

    # Playback uses existing requestAnimationFrame; Pause and Reset must not
    # trigger a new hidden ticker, change mode or collapse the user preference.
    page.locator("#mechanicalModeBtn").click()
    ck(page.locator("#mechanicalView").is_visible(),"Mechanical mode broken")
    ck(page.locator("#wiggersChart").is_visible(),"Mechanical hides Wiggers")
    page.locator("#resetBtn").click()
    ck(page.evaluate("document.getElementById('wiggersDetails').open"),
       "Reset unexpectedly collapsed optional panel")
    ck(page.locator("#wiggersCurrentStage").text_content()=="Ready",
       "Ready status not restored")
    ck(page.locator("#mechanicalPhase").text_content()=="Ready",
       "Mechanical reset regression")
    ck(abs(float(page.locator("#wiggersCursor").get_attribute("x1"))-64)<.01,
       "Reset should put cursor at cycle start")
    page.locator("#playBtn").click()
    page.wait_for_timeout(240)
    page.locator("#pauseBtn").click()
    time_after=page.evaluate("heartState.physiologicalTime")
    ck(time_after>0,"Play did not advance physiological time")
    ck(not page.evaluate("heartState.playing"),"Pause failed")
    recorded=page.locator("#wiggersCursor").get_attribute("x1")
    page.wait_for_timeout(100)
    ck(recorded==page.locator("#wiggersCursor").get_attribute("x1"),
       "Wiggers cursor moved after pause")
    page.locator("#electricalModeBtn").click()
    ck(page.locator("#heartSVG").is_visible(),"Electrical view not restored")

    # Exact v1.9 comparison while optional view is OPEN: moving around the
    # original ECG and Mechanical state must remain functionally identical.
    for hr in (30,72,80,120,180):
        for tab in (page,old):
            tab.locator("#heartRateSlider").evaluate(
                """(el,hr)=>{el.value=hr;el.dispatchEvent(new Event('input',{bubbles:true}));}""",hr)
        for percent in (0,13,55,90,100):
            for tab in (page,old):
                tab.locator("#timeSlider").evaluate(
                    """(el,v)=>{el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));}""",percent)
                tab.evaluate("updateSimulation(19)")
            model="""() => ({
                A:heartState.physiologicalTime,B:heartState.visualizationTime,
                cycleStart:heartState.cycleStartTime,sweep:heartState.sweepPosition,
                speed:animationSpeed,step:heartState.currentStep,
                event:heartState.currentECGEvent,
                ECG:getECGMeasurements(),
                mechanical:window.CardiacMechanical.getMechanicalState(
                    getPhysiologicalCyclePhase()),
                samples:[0,10,75,130,200,270].map(x=>ecgValue(x))
            })"""
            ck(page.evaluate(model)==old.evaluate(model),
               f"v1.9 A/B ECG/Mechanical regression HR={hr} seek={percent}")

    # Wide and narrow: only Wiggers has its own horizontal scroll, no added
    # document-level width beyond inherited 437px from the v1.9 baseline.
    for width in (1366,768,390,360):
        page.set_viewport_size({"width":width,"height":900})
        old.set_viewport_size({"width":width,"height":900})
        page.evaluate(f"{view}.sync()")
        overall=page.evaluate("document.documentElement.scrollWidth")
        original=old.evaluate("document.documentElement.scrollWidth")
        ck(overall<=original+1,
           f"Added Wiggers caused document overflow viewport={width}: {overall}>{original}")
        if width<=390:
            ck(page.evaluate("""() => {
                const area=document.querySelector('.wiggers-chart-scroll');
                return area.scrollWidth>area.clientWidth && area.clientWidth<=innerWidth+50;
            }"""),f"Mobile Wiggers not locally horizontally scrollable at {width}")
    ck(errors=={"current":[],"baseline":[]},
       f"JS errors in browser={errors}")

    # Avoid claiming validation of synthetic numeric physiology by this test.
    print(f"PASS {checks} v1.10 Patch 3 checks: native keyboard disclosure, "
          "481-point source-linked SVG traces, valve markers, A-time cursor, "
          "HR/seek/play/pause/reset, Mechanical/Electrical, inherited mobile "
          f"overflow. JS errors={errors}")
    browser.close()
