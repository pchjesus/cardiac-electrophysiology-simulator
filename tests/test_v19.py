"""v1.9 Electrical/Mechanical model, state integration and v1.8 regression."""
from pathlib import Path
import math
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
base=root/'backups/v1.9/BASELINE_v1.8_FINAL'
checks=0

def check(x,why):
 global checks
 checks+=1
 assert x,why

with sync_playwright() as w:
 browser=w.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 pages={}; errors={}
 for name,path in [('v19',root),('v18',base)]:
  page=browser.new_page(viewport={'width':1366,'height':900}, device_scale_factor=1)
  errors[name]=[]
  page.on('pageerror',lambda ex,name=name:errors[name].append(str(ex)))
  page.set_content((path/'index.html').read_text(encoding='utf-8'))
  page.add_style_tag(content=(path/'style.css').read_text(encoding='utf-8'))
  page.add_script_tag(content=(path/'script.js').read_text(encoding='utf-8'))
  if name=='v19':page.add_script_tag(content=(path/'mechanics.js').read_text(encoding='utf-8'))
  pages[name]=page
 page=pages['v19'];old=pages['v18']
 check(not errors['v19'],f'v19 load errors {errors}')
 check(page.locator('#heartSVG').is_visible(),'Electrical visual not default')
 check(not page.locator('#mechanicalView').is_visible(),'Mechanical visible by default')
 check(page.locator('#electricalModeBtn').get_attribute('aria-pressed')=='true','electrical toggle state')
 check(page.locator('#mechanicalPhase').text_content()=='준비','mechanical ready defaults')
 for hr in range(30,181):
  for pg in [old,page]:
   pg.locator('#heartRateSlider').evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}))}',hr)
  snap=page.evaluate('''() => {
    const t=getActiveTiming(),m=window.CardiacMechanical;
    const tm=m.getMechanicalTiming(t),phases=[
      (0+tm.atrialStart)/2,(tm.atrialStart+tm.contractionStart)/2,
      (tm.contractionStart+tm.ejectionStart)/2,
      (tm.ejectionStart+tm.ejectionEnd)/2,
      (tm.ejectionEnd+tm.relaxationEnd)/2,
      (tm.relaxationEnd+tm.rr)/2];
    return {timing:tm,states:phases.map(x=>m.getMechanicalState(x,t)),
      speed:animationSpeed,rr:t.rr,b:heartState.visualizationTime};
  }''')
  boundaries=snap['timing'];states=snap['states']
  check(0<boundaries['atrialStart']<boundaries['contractionStart']<boundaries['ejectionStart']<boundaries['ejectionEnd']<boundaries['relaxationEnd']<boundaries['rr'],f'bad timing {hr}: {boundaries}')
  check(math.isclose(boundaries['rr'],60000/hr,abs_tol=1e-7),f'RR {hr}')
  check([a['stage'] for a in states]==['filling','atrial_systole','isovolumetric_contraction','ejection','isovolumetric_relaxation','filling'],f'phases {hr} {states}')
  for st in states:
   check(0.47<=st['ventricularVolume']<=1.0000001,f'volume {hr} {st}')
   val=st['valves'];ps=st['pressure']
   check(val['mitral']==val['tricuspid']==(ps['atrial']>ps['ventricular']),f'av pressure valve mismatch {hr}')
   check(val['aortic']==val['pulmonary']==(ps['ventricular']>ps['arterial']),f'outflow pressure mismatch {hr}')
   check(not(val['aortic'] and val['mitral']),f'both valve sets open {hr}')
   if st['stage'].startswith('isovolumetric'):
    check(st['flow']=='none' and not val['aortic'] and not val['mitral'],f'isovolumetric contradiction {hr}')
   if st['stage']=='ejection':check(st['flow']=='ejection' and val['aortic'],f'not ejecting {hr}')
  # The new module should never alter ECG waveform, rate, B speed or sweep.
  for pg in [page,old]:
   pg.locator('#timeSlider').evaluate('(el)=>{el.value=41;el.dispatchEvent(new Event("input",{bubbles:true}))}')
   pg.evaluate('updateSimulation(30)')
  e19=page.evaluate('''() => ({A:heartState.physiologicalTime,B:heartState.visualizationTime,speed:animationSpeed,
    sweep:heartState.sweepPosition,event:heartState.currentECGEvent,measures:getECGMeasurements(),
    currentStep:heartState.currentStep,curve:[0,5,60,150,300].map(x=>ecgValue(x))})''')
  e18=old.evaluate('''() => ({A:heartState.physiologicalTime,B:heartState.visualizationTime,speed:animationSpeed,
    sweep:heartState.sweepPosition,event:heartState.currentECGEvent,measures:getECGMeasurements(),
    currentStep:heartState.currentStep,curve:[0,5,60,150,300].map(x=>ecgValue(x))})''')
  check(e19==e18,f'v1.8 electrical regression HR {hr}: {e19} != {e18}')
 # UI switching and paused seeking, mechanical rendering
 page.locator('#mechanicalModeBtn').click()
 check(page.locator('#mechanicalView').is_visible(),'mechanical mode unavailable')
 check(not page.locator('#heartSVG').is_visible(),'conduction not hidden in mechanical mode')
 check(page.locator('#mechanicalModeBtn').get_attribute('aria-pressed')=='true','mechanical button ARIA')
 check(page.locator('#mechanicalPhase').text_content()!='','mechanical phase blank')
 for frac,expect in [(0.1,'atrial_systole'),(0.2,'atrial_systole'),(0.43,'ejection'),(0.68,'filling')]:
  # Select actual computed phase midpoint; converts phase to timeline percentage.
  target=page.evaluate('''(stage) => {
   const t=window.CardiacMechanical.getMechanicalTiming();
   const range=stage==='atrial_systole'?[t.atrialStart,t.contractionStart]:stage==='ejection'?[t.ejectionStart,t.ejectionEnd]:[t.relaxationEnd,t.rr];
   return (range[0]+range[1])*50/t.rr;
  }''',expect)
  page.locator('#timeSlider').evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}))}',target)
  check(page.evaluate('window.CardiacMechanical.currentState.stage')==expect,f'Timeline stage seek {expect}')
  check(page.locator('#mechanicalPhase').text_content()!='준비',f'phase not rendered {expect}')
  check(page.locator('#mechanicalSVG .flow-dot[style*="opacity: 1"]').count()>0, 'Flow particles missing when valve flow active')
 page.locator('#resetBtn').click()
 check(page.locator('#mechanicalModeBtn').get_attribute('aria-pressed')=='true','reset changed mode')
 check(page.locator('#mechanicalPhase').text_content()=='준비','reset not ready')
 check(page.evaluate('heartState.physiologicalTime===0 && !heartState.playing'),'reset clock failed')
 page.locator('#playBtn').click()
 page.wait_for_timeout(240)
 page.locator('#pauseBtn').click()
 check(page.evaluate('heartState.physiologicalTime>0 && !heartState.playing'),'mechanical active playback failed')
 check(page.locator('#mechanicalPhase').text_content()!='준비','mechanical not refreshed during play')
 page.locator('#electricalModeBtn').click()
 check(page.locator('#heartSVG').is_visible() and not page.locator('#mechanicalView').is_visible(),'could not return electrical')
 # both desktop and narrow viewport render without a newly introduced overflow relative to old UI
 page.set_viewport_size({'width':390,'height':844});old.set_viewport_size({'width':390,'height':844})
 v19width=page.evaluate('document.documentElement.scrollWidth')
 v18width=old.evaluate('document.documentElement.scrollWidth')
 check(v19width<=v18width+2,f'mobile overflow worsened {v19width} vs {v18width}')
 page.locator('#mechanicalModeBtn').click()
 check(page.locator('#mechanicalSVG').is_visible(),'mechanical mobile svg not visible')
 page.screenshot(path=str(root/'v19_mobile.png'),full_page=True)
 page.set_viewport_size({'width':1366,'height':900});page.screenshot(path=str(root/'v19_desktop.png'),full_page=True)
 check(not errors['v19'],f'JS page errors {errors}')
 print(f'PASS {checks} v1.9 model+regression checks (HR 30-180, mode/seek/play/reset), errors={errors["v19"]}; mobile widths v19={v19width}, v18={v18width}')
 browser.close()
