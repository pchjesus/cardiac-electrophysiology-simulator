"""v1.12 Patch 1 — read-only guided cardiac-cycle UI integration.

Loads the REAL index.html. Verifies default layout remains compact, original
clinical DOM survives, all five model-derived phases and HR boundaries match
the existing Wiggers profile, and guide interactions never control A/B.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CAPTURES=ROOT/'preview-v112p1'
CAPTURES.mkdir(exist_ok=True)
count=0
def check(ok,label):
 global count
 count+=1
 assert ok,label

with sync_playwright() as playwright:
 browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',
   args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1366,'height':768})
 errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 page.goto((ROOT/'index.html').as_uri(),wait_until='load')
 page.wait_for_function('!!window.CardiacGuidedLearning && !!window.CardiacGuidedContent')

 check(any(v in page.locator('h1').inner_text() for v in ('v1.12 Patch 1','v1.12 Patch 2','v1.12 Patch 3','v1.12 Patch 4')),'version')
 check(page.evaluate('CardiacDashboard.density')=='compact','original compact layout')
 check(page.locator('#guidedV112Toggle').is_visible(),'compact entry point missing')
 check(page.locator('#guidedV112Panel').is_hidden(),'guide must default closed')
 check(page.locator('.dashboard-clinical').is_visible(),'original nursing panel missing')
 check(page.locator('#ecgCanvas').is_visible(),'ECG no longer visible')
 check(page.locator('#dashboardWiggersBtn').is_visible(),'original view navigation missing')
 check(page.locator('.dashboard-v111>.measurements-panel').is_visible(),
       'six original measurements missing')
 check(page.locator('#dashboardElectrical').is_visible(),'electrical state missing')
 check(page.locator('#dashboardMechanical').is_visible(),'mechanical state missing')
 check(page.locator('#dashboardEvent').is_visible(),'ECG current-event missing')
 check(page.locator('#wiggersDeepDive').count()==1,'original full teaching removed')
 check(page.evaluate('CardiacGuidedLearning.open') is False,'guide unexpectedly open')
 check(page.evaluate('CardiacGuidedLearning.selectedStageId')=='atrial_systole','default lesson')
 initial_height=page.evaluate('document.documentElement.scrollHeight')
 page.screenshot(path=str(CAPTURES/'01-default-compact-desktop.png'),full_page=True,animations='disabled')
 check(initial_height<=910,
       f'default layout regressed beyond 16px budget: {initial_height}px')

 def state():
    return page.evaluate("""() => ({
      a:heartState.physiologicalTime,b:heartState.visualizationTime,
      cycle:heartState.cycleStartTime,sweep:heartState.sweepPosition,
      hr:heartRate,playing:heartState.playing,step:heartState.currentStep,
      view:CardiacDashboard.view,density:CardiacDashboard.density,
      mechanical:CardiacMechanical.mode,preset:CardiacLearning.activePreset
    })""")

 before=state()
 page.locator('#guidedV112Toggle').click()
 check(page.evaluate('CardiacGuidedLearning.open'),'guide did not open')
 page.screenshot(path=str(CAPTURES/'02-guided-ready-desktop.png'),full_page=True,animations='disabled')
 check(page.locator('#guidedV112Panel').is_visible(),'guide panel hidden')
 check(page.locator('.dashboard-clinical').is_hidden(),'original clinical summary not replaced')
 check(page.locator('#guidedV112Toggle').get_attribute('aria-expanded')=='true',
       'button accessibility state')
 check('1/5' in page.locator('#guidedV112Counter').inner_text(),'stage count')
 check('Ready' in page.locator('#guidedV112Live').inner_text(),'Ready distinction missing')
 check(page.locator('#guidedV112Select option').count()==5,'five stages missing')
 check(state()==before,'opening guide modified canonical simulation')
 # Patch 2 controls are intentionally present, but have no side effects
 # until the learner clicks the corresponding button.
 check(page.locator('#guidedV112Seek').is_visible(),
       'explicit guided seek control missing')
 check(page.locator('#guidedV112ViewWiggers').is_visible(),
       'user-triggered Wiggers view control missing')

 stages=[
 ('atrial_systole','심방 수축'),
 ('isovolumetric_contraction','등용적 수축'),
 ('ejection','심실 박출'),
 ('isovolumetric_relaxation','등용적 이완'),
 ('filling','심실 충만')
 ]
 for i,(stage,label) in enumerate(stages):
    page.locator('#guidedV112Select').select_option(stage)
    check(page.evaluate('CardiacGuidedLearning.selectedStageId')==stage,
          'incorrect selected study stage')
    check(label in page.locator('#guidedV112Title').inner_text(),'step label missing')
    check(f'{i+1}/5' in page.locator('#guidedV112Counter').inner_text(),
          'step counter missing')
    for piece in ('Electrical','Hemodynamics','Volume','Nursing'):
       text=page.locator('#guidedV112'+piece).inner_text()
       from_source=page.evaluate("""(args)=>{
         const [id,kind]=args;
         const src=CardiacLearning.getStageNarrative(id)[kind.toLowerCase()];
         const pos=src.indexOf('다.');
         return pos>=0?src.slice(0,pos+2):src.trim();
       }""",[stage,piece])
       check(len(text)>8 and text==from_source,
             'phase text must equal original nursing source '+stage+':'+piece)
    check('이동하지 않음' in page.locator('#guidedV112Model').inner_text(),
          'observation point must not imply an automatic seek')
    check(state()==before,'stage selection unexpectedly moved simulation')
    if stage=='filling':
       novice=page.locator('#guidedV112Limits').inner_text()
       check('RR' in novice,'the two filling intervals must remain acknowledged')
       page.locator('#guidedV112Level').select_option('intermediate')
       caution=page.locator('#guidedV112Limits').inner_text()
       check('RR' in caution and '0.88' in caution,
             'detailed filling model caveat missing at nursing-connection level')
       page.locator('#guidedV112Level').select_option('basic')

 # Stage text is taken from the source learning dictionary.
 check(page.evaluate("""() => {
   const id='atrial_systole';
   const content=CardiacLearning.getStageNarrative(id);
   return content.phase===id && content.electrical.includes('P파') &&
     content.nursing.includes('P-QRS') && !('patientBloodPressure' in content);
 }"""),'existing source narrative not reused')
 check(page.locator('#wiggersDeepDive').evaluate('(e)=>!e.open'),
       'source nursing details unexpectedly opened')

 # All HRs and representative midpoints must agree with the canonical
 # profile, and filling must explicitly use the post-relaxation interval.
 for hr in (30,50,59,60,72,80,100,101,120,180):
    page.locator('#heartRateSlider').evaluate("""(el,hr)=>{
        el.value=String(hr);el.dispatchEvent(new Event('input',{bubbles:true}));
    }""",hr)
    check(page.evaluate('heartRate')==hr,f'HR slider failed at {hr}')
    for stage,_ in stages:
       actual=page.evaluate("""id=>{
         const model=CardiacGuidedContent.getObservation(
          id,getActiveTiming(),CardiacMechanical,CardiacWiggersProfile);
         const current=CardiacWiggersProfile.getSnapshot(
          model.midpointMs,getActiveTiming());
         return {
           id:current.mechanical.stage,
           rr:model.rrMs,start:model.startMs,end:model.endMs,
           mid:model.midpointMs,volume:model.relativeLVVolume,
           relaxationEnd:CardiacMechanical.getMechanicalTiming(getActiveTiming()).relaxationEnd
         };
       }""",stage)
       check(actual['id']==stage,f'model stage mismatch at {hr} {stage}')
       check(0<=actual['start']<actual['mid']<actual['end']<=actual['rr'],
             f'invalid target interval at {hr} {stage}: {actual}')
       if stage=='filling':
          check(actual['start']==actual['relaxationEnd'],
                'filling guide target must be in RR later segment')
          check(.48<actual['volume']<.88,
                f'filling relative LV volume midpoint wrong at {hr}')
    check(state()['a']==before['a'] and state()['b']==before['b'],
          'guide or HR altered Ready-time A/B unexpectedly')
 check('180' in page.locator('#guidedV112Model').inner_text() or
       'ms' in page.locator('#guidedV112Model').inner_text(),
       'HR-dependent model observation not updated')

 # Seek via the existing Timeline is still available, without guide owning it.
 page.locator('#timeSlider').evaluate("""el=>{
   el.value='34';el.dispatchEvent(new Event('input',{bubbles:true}));
 }""")
 a=state()
 check(a['a']>0 and a['b']>0,'original seek stopped working')
 check('현재 시뮬레이션' in page.locator('#guidedV112Live').inner_text(),
       'live simulation status missing')
 page.locator('#guidedV112Select').select_option('ejection')
 check(state()==a,'study stage selection changed sought A/B')
 check('다름' in page.locator('#guidedV112Live').inner_text() or
       '일치' in page.locator('#guidedV112Live').inner_text(),
       'study/live distinction disappeared')

 # Original independent deep dive remains accessible while guide is active.
 page.locator('#wiggersDeepDive summary').click()
 page.wait_for_function("document.getElementById('wiggersDeepDive').open")
 page.wait_for_function("document.getElementById('learningNursing').textContent.trim().length>70")
 check(page.locator('#learningNursing').is_visible(),'full nursing detail not accessible')
 check(state()==a,'opening independent nursing detail changed simulation')
 page.locator('#guidedV112Toggle').click()
 check(page.locator('#guidedV112Panel').is_hidden(),'guide did not close')
 check(page.locator('.dashboard-clinical').is_visible(),'original summary did not restore')
 check(page.locator('#guidedV112Toggle').get_attribute('aria-expanded')=='false',
       'close aria state')
 check(page.locator('#wiggersDeepDive').evaluate('(e)=>e.open'),
       'closing guide discarded full teaching state')
 check(state()==a,'closing guide changed original simulation state')

 # Existing modes and controls remain independently functional.
 page.locator('#mechanicalModeBtn').click()
 check(page.locator('#mechanicalView').is_visible(),'Mechanical view broken')
 page.locator('#dashboardWiggersBtn').click()
 check(page.locator('#wiggersChart').is_visible(),'Wiggers view broken')
 check(page.locator('#wiggersMarkers [data-event]').count()==4,
       'Wiggers valve markers disappeared')
 page.locator('#electricalModeBtn').click()
 check(page.locator('#ecgCanvas').is_visible(),'ECG hidden after three tab cycles')
 page.locator('#playBtn').click()
 page.wait_for_timeout(120)
 check(page.evaluate('heartState.playing'),'Play failed')
 page.locator('#guidedV112Toggle').click()
 check(page.evaluate('heartState.playing'),'opening guide paused playback')
 page.locator('#pauseBtn').click()
 check(not page.evaluate('heartState.playing'),'Pause failed')
 page.locator('#resetBtn').click()
 check(page.evaluate('CardiacDashboard.isReady'),'Reset Ready failed')
 check(page.evaluate('CardiacGuidedLearning.open'),
       'Reset unexpectedly dismissed guide')
 check('Ready' in page.locator('#guidedV112Live').inner_text(),
       'guide Ready state stale after Reset')
 check(page.evaluate('CardiacDashboard.view')=='electrical',
       'Reset changed visualization tab')
 page.locator('#guidedV112Toggle').click()

 for width in (1440,1366,1024,768,390,360):
    page.set_viewport_size({'width':width,'height':800})
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'),
          f'global viewport overflow {width}')
    check(page.locator('#guidedV112Toggle').is_visible(),
          f'guided entry missing {width}')
    page.locator('#guidedV112Toggle').click()
    if width==390:
       page.screenshot(path=str(CAPTURES/'03-guided-mobile-390.png'),
                       full_page=True,animations='disabled')
    check(page.locator('#guidedV112Panel').is_visible(),
          f'guide inaccessible {width}')
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'),
          f'guide causes global overflow {width}')
    page.locator('#guidedV112Toggle').click()
    check(page.locator('.dashboard-clinical').is_visible(),
          f'guide exit failed {width}')

 check(not errors,'JS exceptions: '+str(errors))
 print(f'PASS {count} v1.12 Patch1 guided integration checks; '
       f'default page height={initial_height}px at 1366x768.')
 browser.close()
