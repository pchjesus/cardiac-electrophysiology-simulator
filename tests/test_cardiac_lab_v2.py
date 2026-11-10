"""Cardiac Lab UX Reset v2 — live DOM, model isolation, responsive screenshot QA."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "preview-cardiac-lab-v2"
OUT.mkdir(exist_ok=True)

def check(condition, message):
    assert condition, message

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri())
    check(page.locator(".ux-reset-intro").is_visible(), "learner-first introduction missing")
    check(page.locator("link[href='cardiac-lab-v2.css']").count() == 1, "new visual layer missing")
    check(page.locator("#ecgCanvas").count() == 1, "duplicate ECG canvas")
    check(page.locator("#heartSVG").count() == 1, "duplicate native electrical SVG")
    check(page.locator("#timeSlider").count() == 1, "duplicate canonical Timeline")
    check(page.locator("#v113TabClinical").is_disabled(), "clinical was exposed")
    check(page.locator("#v113TabLearning").is_enabled(), "learning unavailable")
    check(page.evaluate("getComputedStyle(document.querySelector('.dashboard-v111')).display") == "grid", "desktop grid missing")
    boxes = page.evaluate("""() => {
      const r = selector => {
        const x = document.querySelector(selector).getBoundingClientRect();
        return {left:x.left,right:x.right,top:x.top,bottom:x.bottom};
      };
      return {ecg:r('.dashboard-primary>.ecg-panel'),
              visual:r('.dashboard-primary>.dashboard-workspace'),
              inspector:r('.dashboard-v111>.dashboard-inspector')};
    }""")
    check(boxes["ecg"]["right"] <= boxes["visual"]["left"]+3,
          "ECG and anatomical display overlap: " + str(boxes))
    check(boxes["visual"]["right"] <= boxes["inspector"]["left"]+3,
          "anatomical controls blocked by inspector: " + str(boxes))
    check(abs(boxes["ecg"]["top"]-boxes["visual"]["top"]) < 12,
          "ECG and anatomical display not observable in one row: " + str(boxes))

    page.locator("#playBtn").click()
    page.wait_for_timeout(180)
    check(page.evaluate("heartState.playing"), "Play not connected")
    page.locator("#pauseBtn").click()
    check(not page.evaluate("heartState.playing"), "Pause not connected")
    before = page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    page.locator("#mechanicalModeBtn").scroll_into_view_if_needed()
    print("MODE DIAG",page.evaluate("""() => {
      const rect=sel=>{const a=document.querySelector(sel).getBoundingClientRect();return {x:a.x,y:a.y,width:a.width,height:a.height,right:a.right}};
      const m=document.getElementById('mechanicalModeBtn').getBoundingClientRect();
      const el=document.elementFromPoint(m.x+m.width/2,m.y+m.height/2);
      return {button:rect('#mechanicalModeBtn'),tabs:rect('.heart-mode-switch'),
        visual:rect('.dashboard-visual'),workspace:rect('.dashboard-workspace'),
        inspector:rect('.dashboard-inspector'),over:el?.tagName+' '+(el?.className||''),
        scrollX:scrollX,scrollY:scrollY,primaryGrid:getComputedStyle(document.querySelector('.dashboard-primary')).gridTemplateColumns};
    }"""),flush=True)
    page.screenshot(path=str(OUT / "mode-diagnostic.png"),full_page=True,animations="disabled")
    page.locator("#mechanicalModeBtn").click()
    page.locator("#dashboardWiggersBtn").click()
    page.locator("#electricalModeBtn").click()
    after = page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    check(before == after, "visual switches mutated A/B clocks")
    page.locator("#timeSlider").evaluate("(e)=>{e.value='42';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    check(not page.evaluate("heartState.playing"), "seek did not pause")
    page.locator("#resetBtn").click()
    check(page.evaluate("heartState.physiologicalTime===0 && heartState.visualizationTime===0"), "reset broken")
    page.locator("#v113TabLearning").click()
    check(page.locator(".v113-unit-title").is_visible(), "course hidden")
    page.locator("#v113TabSimulator").click()

    for width in (320, 360, 390, 768, 1024, 1366, 1440):
        page.set_viewport_size({"width": width, "height": 900})
        page.wait_for_timeout(80)
        check(page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth+1"),
              f"horizontal document overflow at {width}")
        check(page.locator("#ecgCanvas").is_visible(), f"ECG missing at {width}")
        check(page.locator("#playBtn").is_visible(), f"Play missing at {width}")
        if width in (390, 768, 1440):
            page.screenshot(path=str(OUT / f"simulator-{width}.png"), full_page=True, animations="disabled")
        page.locator("#v113TabLearning").click()
        check(page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth+1"),
              f"Learning horizontal document overflow at {width}")
        if width in (390, 1440):
            page.screenshot(path=str(OUT / f"learning-{width}.png"), full_page=True, animations="disabled")
        page.locator("#v113TabSimulator").click()

    qa = browser.new_page(viewport={"width": 1440, "height": 900})
    qa.goto((ROOT / "index.html").as_uri() + "?v113Preview=1")
    qa.locator("#v113TabClinical").click()
    check(qa.locator("#v113ClinicalScreen").is_visible(), "QA Clinical preview unavailable")
    qa.screenshot(path=str(OUT / "clinical-qa-1440.png"), full_page=True, animations="disabled")
    check(not errors, "JS errors: " + str(errors))
    browser.close()
print("Cardiac Lab v2 UX/engine/responsive preview checks PASS")
