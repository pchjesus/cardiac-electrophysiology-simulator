"""v1.10 Patch 5: scenario education, reference overlays and protected regressions."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
count=0
def ck(cond,msg):
    global count
    count+=1
    assert cond,msg

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path="/usr/bin/chromium",
       args=["--no-sandbox","--disable-dev-shm-usage"])
    page=browser.new_page(viewport={"width":1366,"height":900})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.set_content((ROOT/"index.html").read_text(encoding="utf-8"))
    page.add_style_tag(content=(ROOT/"style.css").read_text(encoding="utf-8"))
    for f in ("script.js","mechanics.js","wiggers.js","wiggers-profile.js",
              "wiggers-view.js","wiggers-help.js","wiggers-learning.js",
              "ui-info-panels.js"):
        page.add_script_tag(content=(ROOT/f).read_text(encoding="utf-8"))

    saved=page.evaluate("""() => ({
        A:heartState.physiologicalTime,B:heartState.visualizationTime,
        playing:heartState.playing,hr:heartRate,mode:CardiacMechanical.mode
    })""")
    notes=page.locator("#patchNotesPanel")
    guide=page.locator("#userGuidePanel")
    notesBtn=page.locator("#patchNotesBtn")
    guideBtn=page.locator("#userGuideBtn")
    ck(notes.is_hidden() and guide.is_hidden(),"Reference popovers not initially hidden")
    notesBtn.focus()
    page.keyboard.press("Enter")
    ck(notes.is_visible() and guide.is_hidden(),"Keyboard patch notes opening")
    ck(page.evaluate("CardiacInfoPanels.current")=="patchNotesPanel","Wrong info panel active")
    ck(notesBtn.get_attribute("aria-expanded")=="true","Patch notes aria-expanded")
    ck(notes.locator(".patch-group").count()==4,"History not categorized")
    ck("v1.10 P5" in notes.text_content(),"Patch 5 missing from notes")
    ck(notes.locator("[data-close-info]").evaluate("(e)=>document.activeElement===e"),
       "Popup focus not on close button")
    notes.locator("h3").first.click()
    ck(notes.is_visible(),"Click inside dismissed patch notes")
    guideBtn.click()
    ck(notes.is_hidden() and guide.is_visible(),"Switch between overlays failed")
    ck(notesBtn.get_attribute("aria-expanded")=="false","Old trigger state not cleared")
    ck(guide.locator(".guide-section").count()==5,"Guide lacks required steps")
    ck("Physiological" in guide.text_content() or "physiological" in guide.text_content(),
       "A/B clocks guide missing")
    page.keyboard.press("Escape")
    ck(guide.is_hidden(),"Escape did not dismiss guide")
    ck(guideBtn.evaluate("(e)=>document.activeElement===e"),"Escape focus not restored")
    guideBtn.click()
    guide.locator("[data-close-info]").click()
    ck(guide.is_hidden(),"× did not dismiss")
    ck(guideBtn.evaluate("(e)=>document.activeElement===e"),"× focus restoration")
    notesBtn.click()
    page.locator("#ecgCanvas").click(position={"x":12,"y":60})
    ck(notes.is_hidden(),"Outside click failed to dismiss")
    ck(saved==page.evaluate("""() => ({
        A:heartState.physiologicalTime,B:heartState.visualizationTime,
        playing:heartState.playing,hr:heartRate,mode:CardiacMechanical.mode
    })"""),"Info overlay changed physiological or mode state")

    ck(page.locator("#wiggersDetails").is_visible(),"Wiggers disclosure missing")
    ck(not page.evaluate("document.getElementById('wiggersDetails').open"),
       "Wiggers disclosure changed default")
    page.locator("#wiggersToggle").click(position={"x":12,"y":12})
    page.wait_for_function("document.getElementById('wiggersDetails').open")
    page.wait_for_function("CardiacWiggersView.buildCount>0")
    ck(page.locator("#wiggersDeepDive").count()==1,"Deep education disclosure missing")
    ck(not page.evaluate("document.getElementById('wiggersDeepDive').open"),
       "Deep education should be opt-in")
    ck(page.locator("[data-learning-preset]").count()==3,"Expected 3 scenario buttons")
    if not page.locator('#dashboardResources').evaluate('(e)=>e.open'):
        page.locator('#dashboardResources>summary').click()
    page.locator("#wiggersDeepDive summary").click()
    page.wait_for_function("document.getElementById('wiggersDeepDive').open")
    ck(page.locator("#learningPhaseTitle").text_content().startswith("Ready"),
       "Initial detail must remain Ready")

    for preset,hr,category in (
        ("normal",72,"normal"),("bradycardia",50,"bradycardia"),
        ("tachycardia",120,"tachycardia")
    ):
        page.locator('[data-learning-preset="'+preset+'"]').click()
        info=page.evaluate("""() => ({
            HR:heartRate,rr:getActiveTiming().rr,A:heartState.physiologicalTime,
            B:heartState.visualizationTime,playing:heartState.playing,
            selected:CardiacLearning.activePreset,category:CardiacLearning.category
        })""")
        ck(info["HR"]==hr and abs(info["rr"]-60000/hr)<1e-7,
           f"Scenario did not delegate to physiological HR: {preset}")
        ck(info["selected"]==preset and info["category"]==category,
           f"Preset/category identity wrong {preset}")
        ck(info["A"]==0 and info["B"]==0 and not info["playing"],
           f"Preset mutated Ready clocks {preset}")
        ck(page.locator('[data-learning-preset="'+preset+'"]').get_attribute("aria-pressed")=="true",
           f"Preset accessibility pressed flag {preset}")
        ck(f"{hr} bpm" in page.locator("#learningScenarioSummary").text_content(),
           f"Scenario summary not updated {preset}")
        ck("ms" in page.locator("#learningDuration").text_content(),
           f"Model timing readout missing {preset}")
        ck("환자" in page.locator("#learningNursing").text_content() or
           len(page.locator("#learningNursing").text_content())>30,
           f"Nursing lesson missing {preset}")

    for hr,label in ((30,"bradycardia"),(59,"bradycardia"),
                     (60,"normal"),(80,"normal"),(100,"normal"),
                     (101,"tachycardia"),(180,"tachycardia")):
        page.locator("#heartRateSlider").evaluate("""(el,v)=>{
           el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));
        }""",hr)
        ck(page.evaluate("CardiacLearning.category")==label,
           f"Adult resting HR category wrong: {hr}")
        ck(page.evaluate("CardiacLearning.activePreset") is None,
           f"Manual slider lost Custom identity: {hr}")
        ck("Custom HR" in page.locator("#learningScenarioSummary").text_content(),
           f"Custom summary wrong HR {hr}")

    page.locator('[data-learning-preset="normal"]').click()
    phaseLabels=("filling","atrial_systole","isovolumetric_contraction",
      "ejection","isovolumetric_relaxation")
    for stage in phaseLabels:
        current=page.evaluate("""stage=>{
          const t=CardiacMechanical.getMechanicalTiming();
          const s={
           filling:[t.relaxationEnd,t.rr],
           atrial_systole:[t.atrialStart,t.contractionStart],
           isovolumetric_contraction:[t.contractionStart,t.ejectionStart],
           ejection:[t.ejectionStart,t.ejectionEnd],
           isovolumetric_relaxation:[t.ejectionEnd,t.relaxationEnd]
          }[stage],phase=(s[0]+s[1])/2;
          heartState.physiologicalTime=phase;heartState.cycleStartTime=0;
          heartState.currentStep=1;
          CardiacWiggersView.sync();
          CardiacLearning.sync();
          return CardiacWiggersProfile.getSnapshot(phase,getActiveTiming()).mechanical.stage;
        }""",stage)
        ck(current==stage,f"Stage input {stage} failed")
        ck(len(page.locator("#learningElectrical").text_content())>=45,
           f"Electrical explanation too short {stage}")
        ck(len(page.locator("#learningHemodynamics").text_content())>=55,
           f"Pressure/valve explanation too short {stage}")
        ck(len(page.locator("#learningVolume").text_content())>=55,
           f"Volume explanation too short {stage}")
        ck(len(page.locator("#learningNursing").text_content())>=80,
           f"Nursing explanation too short {stage}")
        ck(len(page.locator("#learningCaution").text_content())>=35,
           f"Clinical limitation missing {stage}")
        ck(page.locator("#learningPhaseTitle").text_content()!="Ready · 시작 전",
           f"Phase not derived from Wiggers {stage}")

    before=page.evaluate("CardiacLearning.renderCount")
    page.evaluate("CardiacLearning.sync();CardiacLearning.sync()")
    ck(page.evaluate("CardiacLearning.renderCount")==before,
       "Excessive detailed text updates on unchanged phase")

    page.locator("#resetBtn").click()
    ck(page.locator("#learningPhaseTitle").text_content().startswith("Ready"),
       "Reset did not restore education Ready state")
    ck(page.evaluate("document.getElementById('wiggersDetails').open"),
       "Reset collapsed original Wiggers panel")
    ck(page.evaluate("document.getElementById('wiggersDeepDive').open"),
       "Reset closed user-selected deep guide")
    page.locator("#timeSlider").evaluate("""(el)=>{
       el.value=45;el.dispatchEvent(new Event('input',{bubbles:true}));
    }""")
    ck(not page.locator("#learningPhaseTitle").text_content().startswith("Ready"),
       "Timeline did not update learning after seek")
    page.locator("#mechanicalModeBtn").click()
    ck(page.locator("#mechanicalView").is_visible(),"Mechanical mode regression")
    page.locator("#electricalModeBtn").click()
    ck(page.locator("#heartSVG").is_visible(),"Electrical mode regression")
    page.locator("#playBtn").click()
    page.wait_for_timeout(180)
    page.locator("#pauseBtn").click()
    ck(not page.evaluate("heartState.playing"),"Pause regression")
    ck(page.evaluate("heartState.physiologicalTime")>0,"A clock stopped advancing")
    ck(page.locator("#wiggersMarkers [data-event]").count()==4,
       "Valve marker regression")
    ck(page.locator("#wiggersChart").is_visible(),"Wiggers graph hidden")

    for width in (1366,768,390,360):
        page.set_viewport_size({"width":width,"height":800})
        for button,popup in ((notesBtn,notes),(guideBtn,guide)):
            button.click()
            box=popup.evaluate("""el=>{
              const r=el.getBoundingClientRect();
              return {l:r.left,r:r.right,t:r.top,b:r.bottom,
                      w:innerWidth,h:innerHeight,scroll:el.scrollHeight,
                      client:el.clientHeight};
            }""")
            ck(box["l"]>=-1 and box["r"]<=box["w"]+1,
               f"Horizontal clipping width {width}: {box}")
            ck(box["t"]>=0 and box["b"]<=box["h"]+1,
               f"Vertical clipping width {width}: {box}")
            ck(box["client"]<=box["h"],f"Popup not scroll constrained {width}")
            page.keyboard.press("Escape")
            ck(popup.is_hidden(),f"Escape failed at width {width}")
    ck(not errors,f"Page JS errors {errors}")
    print(f"PASS {count} v1.10 Patch 5 checks: clinical phases, rates, "
       "scenario identity, two popovers, access/focus, legacy controls and responsive widths.")
    browser.close()
