"""v1.11 integrated learning dashboard regression and safety acceptance.
Launch the REAL index.html with all scripts; v1.8-v1.10 harnesses still test
the pre-enhancement API independently to preserve original behavior.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
checks=0
def ck(ok,label):
 global checks
 checks+=1
 assert ok,label

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',
   args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1366,'height':768})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'index.html').as_uri())
 page.wait_for_function('!!window.CardiacDashboard && !!window.CardiacLearning')
 ck('v1.11' in page.locator('h1').inner_text(),'version headline')
 ck(page.locator('.app.dashboard-active').count()==1,'progressive dashboard failed')
 ck(page.locator('.dashboard-commands #playBtn').count()==1,'existing Play button not moved')
 ck(page.locator('.dashboard-commands #timeSlider').count()==1,'old Timeline not moved')
 ck(page.locator('.dashboard-commands #heartRateSlider').count()==1,'old HR slider not moved')
 ck(page.locator('.dashboard-presets [data-learning-preset]').count()==3,'presets not moved as originals')
 ck(page.locator('.dashboard-v111>.ecg-panel #ecgCanvas').is_visible(),'ECG no longer always visible')
 ck(page.locator('.dashboard-v111>.measurements-panel #measurementQTc').count()==1,
    'measurements not preserved')
 ck(page.locator('#phaseTitle').count()==1 and page.locator('#ecgEventIndicator').count()==1,
    'original event/phase nodes duplicated or removed')
 ck(page.locator('.dashboard-inspector #wiggersDeepDive').count()==1,
    'long-form lesson not relocated')
 ck(page.locator('.dashboard-visual #mechanicalModeBtn').is_visible(),'mode button inaccessible')
 ck(page.locator('#heartSVG').is_visible(),'default Electrical SVG missing')
 ck(not page.locator('#mechanicalView').is_visible(),'Mechanical is not hidden initially')
 ck(not page.locator('#wiggersChart').is_visible(),'Wiggers is not hidden initially')
 ck(page.evaluate('CardiacDashboard.view')=='electrical','default dashboard tab')
 ck(page.evaluate('CardiacDashboard.isReady'),'initial Ready status')
 ck('Ready' in page.locator('#dashboardElectrical').inner_text(),'initial electrical Ready')
 ck('Ready' in page.locator('#dashboardMechanical').inner_text(),'initial mechanical Ready')

 # The three views are only presentations; the canonical A/B and manual
 # controls must never reset when clicking between them.
 page.locator('#timeSlider').evaluate("""el=>{
   el.value='38';el.dispatchEvent(new Event('input',{bubbles:true}));
 }""")
 before=page.evaluate("""() => ({
    a:heartState.physiologicalTime,b:heartState.visualizationTime,
    hr:heartRate,playing:heartState.playing,cycle:heartState.cycleStartTime,
    sweep:heartState.sweepPosition
 })""")
 ck(before['a']>0 and before['b']>0,'seek did not update A/B')
 page.locator('#dashboardWiggersBtn').click()
 ck(page.evaluate('CardiacDashboard.view')=='wiggers','Wiggers tab not selected')
 ck(page.evaluate("document.getElementById('wiggersDetails').open"),
    'Wiggers native disclosure not opened')
 ck(page.locator('#wiggersChart').is_visible(),'Wiggers plot not visible')
 ck(page.locator('#wiggersMarkers [data-event]').count()==4,'Valve markers lost')
 ck('ms' in page.locator('#wiggersCurrentTime').inner_text(),'Wiggers time missing')
 ck(page.locator('#heartSVG').is_hidden(),'Electrical view still taking dashboard space')
 ck(before==page.evaluate("""() => ({
    a:heartState.physiologicalTime,b:heartState.visualizationTime,
    hr:heartRate,playing:heartState.playing,cycle:heartState.cycleStartTime,
    sweep:heartState.sweepPosition
 })"""),'Wiggers tab altered A/B state')
 page.locator('#mechanicalModeBtn').click()
 ck(page.evaluate('CardiacDashboard.view')=='mechanical','Mechanical tab selection')
 ck(page.locator('#mechanicalView').is_visible(),'Mechanical art not displayed')
 ck(not page.evaluate("document.getElementById('wiggersDetails').open"),
    'Wiggers remained open offscreen, wasting animation frame work')
 ck(page.locator('#wiggersChart').is_hidden(),'Wiggers not visually hidden')
 ck(before==page.evaluate("""() => ({
    a:heartState.physiologicalTime,b:heartState.visualizationTime,
    hr:heartRate,playing:heartState.playing,cycle:heartState.cycleStartTime,
    sweep:heartState.sweepPosition
 })"""),'Mechanical tab altered A/B state')
 page.locator('#electricalModeBtn').click()
 ck(page.locator('#heartSVG').is_visible(),'Electrical mode cannot be restored')
 ck(page.evaluate('CardiacDashboard.view')=='electrical','Electrical tab state')
 ck(page.locator('#ecgCanvas').is_visible(),'ECG disappeared during tab switch')

 # Keyboard view navigation must reuse the same native mode handlers.
 page.locator('#electricalModeBtn').focus()
 page.keyboard.press('ArrowRight')
 ck(page.evaluate('CardiacDashboard.view')=='mechanical','Right arrow tab step')
 page.keyboard.press('End')
 ck(page.evaluate('CardiacDashboard.view')=='wiggers','End keyboard tab navigation')
 page.keyboard.press('Home')
 ck(page.evaluate('CardiacDashboard.view')=='electrical','Home keyboard tab navigation')

 # Check 3 user presets, age-related category thresholds and independent
 # custom HR slider without adding a second rate state.
 for preset,hr in [('normal',72),('bradycardia',50),('tachycardia',120)]:
    page.locator('[data-learning-preset="'+preset+'"]').click()
    ck(page.evaluate('heartRate')==hr,f'Preset failed {preset}')
    ck(page.evaluate('CardiacLearning.activePreset')==preset,f'Preset state lost {preset}')
    ck(page.locator('[data-learning-preset="'+preset+'"]').get_attribute('aria-pressed')=='true',
       f'Presets not aria pressed {preset}')
 page.locator('#heartRateSlider').evaluate("""el=>{
   el.value=93;el.dispatchEvent(new Event('input',{bubbles:true}));
 }""")
 ck(page.evaluate('heartRate')==93,'custom HR not authoritative')
 ck(page.evaluate('CardiacLearning.activePreset') is None,'manual HR did not reset scenario')

 page.locator('#wiggersDeepDive summary').click()
 page.wait_for_function("document.getElementById('wiggersDeepDive').open")
 ck(page.locator('#learningNursing').is_visible(),'Deep nursing paragraph not available')
 ck(len(page.locator('#learningNursing').inner_text())>70,'Nursing teaching text insufficient')
 ck(page.locator('#dashboardPhysiology').inner_text().strip()!='',
   'Summary panel physiology empty')
 ck(page.locator('#dashboardNursing').inner_text().strip()!='',
   'Summary panel nursing empty')
 ck(page.locator('#dashboardMechanical').inner_text()!='Ready','Mechanical phase not synchronized')
 ck(page.locator('#wiggersDeepDive').is_visible(),'Deep learning must be independent of Wiggers tab')

 page.locator('#playBtn').click()
 page.wait_for_timeout(150)
 ck(page.evaluate('heartState.playing'),'Play regression')
 page.locator('#dashboardWiggersBtn').click()
 page.wait_for_timeout(140)
 ck(page.evaluate('heartState.playing'),'Changing views paused playback')
 page.locator('#pauseBtn').click()
 ck(not page.evaluate('heartState.playing'),'Pause regression')
 paused=page.evaluate('heartState.physiologicalTime')
 page.wait_for_timeout(75)
 ck(page.evaluate('heartState.physiologicalTime')==paused,'A clock still advances while paused')
 ck(page.locator('#wiggersChart').is_visible(),'Wiggers lost plot during playback')

 page.locator('#resetBtn').click()
 ck(page.evaluate('CardiacDashboard.view')=='wiggers','Reset changed chosen tab')
 ck(page.evaluate('CardiacDashboard.isReady'),'Reset did not restore Ready')
 ck(page.locator('#dashboardElectrical').inner_text()=='Ready','Reset Electrical inspector stale')
 ck(page.locator('#dashboardMechanical').inner_text()=='Ready','Reset Mechanical inspector stale')
 ck(page.locator('#wiggersCurrentStage').inner_text()=='Ready','Wiggers Ready regression')
 ck(page.evaluate("document.getElementById('wiggersDeepDive').open"),
    'Reset discarded learner disclosure preference')

 # Existing guide and categorized patch history remain independent nonmodal
 # overlays with explicit keyboard dismissal.
 for trigger,panel in [('#patchNotesBtn','#patchNotesPanel'),('#userGuideBtn','#userGuidePanel')]:
    page.locator(trigger).click()
    ck(page.locator(panel).is_visible(),'Header overlay did not open '+panel)
    page.keyboard.press('Escape')
    ck(page.locator(panel).is_hidden(),'Header popup Escape failed '+panel)

 # At low widths the DOCUMENT must fit the viewport. The min 720px
 # Wiggers SVG scrolls within its own bounded container.
 for width in (1440,1366,1024,768,390,360):
    page.set_viewport_size({'width':width,'height':850})
    dims=page.evaluate("""() => {
      const graph=document.querySelector('.wiggers-chart-scroll');
      return {
       viewport:innerWidth,document:document.documentElement.scrollWidth,
       body:document.body.scrollWidth,graphWidth:graph.clientWidth,
       graphScroll:graph.scrollWidth,docClient:document.documentElement.clientWidth
      };
    }""")
    ck(dims['document']<=width+2,f'document overflows viewport={width}: {dims}')
    ck(dims['graphScroll']>dims['graphWidth'] if width<700 else dims['graphWidth']>0,
       f'Wiggers local scroll broken {width}: {dims}')
    ck(page.locator('#ecgCanvas').is_visible(),f'ECG is hidden at {width}')
    ck(page.locator('#dashboardWiggersBtn').is_visible(),f'View tabs are hidden at {width}')

 ck(not errors,'JavaScript errors: '+str(errors))
 print(f'PASS {checks} v1.11 checks: progressive dashboard, full A/B identity, '
       'three views, keyboard, clinical lessons, presets, reset, popups and mobile widths.')
 browser.close()
