"""v1.12 Patch 2: explicit guided navigation/view/seek integration.

Tests the real index.html in Chromium and runs AFTER all older regression
suites. Verifies no implicit A/B/UI side effects; only a direct seek button
is permitted to fire the original Timeline handler and pause playback.
"""
import math
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/'preview-v112p2'
SHOTS.mkdir(exist_ok=True)
n=0

def ck(value,msg):
 global n
 n+=1
 assert value,msg

with sync_playwright() as playwright:
 browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',
      args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1366,'height':768})
 errs=[]
 page.on('pageerror',lambda exc:errs.append(str(exc)))
 page.goto((ROOT/'index.html').as_uri(),wait_until='load')
 page.wait_for_function('window.CardiacGuidedLearning?.version?.startsWith("v1.12 Patch ")')
 ck('v1.12 Patch ' in page.locator('h1').inner_text(),'wrong version')
 ck(page.evaluate('CardiacDashboard.density')=='compact','density regression')
 ck(page.locator('#ecgCanvas').is_visible(),'no ECG')
 ck(page.locator('#guidedV112Panel').is_hidden(),'guide starts open')
 ck(page.locator('.dashboard-clinical').is_visible(),'original clinical summary hidden')
 ck(page.locator('#guidedV112Previous').count()==1,'duplicate previous control')
 ck(page.locator('#guidedV112Next').count()==1,'duplicate next control')
 ck(page.locator('#guidedV112ViewWiggers').count()==1,'duplicate Wiggers control')
 ck(page.locator('#guidedV112Seek').count()==1,'duplicate seek control')
 ck(page.evaluate("""() => {
   const nav=document.querySelector('.v113-main-nav');
   const style=nav&&getComputedStyle(nav);
   const navigationFootprint=nav ? nav.getBoundingClientRect().height+
     parseFloat(style.marginTop)+parseFloat(style.marginBottom) : 0;
   return document.documentElement.scrollHeight-navigationFootprint;
 }""")<=1150,
    'closed dashboard exceeds 892+16px contract')
 page.screenshot(path=str(SHOTS/'01-default-compact-1366.png'),
                 full_page=True,animations='disabled')

 # Spy on original Timeline dispatch to ensure stage navigation does not
 # produce even one hidden seek.
 page.evaluate("""() => {
    window.__p2TimelineEvents=0;
    document.getElementById('timeSlider').addEventListener('input',
       ()=>{window.__p2TimelineEvents++;});
 }""")
 def clock():
    return page.evaluate("""() => ({
       a:heartState.physiologicalTime,
       b:heartState.visualizationTime,
       start:heartState.cycleStartTime,
       sweep:heartState.sweepPosition,
       hr:heartRate,step:heartState.currentStep,
       playing:heartState.playing,
       view:CardiacDashboard.view,
       mech:CardiacMechanical.mode,
       density:CardiacDashboard.density,
       inputCount:window.__p2TimelineEvents
    })""")
 before=clock()
 page.locator('#guidedV112Toggle').click()
 page.locator("#guidedV112Tools").evaluate("(e)=>e.open=true")
 ck(page.evaluate('CardiacGuidedLearning.open'),'guide did not open')
 ck(page.locator('#guidedV112Previous').is_disabled(),'first previous not disabled')
 ck(not page.locator('#guidedV112Next').is_disabled(),'first next unexpectedly disabled')
 ck(page.locator('#guidedV112Seek').get_attribute('aria-describedby')=='guidedV112SeekNotice',
    'seek warning association missing')
 ck('일시 정지' in page.locator('#guidedV112SeekNotice').inner_text(),
    'seek effects must be announced before click')
 ck('Timeline' in page.locator('#guidedV112SeekNotice').inner_text(),
    'seek notice should identify original Timeline')
 ck(not clock()['playing'] and clock()['inputCount']==before['inputCount']+1,'course start must use one Timeline seek')
 before=clock()
 page.screenshot(path=str(SHOTS/'02-guided-navigation-desktop.png'),
                 full_page=True,animations='disabled')

 stages=['atrial_systole','isovolumetric_contraction','ejection',
         'isovolumetric_relaxation','filling']
 for idx,stage in enumerate(stages):
    ck(page.evaluate('CardiacGuidedLearning.selectedStageId')==stage,
       f'stage sequence wrong at {idx}')
    ck(f'{idx+1}/5' in page.locator('#guidedV112Counter').inner_text(),
       f'counter out of sync at {idx}')
    ck(page.locator('#guidedV112Previous').is_disabled()==(idx==0),
       f'previous boundary wrong at {idx}')
    ck(page.locator('#guidedV112Next').is_disabled()==(idx==4),
       f'next boundary wrong at {idx}')
    ck(not clock()['playing'],'guided navigation should pause simulation')
    if idx!=4:page.locator('#guidedV112Next').click()
 ck(page.locator('#guidedV112Next').is_disabled(),'fifth stage next not disabled')
 ck(not clock()['playing'] and clock()['inputCount']>=4,'guided next navigation did not seek')
 for idx in (3,2,1,0):
    page.locator('#guidedV112Previous').click()
    ck(page.evaluate('CardiacGuidedLearning.selectedStageId')==stages[idx],
       f'previous changed wrong study stage at {idx}')
 ck(not clock()['playing'] and clock()['inputCount']>=8,'guided previous navigation did not seek')
 ck(page.locator('#guidedV112Previous').is_disabled(),'first previous boundary lost')
 # Native selector and next/previous share same cursor.
 page.locator('#guidedV112Select').select_option('ejection')
 ck(page.locator('#guidedV112Counter').inner_text().endswith('3/5'),
    'native select does not update step counter')
 page.locator('#guidedV112Previous').click()
 ck(page.evaluate('CardiacGuidedLearning.selectedStageId')=='isovolumetric_contraction',
    'previous after dropdown out of sync')
 # Enter keyboard should activate a native button, without moving simulation.
 page.locator('#guidedV112Next').focus()
 page.keyboard.press('Enter')
 ck(page.evaluate('CardiacGuidedLearning.selectedStageId')=='ejection',
    'keyboard Enter did not navigate')
 ck(not clock()['playing'],'guided dropdown/keyboard must pause')

 # Wiggers is user-triggered and changes ONLY the view when requested.
 ck(page.evaluate('CardiacDashboard.view')=='electrical',
    'guide navigation implicitly switched to Wiggers')
 beforeView=clock()
 page.locator('#guidedV112ViewWiggers').click()
 w=clock()
 ck(w['view']=='wiggers','Wiggers button did not switch view')
 ck(page.locator('#wiggersChart').is_visible(),'Wiggers graph is hidden')
 ck(page.locator('#wiggersMarkers [data-event]').count()==4,
    'original valve events lost')
 for key in ('a','b','start','sweep','hr','step','playing','inputCount','mech','density'):
    ck(w[key]==beforeView[key],f'Wiggers button changed simulation state {key}')
 ck(page.evaluate('CardiacGuidedLearning.selectedStageId')=='ejection',
    'manual Wiggers view unexpectedly changed study stage')
 page.locator('#electricalModeBtn').click()
 ck(page.evaluate('CardiacDashboard.view')=='electrical',
    'manual Electrical return not available')
 ck(clock()['inputCount']==w['inputCount'],'manual views implicitly sought timeline')

 # All HRs: target = in-stage midpoint; native Timeline input must
 # dispatch exactly one event per explicit click and preserve chosen mode.
 for hr in (30,50,59,60,72,80,100,101,120,180):
    page.locator('#heartRateSlider').evaluate("""(el,hr)=>{
      el.value=String(hr);
      el.dispatchEvent(new Event('input',{bubbles:true}));
    }""",hr)
    ck(page.evaluate('heartRate')==hr,f'HR slider broken {hr}')
    for stage in stages:
       page.locator('#guidedV112Select').select_option(stage)
       prior=clock()
       observation=page.evaluate("""stage=>{
         return CardiacGuidedContent.getObservation(
           stage,getActiveTiming(),CardiacMechanical,CardiacWiggersProfile);
       }""",stage)
       ck(prior['playing'] is False,'unexpected playback before explicit seek')
       ck(prior['inputCount']==page.evaluate('window.__p2TimelineEvents'),
          'stage dropdown unexpectedly fired Timeline event')
       page.locator('#guidedV112Seek').click()
       got=clock()
       ck(got['inputCount']==prior['inputCount']+1,
          f'explicit seek should fire exactly one native input at {hr} {stage}')
       ck(got['playing'] is False,'native Timeline seek must pause')
       ck(got['hr']==hr and got['view']=='electrical',
          f'explicit seek changed rate or view at {hr} {stage}')
       ck(got['a']>=observation['startMs']-1e-8 and
          got['a']<observation['endMs']+1e-8,
          f'new A outside selected stage at {hr} {stage}: {got["a"]}')
       # The native slider rounds 0.1% increments of the model RR.
       ck(abs(got['a']-observation['midpointMs'])<=observation['rrMs']*.001+1e-7,
          f'timeline representative position wrong at {hr} {stage}')
       ck(page.evaluate("""() => CardiacWiggersProfile.getSnapshot(
           getPhysiologicalCyclePhase(),getActiveTiming()).mechanical.stage""")==stage,
          f'Wiggers stage after actual seek wrong at {hr} {stage}')
       normalized=page.evaluate("""() => ({
         a:heartState.physiologicalTime/getActiveTiming().rr,
         b:heartState.visualizationTime/baseCycleLength,
         slider:Number(document.getElementById('timeSlider').value)/100
       })""")
       ck(abs(normalized['a']-normalized['b'])<.0011,
          f'A/B time fraction diverged {hr} {stage}')
       ck(abs(normalized['b']-normalized['slider'])<1e-8,
          'B clock does not follow original slider')
       ck(page.evaluate('CardiacGuidedLearning.selectedStageId')==stage,
          'seek changed chosen study stage')
 ck(page.evaluate('window.__p2TimelineEvents')>=len(stages)*10,
    'unexpected extra timeline input events')

 # Reset the time and check playback, study navigation and view controls
 # never implicitly pause or reset a currently running simulation.
 page.locator('#resetBtn').click()
 ck(page.evaluate('CardiacDashboard.isReady'),'Reset Ready broken')
 page.locator('#playBtn').click()
 page.wait_for_timeout(150)
 ck(page.evaluate('heartState.playing'),'Play broken')
 page.locator('#guidedV112Previous').click()
 ck(not page.evaluate('heartState.playing'),'guided previous must pause playback')
 page.locator('#guidedV112ViewWiggers').click()
 ck(not page.evaluate('heartState.playing'),'manual Wiggers must preserve paused state')
 ck(page.evaluate('CardiacDashboard.view')=='wiggers',
    'Wiggers action failed during playback')
 page.locator('#guidedV112Seek').click()
 ck(not page.evaluate('heartState.playing'),
    'explicit native Timeline seek failed to pause playback')
 ck(page.evaluate('CardiacDashboard.view')=='wiggers',
    'explicit seek should retain current visualization')
 ck(page.locator('#ecgCanvas').is_visible(),'ECG no longer visible')
 page.locator('#guidedV112Toggle').click()
 ck(page.locator('#guidedV112Panel').is_hidden(),'guide cannot close')
 ck(page.locator('.dashboard-clinical').is_visible(),
    'original clinical nursing panel did not return')
 ck(page.locator('#wiggersDeepDive').count()==1,
    'full six-part clinical content removed')
 page.locator('#dashboardDensityBtn').click()
 ck(page.evaluate('CardiacDashboard.density')=='expanded','full info toggle broken')
 page.locator('#dashboardDensityBtn').click()
 ck(page.evaluate('CardiacDashboard.density')=='compact','compact restore broken')

 # Desktop and mobile layouts with guide open, and local Wiggers scrolling.
 for width in (1440,1366,1024,768,390,360):
    page.set_viewport_size({'width':width,'height':800})
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       f'page overflow before guide at {width}px')
    page.locator('#guidedV112Toggle').click()
    ck(page.locator('#guidedV112Panel').is_visible(),
       f'guided section not visible at {width}px')
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       f'page overflow with guide at {width}px')
    for control in ('#guidedV112Previous','#guidedV112Next',
                    '#guidedV112ViewWiggers','#guidedV112Seek'):
       ck(page.locator(control).is_visible(),f'button missing at {width}: {control}')
       box=page.locator(control).bounding_box()
       ck(box and box['height']>=39,f'unsafe tap target at {width}: {control}')
    if width==390:
       page.screenshot(path=str(SHOTS/'03-guided-mobile-390.png'),
                       full_page=True,animations='disabled')
    page.locator('#guidedV112Toggle').click()
    ck(page.locator('.dashboard-clinical').is_visible(),
       f'closing guide failed at {width}')
 ck(not errs,'Uncaught JavaScript errors: '+str(errs))
 print(f'PASS {n} v1.12 Patch2 browser checks: no implicit clock mutation, '
       '50 native seeks, preserved modes and responsive navigation.')
 browser.close()
