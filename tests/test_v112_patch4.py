"""v1.12 Patch 4: novice-first three-tier clinical learning and UI regressions.

True index.html Chromium integration. All 13 prior suites remain separate.
The simulator is not a patient monitor or clinical decision tool.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/'preview-v112p4'
SHOTS.mkdir(exist_ok=True)
checks=0
def ck(test,message):
 global checks
 checks+=1
 assert test,message

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',
   args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1366,'height':768})
 errors=[]
 page.on('pageerror',lambda exc:errors.append(str(exc)))
 page.goto((ROOT/'index.html').as_uri(),wait_until='load')
 page.wait_for_function('["v1.12 Patch 4","v1.12 Patch 5","v1.12 Patch 6","v1.12 Patch 7","v1.12 Patch 8","v1.12 Patch 9","v1.12 Patch 10","v1.12 Patch 11","v1.12 Patch 12","v1.12 Patch 13"].includes(window.CardiacGuidedLearning?.version)')
 ck(any(v in page.locator('h1').inner_text() for v in ('v1.12 Patch 4','v1.12 Patch 5','v1.12 Patch 6','v1.12 Patch 7','v1.12 Patch 8','v1.12 Patch 9','v1.12 Patch 10','v1.12 Patch 11','v1.12 Patch 12','v1.12 Patch 13')),'version')
 ck(page.evaluate('CardiacDashboard.density')=='compact','original compact mode')
 ck(page.locator('#guidedV112Panel').is_hidden(),'guide must default hidden')
 ck(page.locator('.dashboard-clinical').is_visible(),'old clinical summary not shown')
 ck(page.locator('#ecgCanvas').is_visible(),'ECG missing')
 ck(page.locator('#wiggersDeepDive').count()==1,'source six-part nursing detail missing')
 ck(page.evaluate('document.documentElement.scrollHeight')<=1150,
    'first-viewport height regression >16px above 892px baseline')
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='basic','not novice by default')
 page.screenshot(path=str(SHOTS/'01-compact-default-1366.png'),
                 full_page=True,animations='disabled')

 page.evaluate("""() => {
   window.__p4SeekEvents=0;
   document.getElementById('timeSlider').addEventListener('input',
     ()=>{window.__p4SeekEvents++;});
 }""")
 def state():
    return page.evaluate("""() => ({
      a:heartState.physiologicalTime,
      b:heartState.visualizationTime,
      start:heartState.cycleStartTime,
      sweep:heartState.sweepPosition,
      hr:heartRate,playing:heartState.playing,
      step:heartState.currentStep,
      view:CardiacDashboard.view,
      mech:CardiacMechanical.mode,
      density:CardiacDashboard.density,
      count:window.__p4SeekEvents
    })""")

 original=state()
 page.locator('#guidedV112Toggle').click()
 page.locator("#guidedV112Tools").evaluate("(e)=>e.open=true")
 ck(page.locator('#guidedV112Panel').is_visible(),'study not opened')
 ck(page.locator('.dashboard-clinical').is_hidden(),'old summary not replaced')
 ck(page.locator('#guidedV112Level').input_value()=='basic','not beginner tier')
 ck(page.locator('#guidedV112Level option').count()==3,'not three progressive levels')
 ck(page.locator('#guidedV112Promote').is_visible(),'no next learning level')
 ck(page.locator('#guidedV112Model').is_hidden(),'model milliseconds confuse beginners')
 ck(page.locator('#guidedV112Advanced').is_hidden(),'extra study leaked')
 ck(page.locator('#guidedV112Nursing').is_hidden(),'nursing detail not gated to next level')
 ck(page.locator('#guidedV112Electrical').is_visible(),'ECG novice concept missing')
 ck(page.locator('#guidedV112Hemodynamics').is_visible(),'valves novice concept missing')
 ck(page.locator('#guidedV112Volume').is_visible(),'flow novice concept missing')
 ck('한 문장으로 이해하기' in page.locator('#guidedV112Gist').inner_text(),
    'one-sentence novice anchor missing')
 ck('1단계' in page.locator('#guidedV112LevelHint').inner_text(),
    'progressive first-step instruction missing')
 ck(page.locator('#guidedV112Quiz').evaluate('(el)=>!el.open'),
    'quiz must stay optional closed')
 ck(not state()['playing'] and state()['a']>0,'course start failed to show stage 1')
 original=state()
 page.screenshot(path=str(SHOTS/'02-novice-first-stage-desktop.png'),
                 full_page=True,animations='disabled')

 # Every novice concept corresponds to the selected cardiac stage.
 stages=['atrial_systole','isovolumetric_contraction','ejection',
         'isovolumetric_relaxation','filling']
 for index,stage in enumerate(stages):
    page.locator('#guidedV112Select').select_option(stage)
    gist=page.locator('#guidedV112Gist').inner_text()
    ck(len(gist)>25,'novice one-liner absent '+stage)
    ck('1단계' in page.locator('#guidedV112LevelHint').inner_text(),
       'novice tier changed during stage navigation')
    ck(page.locator('#guidedV112Nursing').is_hidden(),
       'too much beginner content '+stage)
    ck(page.locator('#guidedV112Model').is_hidden(),
       'model ms should not be entry-level information '+stage)
    ck(page.locator('#guidedV112Advanced').is_hidden(),
       'source caution leaked '+stage)
    if stage=='filling':
       ck('RR' in page.locator('#guidedV112Limits').inner_text(),
          'important two-interval filling caveat lost')
    ck(not state()['playing'] and (index==0 or page.evaluate('CardiacMechanical.currentState.stage')==stage),'stage auto-observation wrong '+stage)
 ck(page.evaluate('CardiacGuidedLearning.selectedStageId')=='filling',
    'stage selection lost')
 original=state()

 # Second tier reveals concise nursing observation WITHOUT extra 
 # diagnosis or full length advanced source.
 page.locator('#guidedV112Promote').click()
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='intermediate',
    'next-level action did not enter nursing connection tier')
 ck(page.locator('#guidedV112Level').input_value()=='intermediate',
    'native difficulty menu out of sync')
 ck('2단계' in page.locator('#guidedV112LevelHint').inner_text(),
    'nursing progression label missing')
 ck(page.locator('#guidedV112Nursing').is_visible(),
    'intermediate nursing observation not visible')
 ck('간호' in page.locator('#guidedV112LevelHint').inner_text(),
    'intermediate learning purpose not visible')
 ck(page.locator('#guidedV112Advanced').is_hidden(),
    'full advanced content leaked in nursing tier')
 ck(page.locator('#guidedV112Model').is_hidden(),
    'model midpoint should stay extra study')
 ck('0.88' in page.locator('#guidedV112Limits').inner_text(),
    'detailed filling safety caveat missing when ready')
 ck('추가학습' in page.locator('#guidedV112Promote').inner_text(),
    'advance to optional extra study missing')
 ck(state()==original,'nursing connection changed A/B/HR/view')
 page.screenshot(path=str(SHOTS/'03-nursing-connection-desktop.png'),
                 full_page=True,animations='disabled')

 # Third tier preserves all source PHASES/RATE text and advanced quizzes.
 page.locator('#guidedV112Promote').click()
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='advanced',
    'extra learning action failed')
 ck(page.locator('#guidedV112Promote').is_hidden(),
    'last learning level must not display another next tier')
 ck(page.locator('#guidedV112Advanced').is_visible(),
    'full clinical extra study missing')
 ck(page.locator('#guidedV112Model').is_visible(),
    'advanced model observation absent')
 ck('추가학습' in page.locator('#guidedV112Advanced summary').inner_text(),
    'original source not labeled extra learning')
 ck(page.locator('#guidedV112Advanced').evaluate('(e)=>!e.open'),
    'long advanced text was forcibly expanded')
 page.locator('#guidedV112Advanced summary').click()
 for stage in stages:
    page.locator('#guidedV112Select').select_option(stage)
    for key,source in [('Electrical','electrical'),
        ('Hemodynamics','hemodynamics'),('Volume','volume'),
        ('Nursing','nursing'),('Caution','caution'),
        ('Comparison','comparison')]:
       actual=page.locator('#guidedV112Full'+key).inner_text()
       expected=page.evaluate(
         '(s)=>CardiacLearning.getStageNarrative(s[0])[s[1]]',[stage,source])
       ck(actual==expected,'source paragraph changed: '+stage+' '+source)
    ck(not state()['playing'] and page.evaluate('CardiacMechanical.currentState.stage')==stage,'extra study observation failed')
 original=state()
 page.screenshot(path=str(SHOTS/'04-additional-study-desktop.png'),
                 full_page=True,animations='disabled')

 # Quiz remains available, stage-local basic and optional advanced untouched.
 page.locator('#guidedV112Quiz summary').click()
 ck(page.locator('#guidedV112BasicQuestion').is_visible(),'basic quiz lost')
 ck(page.locator('#guidedV112AdvancedQuestion').is_visible(),'advanced quiz lost')
 ck(page.locator('#guidedV112SubmitBasic').is_disabled(),
    'correctness offered before option')
 page.locator('#guidedV112BasicQuestion input[type=radio]').first.check()
 ck(page.locator('#guidedV112FeedbackBasic').is_hidden(),
    'correctness revealed before user submits')
 page.locator('#guidedV112SubmitBasic').click()
 ck(page.locator('#guidedV112FeedbackBasic').is_visible(),'quiz submit broken')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==1,
    'progress lost')
 ck(state()==original,'quiz mutated cardiac A/B/player')
 page.locator('#guidedV112Level').select_option('basic')
 ck(page.locator('#guidedV112Advanced').is_hidden(),
    'full extra source visible when returning to novice')
 ck(page.locator('#guidedV112Nursing').is_hidden(),
    'nursing overload reappeared in novice')
 ck(page.locator('#guidedV112AdvancedQuestion').is_hidden(),
    'advanced quiz leaked in novice')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==1,
    'tier change destroyed in-memory answers')
 page.locator('#guidedV112Level').select_option('intermediate')
 ck(page.locator('#guidedV112Nursing').is_visible(),'middle-level via select failed')
 ck(page.locator('#guidedV112Advanced').is_hidden(),
    'intermediate must keep long sources opt-in')
 ck(state()==original,'tier switching mutated simulation')

 # Original explicit Wiggers and Timeline controls retain Patch 2 semantics.
 beforeWiggers=page.evaluate('window.__p4SeekEvents')
 page.locator('#guidedV112ViewWiggers').click()
 ck(page.evaluate('CardiacDashboard.view')=='wiggers','manual Wiggers broken')
 ck(page.locator('#wiggersChart').is_visible(),'Wiggers chart missing')
 ck(page.locator('#wiggersMarkers [data-event]').count()==4,
    'valve event markers missing')
 ck(page.evaluate('window.__p4SeekEvents')==beforeWiggers,'Wiggers view auto-sought')
 page.locator('#guidedV112Seek').click()
 ck(page.evaluate('window.__p4SeekEvents')==beforeWiggers+1,
    'manual Timeline repeat should fire exactly once')
 ck(not page.evaluate('heartState.playing'),'explicit seek must pause playback')
 ck(page.evaluate('CardiacDashboard.view')=='wiggers',
    'explicit seek should not change view')
 page.locator('#resetBtn').click()
 ck(page.evaluate('CardiacDashboard.isReady'),'original Reset not functioning')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==1,
    'Reset erased educational progress')
 page.locator('#guidedV112Toggle').click()
 ck(page.locator('.dashboard-clinical').is_visible(),
    'closing guide failed to restore live nursing')
 ck(page.locator('#wiggersDeepDive').count()==1,
    'full separate original nursing teaching removed')

 # Check both basic and extra study at common viewport sizes, without 
 # forcing user device manual signoff.
 for width in (1440,1366,1024,768,390,360):
    page.set_viewport_size({'width':width,'height':800})
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       'closed page horizontal overflow '+str(width))
    page.locator('#guidedV112Toggle').click()
    page.locator('#guidedV112Level').select_option('basic')
    ck(page.locator('#guidedV112Gist').is_visible(),
       'novice gist missing '+str(width))
    ck(page.locator('#guidedV112Nursing').is_hidden(),
       'novice content leakage '+str(width))
    ck(page.locator('#guidedV112Promote').is_visible(),
       'progression button inaccessible '+str(width))
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       'open novice page horizontal overflow '+str(width))
    page.locator('#guidedV112Level').select_option('advanced')
    ck(page.locator('#guidedV112Advanced').is_visible(),
       'extra sources inaccessible '+str(width))
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       'extra course caused global overflow '+str(width))
    if width==390:
       page.screenshot(path=str(SHOTS/'05-mobile-novice-and-extra-390.png'),
                       full_page=True,animations='disabled')
    page.locator('#guidedV112Toggle').click()

 page.reload(wait_until='load')
 page.wait_for_function('!!window.CardiacGuidedLearning')
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='basic',
    'reload did not default to novice')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==0,
    'question session state unexpectedly persisted')
 ck(not errors,'uncaught JS error: '+str(errors))
 print(f'PASS {checks} v1.12 Patch4 progressive student learning checks')
 browser.close()
