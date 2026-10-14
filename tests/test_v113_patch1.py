"""v1.13 Patch 1 internal top-level tab routing and untouched A/B clock."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/"preview-v113p1"
SHOTS.mkdir(exist_ok=True)
checks=0

def ck(truth, reason):
    global checks
    assert truth, reason
    checks+=1

def snap(page):
    return page.evaluate("""() => ({
      a:heartState.physiologicalTime,b:heartState.visualizationTime,
      start:heartState.cycleStartTime,length:heartState.cycleLength,
      mirror:heartState.ecgTime,sweep:heartState.sweepPosition,
      step:heartState.currentStep,hr:heartRate,speed:animationSpeed,
      timeline:document.querySelector('#timeSlider').value,
      mode:CardiacDashboard.view,stage:CardiacGuidedLearning.selectedStageId,
      level:CardiacGuidedLearning.detailLevel,
      answers:CardiacGuidedLearning.submittedAnswerCount
    })""")

def button(page, key):
    return page.locator('#v113Tab'+key)

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":1366,"height":800})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    ck('v1.13' in page.locator('h1').inner_text(),'v1.13 title missing')
    ck('v1.12 Patch 14' in page.locator('h1').inner_text(),'underlying not-final engine not disclosed')
    ck(page.evaluate("CardiacMainTabs.active")=="simulator","default route")
    ck(not button(page,'Learning').is_disabled() and button(page,'Clinical').is_disabled(),
       'Learning should be released; unreviewed Clinical stays gated')
    ck(page.locator('#dashboardV111').is_visible(),'original simulator hidden on default route')
    for selector in ('#ecgCanvas','#heartSVG','#mechanicalSVG','#wiggersChart',
                     '#guidedV112Assumptions','#timeSlider','#playBtn'):
        ck(page.locator(selector).count()==1,"original DOM duplicated: "+selector)
    ck(page.evaluate("heartState.physiologicalTime===0 && heartState.visualizationTime===0"),
       "Ready clock changed")
    ck(not page.evaluate("CardiacMainTabs.switchTo('clinical')"),"public route bypass")
    ck(page.evaluate("CardiacMainTabs.active")=="simulator","invalid route navigation")
    page.close()

    page=browser.new_page(viewport={"width":1366,"height":800})
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri()+"?v113Preview=1")
    ck(page.evaluate("CardiacMainTabs.preview"),"internal test view not enabled")
    ck(not button(page,"Learning").is_disabled() and not button(page,"Clinical").is_disabled(),
       "internal route buttons disabled")
    assert page.evaluate("CardiacDashboard.isReady"),"should start Ready"
    initial=snap(page)
    button(page,'Learning').click()
    ck(snap(page)==initial,"Learning click must not seek or change Ready state")
    ck(not page.evaluate("CardiacGuidedLearning.open"),"Learning tab auto-started Guided")
    ck(page.locator('#v113LearningScreen').is_visible(),"Learning preview missing")
    ck(not page.locator('#dashboardV111').is_visible(),"hidden simulator remains visible")
    button(page,'Clinical').click()
    ck(snap(page)==initial,"Ready -> clinical route mutated state")
    button(page,'Simulator').click()
    ck(snap(page)==initial,"route return changed Ready")
    ck(button(page,'Simulator').get_attribute('aria-pressed')=='true',"pressed state wrong")

    # Each rate has the same pause/position invariant, with no auto-play on return.
    for rate in (30,72,180):
        page.locator('#heartRateSlider').evaluate("(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}",rate)
        page.locator('#playBtn').click()
        page.wait_for_function("heartState.playing && heartState.physiologicalTime>0")
        # Take the reference and trigger the DOM click in ONE JS turn:
        # RAF is allowed to advance between separate Playwright calls.
        before=page.evaluate("""() => {
          const value={
            a:heartState.physiologicalTime,b:heartState.visualizationTime,
            start:heartState.cycleStartTime,length:heartState.cycleLength,
            mirror:heartState.ecgTime,sweep:heartState.sweepPosition,
            step:heartState.currentStep,hr:heartRate,speed:animationSpeed,
            timeline:document.querySelector('#timeSlider').value,
            mode:CardiacDashboard.view,stage:CardiacGuidedLearning.selectedStageId,
            level:CardiacGuidedLearning.detailLevel,
            answers:CardiacGuidedLearning.submittedAnswerCount
          };
          document.getElementById('v113TabClinical').click();
          return value;
        }""")
        ck(not page.evaluate("heartState.playing"),f"pause failure HR={rate}")
        ck(snap(page)==before,f"route changed model state HR={rate}")
        page.wait_for_timeout(200)
        ck(snap(page)==before,f"hidden animation advanced HR={rate}")
        button(page,'Learning').click()
        button(page,'Simulator').click()
        ck(snap(page)==before,f"round trip changed A/B HR={rate}")
        ck(not page.evaluate("heartState.playing"),"return autoplays")
        same=page.evaluate("heartState.playbackGeneration")
        button(page,'Simulator').click()
        ck(page.evaluate("heartState.playbackGeneration")==same,"same-tab side effect")
        page.locator('#pauseBtn').click()
        page.locator('#resetBtn').click()
        ck(page.evaluate("heartState.physiologicalTime===0 && heartState.visualizationTime===0"),
           "native Reset broken")

    # Original Guided start may deliberately seek once; route switches may not.
    ck(not page.evaluate("CardiacGuidedLearning.open"),"unexpected prestart Guided")
    original=snap(page)
    button(page,"Learning").click()
    button(page,"Simulator").click()
    ck(snap(page)==original,"Ready roundtrip changed state")
    button(page,"Learning").click()
    ck(snap(page)==original,"Learning screen automatically moved time")
    page.locator('#guidedV112Toggle').click()
    ck(page.evaluate("CardiacGuidedLearning.open"),"explicit Guided start failed")
    ck(page.evaluate("heartState.physiologicalTime>0"),"native Guided Ready observation lost")
    # Submitted concept answer remains owned by the ONE original Guided instance.
    pre_answer=snap(page)
    page.locator('#guidedV112Quiz summary').click()
    page.locator('#guidedV112BasicQuestion input[type=radio]').first.check()
    page.locator('#guidedV112SubmitBasic').click()
    ck(page.evaluate("CardiacGuidedLearning.submittedAnswerCount")==1,
       "Guided submission was not stored")
    ck(snap(page)['a']==pre_answer['a'] and snap(page)['b']==pre_answer['b'],
       "answer submission touched A/B")
    after_start=snap(page)
    button(page,'Clinical').click()
    button(page,'Learning').click()
    button(page,'Simulator').click()
    ck(snap(page)==after_start,"Guided stage changed on route switch")
    ck(page.evaluate("CardiacGuidedLearning.open"),"Guided open state reset")
    page.locator('#mechanicalModeBtn').click()
    ck(page.locator('#mechanicalView').is_visible(),"Mechanical view regression")
    before=snap(page)
    button(page,'Learning').click()
    button(page,'Simulator').click()
    ck(snap(page)==before,"Mechanical view or timestamp changed")
    ck(page.locator('#mechanicalView').is_visible(),"Mechanical re-entry display failure")
    page.locator('#dashboardWiggersBtn').click()
    ck(page.locator('#wiggersChart').is_visible(),"Wiggers view regression")
    before=snap(page)
    button(page,'Clinical').click()
    button(page,'Simulator').click()
    ck(snap(page)==before,"Wiggers mode or timestamp changed")
    ck(page.locator('#wiggersChart').is_visible(),"Wiggers return display failure")

    for width in (360,390,768,900,1024,1366):
        page.set_viewport_size({"width":width,"height":800})
        for key in ('Simulator','Learning','Clinical'):
            button(page,key).click()
            ck(button(page,key).get_attribute('aria-pressed')=='true',
               f"{width} {key} pressed-state mismatch")
            ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
               f"{width} {key} horizontal overflow")
        page.screenshot(path=str(SHOTS/f"{width}-clinical-preview.png"),full_page=True)
        button(page,'Simulator').click()
        page.screenshot(path=str(SHOTS/f"{width}-simulator.png"),full_page=True)
        ck(page.locator('#ecgCanvas').is_visible(),f"{width} ECG did not return")
    button(page,"Learning").focus()
    ck(button(page,"Learning").evaluate("e=>document.activeElement===e"),
       "top nav keyboard focus broken")
    ck(not errors,"JavaScript errors: "+str(errors))
    browser.close()
print(f"v1.13 Patch 1: {checks} checks passed")
