"""v1.11.1 compact-first stabilization: true-index browser regression.

Do not replace legacy tests. This checks that changing presentation density
cannot touch clocks, Play/Pause/Reset, clinical text, or Wiggers mode.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SCREENSHOTS=ROOT/'preview-v1111'
SCREENSHOTS.mkdir(exist_ok=True)
n=0
def ck(ok,message):
 global n
 n+=1
 assert ok,message

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',
   args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1366,'height':768})
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.goto((ROOT/'index.html').as_uri(),wait_until='load')
 page.wait_for_function('!!window.CardiacDashboard && !!window.CardiacLearning')

 density=page.locator('#dashboardDensityBtn')
 ck(any(v in page.locator('h1').inner_text() for v in ('v1.11.1','v1.12')),'new patch title')
 ck(page.evaluate('CardiacDashboard.density')=='compact','default compact density')
 ck(density.get_attribute('aria-pressed')=='false','compact aria state')
 ck(density.is_visible(),'full information toggle visible')
 ck(page.locator('#dashboardV111').count()==1,'dashboard uniquely labelled')
 ck(page.locator('.dashboard-v111>.measurements-panel').is_visible(),
   'measurements must remain permanently visible')
 ck(page.locator('#ecgCanvas').is_visible(),'ECG permanently visible')
 ck(page.locator('#dashboardPhysiology').is_visible(),'clinical physiology absent')
 ck(page.locator('#dashboardNursing').is_visible(),'nursing summary absent')
 ck(page.locator('#dashboardElectrical').is_visible(),'electrical phase absent')
 ck(page.locator('#dashboardMechanical').is_visible(),'mechanical stage absent')
 ck(page.locator('#dashboardEvent').is_visible(),'ECG event summary absent')
 for selector in ('.dashboard-ecg-details','.dashboard-phase-details',
                  '.dashboard-event-details','#wiggersDeepDive'):
    ck(not page.locator(selector).evaluate('(el)=>el.open'),
       f'nonessential lengthy detail opens by default: {selector}')
 for element in ('#ecgExplanationText','#phaseDescription','#eventSyncStatus',
                 '#measurementHeartRate','#measurementRR','#measurementPR',
                 '#measurementQRS','#measurementQT','#measurementQTc'):
    ck(page.locator(element).count()==1,f'dynamic DOM node missing: {element}')
 ck(page.locator('.dashboard-v111 .measurement-list small').first.is_hidden(),
    'compact references should be hidden, not deleted')

 def snapshot():
    return page.evaluate("""() => ({
       a:heartState.physiologicalTime,b:heartState.visualizationTime,
       t:heartState.cycleStartTime,sweep:heartState.sweepPosition,
       hr:heartRate,playing:heartState.playing,mode:CardiacMechanical.mode,
       selected:CardiacLearning.activePreset,view:CardiacDashboard.view
    })""")

 original=snapshot()
 compact_height=page.evaluate('document.documentElement.scrollHeight')
 page.screenshot(path=str(SCREENSHOTS/'01-compact-desktop.png'),full_page=True,animations='disabled')
 worktop=page.locator('.dashboard-workspace').evaluate('el=>el.getBoundingClientRect().top')
 ck(worktop<690,f'compact desktop visualization starts too low: {worktop}')
 density.click()
 ck(page.evaluate('CardiacDashboard.density')=='expanded','expanded state missing')
 ck(density.get_attribute('aria-pressed')=='true','expanded aria state')
 ck('핵심 보기' in density.inner_text(),'restore label missing')
 for selector in ('.dashboard-ecg-details','.dashboard-phase-details','.dashboard-event-details'):
    ck(page.locator(selector).evaluate('(el)=>el.open'),f'expanded did not reveal {selector}')
 ck(page.locator('.dashboard-v111 .measurement-list small').first.is_visible(),
    'normal interval reference was lost in expanded mode')
 full_height=page.evaluate('document.documentElement.scrollHeight')
 page.screenshot(path=str(SCREENSHOTS/'02-full-desktop.png'),full_page=True,animations='disabled')
 ck(full_height>compact_height+100,
    f'compact view not materially shorter: compact={compact_height},full={full_height}')
 ck(snapshot()==original,'showing full clinical information mutated simulation')
 density.click()
 ck(page.evaluate('CardiacDashboard.density')=='compact','return compact failed')
 ck(page.evaluate('document.documentElement.scrollHeight')<=compact_height+8,
    'return compact did not recover initial height')
 ck(snapshot()==original,'returning compact mutated simulation')
 for selector in ('.dashboard-ecg-details','.dashboard-phase-details','.dashboard-event-details'):
    ck(not page.locator(selector).evaluate('(el)=>el.open'),
       f'compact mode did not collapse old detail {selector}')

 # Selection of an ECG wave reveals just its own full explanatory source.
 page.locator('[data-ecg-component="QRS"]').click()
 ck(page.locator('.dashboard-ecg-details').evaluate('(el)=>el.open'),
    'clicking QRS should reveal original clinical description')
 ck('QRS' in page.locator('#ecgExplanationTitle').inner_text(),
    'original ECG explanation event broken')
 ck(not page.locator('.dashboard-phase-details').evaluate('(el)=>el.open'),
    'QRS click unexpectedly opened unrelated long phase text')
 ck(snapshot()==original,'ECG component selection mutated simulation')

 # Existing native disclosure preferences are separate from new density.
 page.locator('#wiggersDeepDive summary').click()
 page.wait_for_function('document.getElementById("wiggersDeepDive").open')
 page.locator('#timeSlider').evaluate("""el=>{
    el.value='42';el.dispatchEvent(new Event('input',{bubbles:true}));
 }""")
 before=snapshot()
 ck(before['a']>0 and before['b']>0,'Timeline no longer seeks A/B')
 density.click()
 density.click()
 ck(snapshot()==before,'density change rewound the sought A/B clocks')
 ck(page.locator('#wiggersDeepDive').evaluate('(el)=>el.open'),
    'long nursing details preference lost when switching density')
 ck(page.locator('#dashboardMechanical').inner_text()!='Ready',
    'mechanical stage not updated after seeking')
 ck(page.locator('#dashboardEvent').inner_text()!='',
    'ECG event became blank')
 ck(len(page.locator('#learningNursing').inner_text())>70,
    'original full nursing explanation lost')
 ck(len(page.locator('#learningCaution').inner_text())>30,
    'medical-model limits missing')

 # Switch all three visualizations, focus Wiggers and prove state identity.
 page.locator('#dashboardWiggersBtn').click()
 ck(page.locator('#wiggersChart').is_visible(),'Wiggers graph not visible')
 page.screenshot(path=str(SCREENSHOTS/'03-wiggers-desktop.png'),full_page=True,animations='disabled')
 ck(page.locator('#wiggersMarkers [data-event]').count()==4,
    'valve event markers lost')
 active=snapshot()
 page.locator('#dashboardFocusBtn').click()
 ck(snapshot()==active,'graph focus changed canonical state')
 page.locator('#dashboardFocusBtn').click()
 density.click()
 density.click()
 ck(snapshot()==active,'density toggle changed active Wiggers state')
 page.locator('#mechanicalModeBtn').click()
 ck(page.locator('#mechanicalView').is_visible(),'Mechanical mode missing')
 page.locator('#electricalModeBtn').click()
 ck(page.locator('#heartSVG').is_visible(),'Electrical mode missing')
 ck(page.locator('#ecgCanvas').is_visible(),'ECG lost during tab switching')

 # Presets delegate to the existing HR source and Reset retains view/density.
 for key,hr in [('normal',72),('bradycardia',50),('tachycardia',120)]:
    page.locator(f'[data-learning-preset="{key}"]').click()
    ck(page.evaluate('heartRate')==hr,f'rate preset {key} regressed')
 page.locator('#heartRateSlider').evaluate("""el=>{
    el.value='80';el.dispatchEvent(new Event('input',{bubbles:true}));
 }""")
 ck(page.evaluate('CardiacLearning.activePreset') is None,
    'custom HR did not reset learning preset')
 page.locator('#playBtn').click()
 page.wait_for_timeout(150)
 ck(page.evaluate('heartState.playing'),'Play stopped working')
 page.locator('#pauseBtn').click()
 ck(not page.evaluate('heartState.playing'),'Pause stopped working')
 page.locator('#resetBtn').click()
 ck(page.evaluate('CardiacDashboard.isReady'),'Reset did not reach Ready')
 ck(page.evaluate('CardiacDashboard.density')=='compact','Reset changed learner view density')
 ck(page.locator('#dashboardEvent').inner_text()=='Ready','Reset ECG event summary stale')
 ck(page.locator('#dashboardMechanical').inner_text()=='Ready',
    'Reset mechanical status stale')
 ck(page.locator('#wiggersDeepDive').evaluate('(el)=>el.open'),
    'Reset discarded manually opened full nursing text')

 for width in (1440,1366,1024,768,390,360):
    page.set_viewport_size({'width':width,'height':768})
    dims=page.evaluate("""() => ({
       width:innerWidth,document:document.documentElement.scrollWidth,
       chartWidth:document.querySelector('.wiggers-chart-scroll').clientWidth,
       chartScroll:document.querySelector('.wiggers-chart-scroll').scrollWidth
    })""")
    ck(dims['document']<=width+2,
       f'document overflow at {width}px: {dims}')
    ck(page.locator('#dashboardDensityBtn').is_visible(),
       f'density button hidden at {width}')
    ck(page.locator('#dashboardWiggersBtn').is_visible(),
       f'three-view switch hidden at {width}')
    page.locator('#dashboardWiggersBtn').click()
    ck(page.locator('#wiggersChart').is_visible(),
       f'Wiggers graph clipped or hidden at {width}')
    if width==390:
       page.screenshot(path=str(SCREENSHOTS/'04-wiggers-mobile-390.png'),
                       full_page=True,animations='disabled')
    if width<700:
       graph=page.locator('.wiggers-chart-scroll').evaluate("""el=>({
          client:el.clientWidth,scroll:el.scrollWidth
       })""")
       ck(graph['scroll']>graph['client'],
          f'Wiggers no longer scrolls internally at {width}: {graph}')
    page.locator('#electricalModeBtn').click()

 ck(not errors,f'JavaScript errors: {errors}')
 print(f"PASS {n} v1.11.1 assertions; desktop compact/full page heights "
       f"{compact_height}/{full_height}px; difference {full_height-compact_height}px; "
       f"workspace y={worktop:.0f}px. Clinical details, A/B, modes and mobile preserved.")
 browser.close()
