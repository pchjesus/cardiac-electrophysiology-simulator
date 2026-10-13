"""v1.12 Patch 5 clinical text, model boundary and UX regression.
Actual Chromium against index.html. Screenshots are automated, not target-device signoff.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "preview-v112p5"
SHOTS.mkdir(exist_ok=True)
checks = 0

def ck(ok, message):
    global checks
    checks += 1
    assert ok, message

STAGES = [
    "atrial_systole", "isovolumetric_contraction", "ejection",
    "isovolumetric_relaxation", "filling"
]
RATES = [30, 50, 59, 60, 72, 80, 100, 101, 120, 180]

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium",
        args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={"width": 1366, "height": 768})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((ROOT / "index.html").as_uri(), wait_until="load")
    page.wait_for_function('window.CardiacGuidedLearning?.version?.startsWith("v1.12 Patch ")')
    ck("v1.12 Patch " in page.locator("h1").inner_text(), "version mismatch")
    ck(page.evaluate("CardiacDashboard.density") == "compact", "compact startup changed")
    ck(page.locator("#guidedV112Panel").is_hidden(), "course not opt-in")
    ck(page.locator(".dashboard-clinical").is_visible(), "original live panel missing")
    ck(page.evaluate("document.documentElement.scrollHeight") <= 1150,
       "default desktop viewport grew")
    page.screenshot(path=str(SHOTS/"01-default-1366.png"),
        full_page=True, animations="disabled")

    # Physiology is NOT modified: compare the independent model and stage
    # boundaries across the complete supported HR range.
    cases = page.evaluate("""(rates) => {
      const expected = [
        ['atrial_systole',true,false],
        ['isovolumetric_contraction',false,false],
        ['ejection',false,true],
        ['isovolumetric_relaxation',false,false],
        ['filling',true,false]
      ];
      return rates.map(hr=>{
        const t=getPhysiologicalTiming(hr);
        const b=CardiacMechanical.getMechanicalTiming(t);
        const segs=[
          [b.atrialStart,b.contractionStart],
          [b.contractionStart,b.ejectionStart],
          [b.ejectionStart,b.ejectionEnd],
          [b.ejectionEnd,b.relaxationEnd],
          [b.relaxationEnd,b.rr]
        ];
        const actual=segs.map(([a,z],i)=>{
          const guided=CardiacGuidedContent.getObservation(expected[i][0],
            t,CardiacMechanical,CardiacWiggersProfile);
          const snap=CardiacWiggersProfile.getSnapshot((a+z)/2,t);
          const mech=CardiacMechanical.getMechanicalState((a+z)/2,t);
          const before=CardiacWiggersProfile.getSnapshot(Math.max(0,a-0.0001),t);
          const at=CardiacWiggersProfile.getSnapshot(a,t);
          return {stage:snap.mechanical.stage,mechanical:mech.stage,
            mitral:snap.valves.mitral,aortic:snap.valves.aortic,
            start:guided.startMs,end:guided.endMs,mid:guided.midpointMs,
            interval:[a,z],v:snap.ventricularVolume.relativeValue,
            pressure:snap.pressure,at:at.mechanical.stage,
            before:before.mechanical.stage,
            expected:expected[i]};
        });
        const early=CardiacWiggersProfile.getSnapshot(b.atrialStart/2,t);
        const lateStart=CardiacWiggersProfile.getSnapshot(b.relaxationEnd,t);
        const late=CardiacWiggersProfile.getSnapshot((b.relaxationEnd+b.rr)/2,t);
        const nearEnd=CardiacWiggersProfile.getSnapshot(b.rr-0.0001,t);
        return {hr,rr:t.rr,b,actual,
          earlyV:early.ventricularVolume.relativeValue,
          lateStartV:lateStart.ventricularVolume.relativeValue,
          lateV:late.ventricularVolume.relativeValue,
          nearEndV:nearEnd.ventricularVolume.relativeValue,
          earlyStage:early.mechanical.stage,
          lateStage:late.mechanical.stage};
      });
    }""", RATES)

    for case in cases:
        hr, bounds = case["hr"], case["b"]
        ck(abs(case["rr"]-60000/hr)<1e-7, f"RR/Hr mismatch {hr}")
        ck(0 < bounds["atrialStart"] < bounds["contractionStart"] <
           bounds["ejectionStart"] < bounds["ejectionEnd"] <
           bounds["relaxationEnd"] < bounds["rr"], f"boundary order {hr}")
        for i, entry in enumerate(case["actual"]):
            label, mitral, aortic = (
                (STAGES[i], True, False) if i==0 else
                (STAGES[i], False, False) if i in (1,3) else
                (STAGES[i], False, True) if i==2 else
                (STAGES[i], True, False)
            )
            ck(entry["stage"] == label, f"Wiggers stage {hr} {label}")
            ck(entry["mechanical"] == label, f"Mechanical stage {hr} {label}")
            ck(entry["at"] == label, f"exact boundary stage {hr} {label}")
            ck(entry["mitral"] == mitral and entry["aortic"] == aortic,
               f"valve state {hr} {label}")
            ck(abs(entry["start"] - entry["interval"][0])<1e-7 and
               abs(entry["end"] - entry["interval"][1])<1e-7,
               f"guided timing {hr} {label}")
            ck(entry["start"] < entry["mid"] < entry["end"],
               f"representative midpoint {hr} {label}")
            if i in (1,3):
                target=1.0 if i==1 else 0.48
                ck(abs(entry["v"]-target)<1e-6, f"isovolumetric volume {hr} {label}")
        ck(case["earlyStage"]=="filling" and case["lateStage"]=="filling",
           f"two filling segments missing {hr}")
        ck(abs(case["earlyV"]-0.88)<1e-6, f"early filling plateau {hr}")
        ck(abs(case["lateStartV"]-0.48)<1e-6, f"late filling start {hr}")
        ck(0.48<case["lateV"]<0.88, f"late filling does not increase {hr}")
        ck(abs(case["nearEndV"]-0.88)<1e-5, f"late filling end {hr}")

    # Both original detailed teaching sources now explicitly state the
    # special early-RR plateau. All ten existing questions remain intact.
    page.locator("#guidedV112Toggle").click()
    page.locator("#guidedV112Select").select_option("filling")
    ck("RR" in page.locator("#guidedV112Limits").inner_text(),
       "student-facing two-segment caveat missing")
    ck("0.88" in page.evaluate(
       "CardiacLearning.getStageNarrative('filling').volume"),
       "original Wiggers source misses plateau")
    ck("0.88" in page.evaluate(
       "document.getElementById('wiggersLearningStage')?.textContent || ''") or
       page.evaluate("typeof CardiacWiggersView==='object'"),
       "Wiggers education unavailable")
    for stage in STAGES:
        page.locator("#guidedV112Select").select_option(stage)
        for tier in ("basic", "advanced"):
            ck(page.evaluate("""([s,t]) => {
              const q=CardiacGuidedQuestions.get(s,t);
              return !!q && q.options.length===3 &&
                q.correctIndex>=0 && q.correctIndex<=2 &&
                q.explanation.length>12;
            }""", [stage,tier]), f"existing question lost {stage}/{tier}")
    page.locator("#guidedV112Select").select_option("filling")
    ck("상대 용적" in page.locator("#guidedV112Gist").inner_text(),
       "beginner text not aligned to modeled late filling")
    page.screenshot(path=str(SHOTS/"02-basic-filling-1366.png"),
        full_page=True, animations="disabled")
    page.locator("#guidedV112Promote").click()
    ck(page.locator("#guidedV112Nursing").is_visible(),
       "nursing tier not readable")
    page.screenshot(path=str(SHOTS/"03-nursing-1366.png"),
        full_page=True, animations="disabled")
    page.locator("#guidedV112Promote").click()
    page.locator("#guidedV112Advanced summary").click()
    ck("0.88" in page.locator("#guidedV112FullVolume").inner_text(),
       "full source filling exception missing")
    page.screenshot(path=str(SHOTS/"04-additional-1366.png"),
        full_page=True, animations="disabled")

    # Text-size checks apply to educational caveats only, not the entire UI.
    for width in (1440, 1366, 1024, 768, 390, 360):
        page.set_viewport_size({"width":width,"height":800})
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           f"whole page horizontal overflow {width}")
        size=page.locator("#guidedV112Limits").evaluate(
          "(e)=>parseFloat(getComputedStyle(e).fontSize)")
        ck(size>= (13 if width<700 else 12),
           f"important model caveat too small at {width}: {size}")
        ck(page.locator("#guidedV112Level").is_visible(),
           f"level menu not available {width}")
        if width == 390:
            page.screenshot(path=str(SHOTS/"05-mobile-390.png"),
                full_page=True, animations="disabled")
        if width == 360:
            page.screenshot(path=str(SHOTS/"06-mobile-360.png"),
                full_page=True, animations="disabled")

    # Native keyboard navigation and accessibility: no new timer or implicit seek.
    page.locator("#guidedV112Level").select_option("basic")
    page.locator("#guidedV112Toggle").focus()
    page.keyboard.press("Enter")
    ck(page.locator("#guidedV112Panel").is_hidden(), "keyboard close broken")
    ck(page.locator(".dashboard-clinical").is_visible(), "live content not restored")
    page.locator("#guidedV112Toggle").focus()
    page.keyboard.press("Enter")
    ck(page.locator("#guidedV112Panel").is_visible(), "keyboard reopen broken")
    ck(page.evaluate("CardiacGuidedLearning.selectedStageId")=="filling",
       "keyboard toggle destroyed study selection")
    ck(not errors, "page script error: "+str(errors))
    print(f"PASS {checks} v1.12 Patch5 education/model/UI assertions")
    browser.close()
