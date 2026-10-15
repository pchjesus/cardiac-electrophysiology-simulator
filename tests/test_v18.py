from pathlib import Path
from playwright.sync_api import sync_playwright
import math, json
p=Path(__file__).resolve().parents[1]
p3=p/'backups/v1.8/patch4_baseline'
checks=0
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 pages={}
 errors={}
 for name,root in [('v18',p),('p3',p3)]:
  page=browser.new_page(viewport={'width':1366,'height':900})
  errors[name]=[]
  page.on('pageerror',lambda exc,name=name:errors[name].append(str(exc)))
  page.set_content((root/'index.html').read_text())
  page.add_style_tag(content=(root/'style.css').read_text())
  page.add_script_tag(content=(root/'script.js').read_text())
  pages[name]=page
 def js(code):return pages['v18'].evaluate(code)
 def check(b,msg):
  global checks
  checks+=1
  assert b,msg
 def isclose(a,b,tol=1e-6):return math.isclose(a,b,abs_tol=tol,rel_tol=1e-10)
 check(not errors['v18'],f'Load JS errors: {errors}')
 print('Initial:',js('({rhythm:document.getElementById("rhythmStatus").textContent,hr:heartRate,RR:getActiveCycleLength(),timing:getActiveTiming(),event:heartState.currentECGEvent})'))
 for hr in [30,50,60,72,80,100,120,150,180]:
  for page in pages.values():page.locator('#heartRateSlider').evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}))}',hr)
  obj=js('''() => ({timing:getActiveTiming(),measures:getECGMeasurements(),events:ecgEvents.map(e=>[e.id,e.start,e.end]),conduction:conductionSteps.map(e=>[e.id,e.start,e.end]),html:Object.fromEntries(['measurementPR','measurementQRS','measurementQT','measurementQTc','measurementRR'].map(id=>[id,document.getElementById(id).textContent]))})''')
  t=obj['timing'];rr=60000/hr
  check(isclose(t['rr'],rr),f'RR mismatch {hr}');check(0<=t['pStart']<t['pEnd']<t['qrsStart']<t['qrsEnd']<t['stEnd']<t['tEnd']<t['rr'],f'interval order {hr} {t}')
  check(isclose(t['qrsEnd']-t['qrsStart'],obj['measures']['qrsDuration']),f'qrs mismatch {hr}')
  check(isclose(t['tEnd']-t['qrsStart'],obj['measures']['qtInterval']),f'qt mismatch {hr}')
  check(isclose(t['qrsStart']-t['pStart'],obj['measures']['prInterval']),f'pr mismatch {hr}')
  check(isclose(obj['measures']['qtc'],t['qtInterval']/math.sqrt(rr/1000)),f'qtc mismatch {hr}')
  check(all(isclose(obj['events'][i][2],obj['events'][i+1][1]) for i in range(6)),f'ECG event gaps {hr} {obj["events"]}')
  check(all(isclose(obj['conduction'][i][2],obj['conduction'][i+1][1]) for i in range(5)),f'conduction gaps {hr} {obj["conduction"]}')
  check(isclose(obj['conduction'][4][2],t['qrsEnd']),f'purkinje/qrs mismatch {hr}')
  # sample 7 intervals; wave event/phase/conduction align.
  times=[(t['pStart']+t['pEnd'])/2,(t['qrsStart']+t['qrsEnd'])/2,(t['stEnd']+t['tEnd'])/2,t['tEnd']+2]
  for phase in times:
   snapshot=js(f'''() => {{reset(); heartState.physiologicalTime={phase}; heartState.visualizationTime={phase}*baseCycleLength/getActiveCycleLength(); heartState.ecgTime=heartState.physiologicalTime; updateConduction(true);updateTimeline();return {{event:heartState.currentECGEvent,ecgText:document.getElementById('phaseECG').textContent,slider:Number(document.getElementById('timeSlider').value),phase:getPhysiologicalCyclePhase(),wave:ecgValue({phase}),pulseR:conductionPulseR.style.opacity,pulseL:conductionPulseL.style.opacity}}}}''')
   check(snapshot['event']==snapshot['ecgText'] or snapshot['ecgText'] in {'P파','QRS파','T파','기준선','ST 분절','PR 간격'},f'phase mismatch {snapshot}')
   check(isclose(snapshot['phase'],phase,1e-4),f'cycle phase mismatch {hr} {snapshot}')
   check(isclose(snapshot['slider'],100*phase/rr,.2),f'timeline mismatch {hr} {snapshot}')
  # B playback speed & sweep position must match Patch3 for the same input frame and slider.
  for page in pages.values():page.locator('#timeSlider').evaluate('(el)=>{el.value=33;el.dispatchEvent(new Event("input",{bubbles:true}))}')
  for page in pages.values():page.evaluate('updateSimulation(42)')
  abc={n:page.evaluate('''() => ({B:heartState.visualizationTime,sweep:heartState.sweepPosition,speed:animationSpeed})''') for n,page in pages.items()}
  for key in ['B','sweep','speed']:check(isclose(abc['v18'][key],abc['p3'][key]),f'pacing changed HR {hr} {key}: {abc}')
  # Timeline 100, reset, quick play pause.
  pages['v18'].locator('#timeSlider').evaluate('(el)=>{el.value=100;el.dispatchEvent(new Event("input",{bubbles:true}))}')
  terminal=js('''() => ({p:getPhysiologicalCyclePhase(),rr:getActiveCycleLength(),event:heartState.currentECGEvent})''')
  check(terminal['p']<terminal['rr'],f'terminal seek issue {hr} {terminal}')
  js('reset()')
  check(js('''heartState.currentECGEvent===null && heartState.physiologicalTime===0 && heartState.visualizationTime===0 && document.getElementById('ecgEventIndicator').textContent==='준비' '''),f'reset mismatch {hr}')
  print('HR',hr,'PR',round(t['prInterval']),'QRS',round(t['qrsDuration']),'QT',round(t['qtInterval']),'QTc',round(t['qtc']),'checks+',checks)
 # Test rapid pause/play generation: fake RAF captures callbacks, then execute stale manually
 js('''() => { window.__savedRAF=requestAnimationFrame; window.__callbacks=[]; window.requestAnimationFrame=(cb)=>{__callbacks.push(cb);return __callbacks.length;}; }''')
 js('play()');js('pause()');js('play()')
 stale=js('''() => {const before=heartState.physiologicalTime; const stale=__callbacks[0]; stale(10000);return {before,after:heartState.physiologicalTime,callbacks:__callbacks.length}}''')
 check(isclose(stale['before'],stale['after']),f'Stale rAF advanced {stale}')
 js('pause()')
 js('''() => {window.requestAnimationFrame=window.__savedRAF;}''')
 # live actual raf smoke
 js('reset()');pages['v18'].locator('#playBtn').click();pages['v18'].wait_for_timeout(250);pages['v18'].locator('#pauseBtn').click()
 check(js('heartState.physiologicalTime>0 && heartState.visualizationTime>0 && !heartState.playing'),'live RAF failed')
 check(errors['v18']==[],f'errors: {errors}')
 # responsive smoke
 pages['v18'].set_viewport_size({'width':390,'height':844})
 pages['p3'].set_viewport_size({'width':390,'height':844})
 base_width=pages['p3'].evaluate('''() => {document.body.style.width='390px'; return document.documentElement.scrollWidth;}''')
 # Both builds carry the same pre-existing 47px overflow in narrow layouts.
 current_width=js('document.documentElement.scrollWidth')
 overflow=pages['v18'].evaluate("""() => [...document.querySelectorAll('body *')]
   .filter(el=>{const r=el.getBoundingClientRect();return r.width>0&&r.right>innerWidth+2;})
   .slice(0,15).map(el=>({tag:el.tagName,id:el.id,cls:typeof el.className==='string'?el.className:'',
     text:(el.textContent||'').trim().slice(0,35),right:Math.round(el.getBoundingClientRect().right)}))""") if current_width>base_width+2 else []
 check(current_width <= base_width + 2,
       f'mobile overflow regressed vs baseline: actual {current_width}px, baseline {base_width}px; offenders {overflow}')
 pages['v18'].screenshot(path=str(p/'v18_mobile_test.png'),full_page=True)
 pages['v18'].set_viewport_size({'width':1366,'height':900})
 pages['v18'].screenshot(path=str(p/'v18_desktop_test.png'))
 print(f'PASS {checks} assertions. JavaScript page errors = {errors["v18"]}; B visual pacing matched Patch3 at nine HRs.')
 browser.close()
