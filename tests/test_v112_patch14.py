"""v1.12 Patch 14: available-width mechanics, readable live text, non-overlay notes."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/"preview-v112p14"
SHOTS.mkdir(exist_ok=True)
checks=0

def ck(condition,message):
    global checks
    assert condition,message
    checks+=1

def snapshot(page):
    return page.evaluate("""() => ({
      a:heartState.physiologicalTime,b:heartState.visualizationTime,
      hr:heartRate,playing:heartState.playing
    })""")

def geometry(page):
    return page.evaluate("""() => {
      const box=s=>document.querySelector(s).getBoundingClientRect();
      const s=box('#mechanicalSVG'),r=box('.mechanical-readout');
      const n=box('#mechanicalModelInfo>summary'),body=box('.mechanical-model-info-body');
      return {sx:s.x,sy:s.y,sw:s.width,sh:s.height,
        rx:r.x,ry:r.y,rw:r.width,rh:r.height,
        rb:r.bottom,nb:n.bottom,bt:body.top,bb:body.bottom};
    }""")

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":1366,"height":800})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    ck('Patch 14' in page.locator('h1').inner_text(),'UI version missing')
    for css in ('#ecgCanvas','#mechanicalSVG','#mechanicalPhase',
                '#mechanicalModelInfo','#guidedV112Assumptions'):
        ck(page.locator(css).count()==1,'original DOM duplicate: '+css)
    page.locator('#mechanicalModeBtn').click()
    ck(page.locator('#mechanicalView').is_visible(),'mechanical view not visible')
    ck(not page.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
       'mechanical note unexpectedly expanded')
    ck(page.locator('.mechanical-readout>p').evaluate(
       'e=>parseFloat(getComputedStyle(e).fontSize)')>=14,'core explanation too small')
    ck(page.locator('.mechanical-stats').evaluate(
       'e=>parseFloat(getComputedStyle(e).fontSize)')>=13,'core valve/flow text too small')
    for width in (360,390,768,899,900,1024,1366,1440):
        page.set_viewport_size({"width":width,"height":800})
        ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
           f'horizontal page overflow at {width}')
        g=geometry(page)
        if width<900:
            ck(g['ry']>=g['sy']+g['sh']-8,
               f'stacked mobile layout failed: {width} {g}')
        else:
            ck(g['rx']>=g['sx']+g['sw']-12,
               f'parallel desktop layout failed: {width} {g}')
            ck(g['sw']>=280 and g['rw']>=280,
               f'mechanical column became too small: {width} {g}')
        summary=page.locator('#mechanicalModelInfo>summary')
        minimum=44 if width<=699 else 40
        ck(summary.evaluate('e=>e.getBoundingClientRect().height')>=minimum-1,
           f'info target too short: {width}')
        if width in (390,900,1024,1366,1440):
            page.screenshot(path=str(SHOTS/f'{width}-compact.png'),
                            full_page=True,animations='disabled')
        closed=geometry(page)
        summary.click()
        ck(page.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
           f'info disclosure failed to open: {width}')
        opened=geometry(page)
        ck(opened['rh']>=closed['rh']+55,
           f'expansion does not grow original card: {width} {opened}')
        ck(opened['bt']>=opened['nb']-3 and opened['bb']<=opened['rb']+2,
           f'floating note overlaps outside its original readout: {width} {opened}')
        ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
           f'expanded note causes horizontal overflow: {width}')
        if width in (390,1024,1366):
            page.screenshot(path=str(SHOTS/f'{width}-info-open.png'),
                            full_page=True,animations='disabled')
        summary.click()
        ck(not page.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
           f'info could not close: {width}')

    page.set_viewport_size({"width":1024,"height":800})
    narrowed=page.add_style_tag(content="""
      .dashboard-active .dashboard-stage[data-view='mechanical'] {
        width:610px!important;max-width:100%!important
      }""")
    g=geometry(page)
    ck(g['ry']>=g['sy']+g['sh']-8,
       f'available-width fallback to one column did not occur: {g}')
    narrowed.evaluate('e=>e.remove()')

    page.set_viewport_size({"width":1366,"height":800})
    state=snapshot(page)
    summary=page.locator('#mechanicalModelInfo>summary')
    summary.focus()
    page.keyboard.press('Enter')
    ck(page.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
       'keyboard Enter cannot open info')
    ck('0.88' in page.locator('.mechanical-model-info-body').inner_text(),
       'mechanical model RR limit lost')
    ck('환자' in page.locator('.mechanical-model-info-body').inner_text(),
       'clinical limitation lost')
    ck(snapshot(page)==state,'info changed physiological/visualization state')
    page.keyboard.press('Enter')
    ck(not page.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
       'keyboard Enter cannot close info')

    for hr in (30,72,180):
        page.locator('#heartRateSlider').evaluate(
          """(e,hr)=>{e.value=hr;e.dispatchEvent(new Event('input',{bubbles:true}))}""",hr)
        page.locator('#timeSlider').evaluate(
          """e=>{e.value=54;e.dispatchEvent(new Event('input',{bubbles:true}))}""")
        ck('Ready' not in page.locator('#mechanicalPhase').inner_text(),
           f'mechanical phase no longer updates at HR {hr}')
        ck('Flow:' in page.locator('#flowState').inner_text(),
           f'flow feedback missing HR {hr}')
    page.locator('#playBtn').click()
    page.wait_for_function('heartState.playing===true')
    page.locator('#pauseBtn').click()
    ck(not page.evaluate('heartState.playing'),'Pause regression')
    page.locator('#resetBtn').click()
    ck(page.locator('#mechanicalPhase').inner_text()=='Ready',
       'mechanical Reset regression')
    page.locator('#dashboardWiggersBtn').click()
    ck(page.locator('#wiggersChart').is_visible(),'Wiggers view missing')
    page.locator('#guidedV112Toggle').click()
    ck(page.locator('#guidedV112Assumptions').count()==1,
       'original five-stage note lost')
    note=page.locator('#guidedV112Assumptions>summary')
    state=snapshot(page)
    note.focus()
    page.keyboard.press('Enter')
    ck(page.locator('#guidedV112Assumptions').evaluate('e=>e.open'),
       'guided note keyboard activation missing')
    ck('상대' in page.locator('#guidedV112Limits').inner_text() or
       'RR' in page.locator('#guidedV112Limits').inner_text(),
       'guided caution content missing')
    ck(snapshot(page)==state,'guided information note changed simulation state')
    page.keyboard.press('Enter')
    ck(not page.locator('#guidedV112Assumptions').evaluate('e=>e.open'),
       'guided note keyboard close missing')
    ck(page.locator('#guidedV112Quiz').count()==1,'quiz UI missing')
    ck(page.evaluate("""()=>['atrial_systole','isovolumetric_contraction',
      'ejection','isovolumetric_relaxation','filling'].every(
       id=>['basic','advanced'].every(level=>
          CardiacGuidedQuestions.get(id,level)?.explanation?.length>12))"""),
       'ten questions or explanations lost')

    touch_context=browser.new_context(
      viewport={"width":390,"height":844},has_touch=True,is_mobile=True)
    touch=touch_context.new_page()
    touch.goto((ROOT/"index.html").as_uri())
    touch.locator('#mechanicalModeBtn').tap()
    touch.locator('#mechanicalModelInfo>summary').tap()
    ck(touch.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
       'touch cannot expand mechanical caution')
    touch.locator('#mechanicalModelInfo>summary').tap()
    ck(not touch.locator('#mechanicalModelInfo').evaluate('e=>e.open'),
       'touch cannot collapse mechanical caution')
    touch_context.close()
    ck(not errors,f'JavaScript runtime errors: {errors}')
    browser.close()

print(f'PASS {checks} Patch14 adaptive mechanical UI, notes and regressions')
