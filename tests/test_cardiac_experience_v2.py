"""Cardiac Experience v2: original engine preservation, responsive UX and review screenshots.

This is a browser-level review candidate only; no real-device or clinical approval.
Run with: python tests/test_cardiac_experience_v2.py
"""
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "preview-cardiac-v2"
OUT.mkdir(exist_ok=True)
checks = 0

def ck(condition, message):
    global checks
    checks += 1
    assert condition, message

def physiology(page):
    return page.evaluate("""() => ({
      A:heartState.physiologicalTime, B:heartState.visualizationTime,
      hr:heartRate, playing:heartState.playing,
      timing:getActiveTiming(),
      measures:getECGMeasurements(),
      wave:[0,55,135,280,400,620].map(v=>ecgValue(v)),
      profile:CardiacWiggersProfile.getSnapshot(getPhysiologicalCyclePhase(),getActiveTiming())
    })""")

def checkpoint(page):
    return page.evaluate("""() => ({
      timeA:heartState.physiologicalTime,timeB:heartState.visualizationTime,
      hr:heartRate,playing:heartState.playing,
      learning:CardiacCourseV113.activeUnitId,
      completed:CardiacCourseV113.completedUnitIds,
      clinical:CardiacClinicalV113.sessionSnapshot
    })""")

def set_controls(page, hr, pos):
    page.locator("#heartRateSlider").evaluate(
        "(e,n)=>{e.value=n;e.dispatchEvent(new Event('input',{bubbles:true}));}", hr)
    page.locator("#timeSlider").evaluate(
        "(e,n)=>{e.value=n;e.dispatchEvent(new Event('input',{bubbles:true}));}", pos)

def shot(page, name):
    page.screenshot(path=str(OUT / name), full_page=True, animations="disabled")

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/chromium",
        args=["--no-sandbox","--disable-dev-shm-usage"])
    original = browser.new_page(viewport={"width": 1440, "height": 900})
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("pageerror",lambda e:errors.append(str(e)))
    original.goto((ROOT / "index.html").as_uri())
    page.goto((ROOT / "experience.html").as_uri())
    ck(page.evaluate("!!window.CardiacExperienceV2"), "v2 adapter not loaded")
    ck(page.locator("html").get_attribute("data-cx-error") is None,
        "v2 adapter dependency failure")
    ck(page.locator(".cx-intro-title").is_visible(), "v2 introduction missing")
    ck(page.locator(".cx-trace").is_visible(), "ECG experience not present")
    ck(page.locator(".cx-control").is_visible(), "native transport not present")
    ck(page.locator(".cx-compare-grid").is_visible(), "paired interpretation not present")
    ck(page.locator(".cx-primary-nav").is_visible(), "original route navigation missing")
    ck(page.locator("#v113TabClinical").is_disabled(), "unreviewed clinical case publicly exposed")
    ck(page.locator(".v113-preview-screen:not([hidden])").count()==0,
        "clinical/learning preview unexpectedly open")
    for id in ("ecgCanvas","heartSVG","mechanicalSVG","wiggersChart",
               "playBtn","pauseBtn","resetBtn","timeSlider","heartRateSlider",
               "guidedV112Panel","v113TabSimulator","v113TabLearning",
               "v113TabClinical","dashboardWiggersBtn"):
        ck(page.locator("#"+id).count()==1, "original node lost/duplicated: "+id)
    ck(page.locator("#ecgCanvas").is_visible(), "ECG Canvas not visibly rehomed")
    ck(page.locator("#heartSVG").is_visible(), "heart conduction SVG hidden")
    ck(page.locator('[data-term-help="ecg"]:visible').count()==1,
       "ECG concept helper hidden after redesign")
    ck(page.locator('[data-term-help="measurements"]:visible').count()==1,
       "measurements concept helper hidden after redesign")
    ck(page.locator("#dashboardDensityBtn").count()==1,
       "resources control should reuse original node")

    # Presentation-only work has to be numerically identical to the original page.
    for hr in (30,50,72,80,100,120,180):
        for seek in (0,18,52,91):
            set_controls(original,hr,seek)
            set_controls(page,hr,seek)
            ck(physiology(page)==physiology(original),
               f"original A/B/model/measurements differed: HR {hr}, seek {seek}")
    for q in ("P","PR","QRS","ST","T"):
        page.locator('[data-ecg-component="'+q+'"]').click()
        ck(page.locator("#ecgExplanationTitle").text_content().strip()!="",
           "ECG description click broken: "+q)
    page.locator("#resetBtn").click()
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0&&!heartState.playing"),
       "canonical Reset no longer restores A/B")
    ck(page.locator("#heartRateSlider").input_value()=="180",
       "Reset must preserve the user-selected HR, not silently set a default")

    # Visual selections must not seek either clock or change HR.
    before=checkpoint(page)
    page.locator("#mechanicalModeBtn").click()
    ck(page.locator("#mechanicalView").is_visible(),"native Mechanical view hidden")
    ck(checkpoint(page)==before, "Mechanical view changed physics/study session")
    page.locator("#dashboardWiggersBtn").click()
    ck(page.locator("#wiggersChart").is_visible(),"Wiggers chart not visible")
    ck(checkpoint(page)==before, "Wiggers view changed clocks/study/clinical state")
    ck(page.locator("#wiggersDetails").evaluate("(e)=>e.open"),"Wiggers details closed")
    shot(page, "02-desktop-wiggers.png")
    page.locator("#electricalModeBtn").click()
    ck(page.locator("#heartSVG").is_visible(),"return to Electrical broken")
    ck(checkpoint(page)==before, "Electrical view changed clocks")

    page.locator("#playBtn").click()
    page.wait_for_timeout(180)
    page.locator("#pauseBtn").click()
    ck(page.evaluate("!heartState.playing&&heartState.physiologicalTime>0&&heartState.visualizationTime>0"),
       "native play/pause did not advance and stop A/B")
    paused=checkpoint(page)
    page.locator("#v113TabLearning").click()
    ck(page.locator("#v113LearningScreen").is_visible(), "Learning tab not activated")
    ck(page.locator("#v113LearningScreen .cx-screen-lead").is_visible(), "Learning entrance not redesigned")
    ck(page.locator(".v113-unit-title").is_visible(),"six-unit reading unavailable")
    ck(checkpoint(page)==paused, "tab switch changed paused clock or sessions")
    ck(page.evaluate("CardiacCourseV113.unitIds.length") == 6, "six units no longer present")
    page.locator(".v113-unit-button").nth(2).click()
    ck(page.evaluate("CardiacCourseV113.activeUnitId") == "unit-ecg-timing",
       "course selection no longer works")
    ck(checkpoint(page)["timeA"] == paused["timeA"], "course unit selection sought Timeline")
    page.locator(".v113-unit-button").first.click()
    ck(page.locator("#guidedV112Toggle").count()==1, "canonical Guided trigger duplicated")
    ck(page.locator("#guidedV112Panel").count()==1, "canonical Guided panel duplicated")
    shot(page, "03-desktop-learning.png")
    page.locator("#v113TabSimulator").click()
    ck(page.locator("#ecgCanvas").is_visible(),"return to Simulator hid ECG")
    ck(page.evaluate("!heartState.playing"),"tab return auto-played")
    page.locator("#resetBtn").click()
    shot(page, "01-desktop-simulator.png")

    # Review original source notes, term dialog and original keyboard dismissal.
    term=page.locator('[data-term-help="ecg"]:visible')
    term.click()
    ck(page.locator("#v113TermDialog").is_visible(),"concept dialog broken")
    page.keyboard.press("Escape")
    ck(page.locator("#v113TermDialog").is_hidden(),"Escape did not dismiss concept dialog")
    ck(term.evaluate("e=>document.activeElement===e"),"term dialog did not restore focus")

    for width in (320,360,390,540,768,1024,1440):
        page.set_viewport_size({"width":width,"height":900})
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           "document horizontal overflow "+str(width))
        ck(page.locator("#ecgCanvas").is_visible(), "ECG hidden at "+str(width))
        ck(page.locator("#timeSlider").is_visible(),"native Timeline hidden "+str(width))
        page.locator("#dashboardWiggersBtn").click()
        ck(page.locator("#wiggersChart").is_visible(),"Wiggers hidden at "+str(width))
        if width<=540:
            ck(page.locator(".wiggers-chart-scroll").evaluate(
               "e=>e.scrollWidth>e.clientWidth"),"Wiggers mobile horizontal exploration lost")
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           "Wiggers made entire document overflow "+str(width))
        page.locator("#electricalModeBtn").click()
    # Prefer-reduced-motion affects decoration, not the physiological render.
    page.emulate_media(reduced_motion="reduce")
    page.locator("#v113TabLearning").click()
    ck(page.locator("#v113LearningScreen .cx-screen-lead").is_visible(),"reduced-motion hides Learning")
    ck(page.locator("#v113LearningScreen").evaluate(
        "e=>getComputedStyle(e).animationDuration") in ("1e-05s","0s","0.00001s"),
        "reduced-motion entrance still animates")
    page.locator("#v113TabSimulator").click()
    page.emulate_media(reduced_motion="no-preference")
    page.set_viewport_size({"width":390,"height":844})
    # Touch-only heart graphic gesture selects the adjacent *native* view.
    # It must never touch A/B time, and the graph retains native horizontal scroll.
    before_swipe=checkpoint(page)
    page.locator("#heartSVG").evaluate("""e=>{
      e.dispatchEvent(new PointerEvent('pointerdown',{pointerId:15,pointerType:'touch',clientX:280,clientY:160,bubbles:true}));
      e.dispatchEvent(new PointerEvent('pointerup',{pointerId:15,pointerType:'touch',clientX:100,clientY:158,bubbles:true}));
    }""")
    ck(page.evaluate("CardiacDashboard.view")=="mechanical","heart swipe did not select Mechanical")
    ck(checkpoint(page)==before_swipe,"touch view swipe changed A/B, HR or session")
    page.locator("#mechanicalSVG").evaluate("""e=>{
      e.dispatchEvent(new PointerEvent('pointerdown',{pointerId:16,pointerType:'touch',clientX:280,clientY:160,bubbles:true}));
      e.dispatchEvent(new PointerEvent('pointerup',{pointerId:16,pointerType:'touch',clientX:100,clientY:158,bubbles:true}));
    }""")
    ck(page.evaluate("CardiacDashboard.view")=="wiggers","mechanical swipe did not select Wiggers")
    ck(checkpoint(page)==before_swipe,"second touch view swipe mutated A/B or study state")
    page.locator("#electricalModeBtn").click()
    shot(page,"04-mobile-simulator.png")
    page.locator("#v113TabLearning").click()
    shot(page,"05-mobile-learning.png")

    # In a separate QA-enabled visit, check the clinical gate and original session.
    qa=browser.new_page(viewport={"width":1440,"height":900})
    qa_errors=[]
    qa.on("pageerror",lambda e:qa_errors.append(str(e)))
    qa.goto((ROOT / "experience.html").as_uri()+"?v113Preview=1")
    ck(qa.locator("#v113TabClinical").is_enabled(),
       "QA-only clinical preview not accessible with authorized flag")
    qa.locator("#v113TabClinical").click()
    ck(qa.locator("#v113ClinicalScreen").is_visible(),"QA clinical view unavailable")
    ck(qa.evaluate("CardiacClinicalV113.caseReviewStatus")=="draft-human-review-pending",
       "unreviewed clinical fixture state changed")
    qa.get_by_role("button",name="가상 사례 시작").click()
    ck(qa.locator(".v113-question-prompt").is_visible(),
       "original case first question not visible")
    ck(qa.evaluate("CardiacClinicalV113.sessionSnapshot.index")==0,
       "original case session not started")
    qa.locator(".v113-choices input").first.check()
    qa.get_by_role("button",name="선택한 답안 제출").click()
    ck(qa.locator("#v113ClinicalScreen .cx-screen-lead").is_visible(),
       "clinical introduction disappeared after original decision render")
    state=qa.evaluate("CardiacClinicalV113.sessionSnapshot")
    ck(any(v["submitted"] for v in state["answers"].values()),
       "clinical decision no longer submits")
    qa.locator("#v113TabLearning").click()
    qa.locator("#v113TabClinical").click()
    ck(qa.locator("#v113ClinicalScreen .cx-screen-lead").is_visible(),
       "clinical intro not retained on return from Learning")
    ck(qa.evaluate("CardiacClinicalV113.sessionSnapshot")==state,
       "clinical decision lost through Learning round-trip")
    shot(qa,"06-qa-clinical.png")
    ck(not qa_errors, "QA browser JS errors: "+str(qa_errors))
    ck(not errors, "Experience JS errors: "+str(errors))
    browser.close()

print("Cardiac Experience v2", checks, "browser assertions PASS; review screenshots in", OUT)
