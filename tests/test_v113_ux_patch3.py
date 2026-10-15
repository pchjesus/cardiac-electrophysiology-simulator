"""v1.13 UX Patch 3: Korean-first labels, accessibility and preserved simulation state."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
checks = 0

def ck(value, message):
    global checks
    assert value, message
    checks += 1

def clocks(page):
    return page.evaluate("""({
      a:heartState.physiologicalTime,
      b:heartState.visualizationTime,
      hr:heartRate,
      playing:heartState.playing,
      guided:CardiacGuidedLearning.hasStarted,
      course:CardiacCourseV113.completedUnitIds
    })""")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1366, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri())

    ck("v1.13 UX Patch 3" in page.title(), "document title not updated")
    ck("v1.13 UX Patch 3" in page.locator("h1").inner_text(), "visible version not updated")
    ck(page.locator("#v113TabClinical").is_disabled(), "unreviewed Clinical released")
    ck(page.locator("#v113TabLearning").is_enabled(), "public Learning unavailable")
    for selector in ("#phaseTitle", "#phaseECG", "#ecgEventIndicator",
                     "#dashboardElectrical", "#dashboardMechanical", "#dashboardEvent"):
        ck(page.locator(selector).inner_text() == "준비", "ready translation " + selector)
    ck(page.locator("#mechanicalPhase").inner_text() == "준비", "mechanical initial Ready")
    ck(page.locator("#wiggersCurrentStage").inner_text() == "준비", "Wiggers initial Ready")

    ck("심장" in page.locator(".header-tools").get_attribute("aria-label") or
       "시뮬레이터" in page.locator(".header-tools").get_attribute("aria-label"),
       "header ARIA translation")
    for selector in ("#mechanicalSVG", "#wiggersChart", ".event-flow",
                     ".learning-scenario-panel", ".learning-preset-row"):
        ck(any("\uac00" <= c <= "\ud7a3" for c in page.locator(selector).get_attribute("aria-label")),
           "non-Korean ARIA name " + selector)
    ck(page.get_by_role("button", name="전기 전도", exact=True).count() == 1,
       "conduction button changed")
    ck(page.get_by_role("button", name="심장 수축·판막", exact=True).count() == 1,
       "mechanical button changed")

    before = clocks(page)
    for kind in ("ecg", "electrical", "mechanical", "wiggers",
                 "timeline", "measurements", "nursing"):
        trigger = page.locator('[data-term-help="' + kind + '"]:visible').last
        ck(trigger.count() >= 1, "missing visible explanation trigger " + kind)
        trigger.click()
        ck(page.locator("#v113TermDialog").is_visible(), "dialog did not open " + kind)
        ck(page.locator("#v113TermBody h3").count() == 4, "four concept sections " + kind)
        page.keyboard.press("Escape")
        ck(page.locator("#v113TermDialog").is_hidden(), "Escape does not close " + kind)
        ck(trigger.evaluate("e=>document.activeElement===e"), "focus not restored " + kind)
        ck(clocks(page) == before, "dialog changed A/B or study state " + kind)

    # Actual ECG component explanation was originally English even after UX Patch 2.
    for component, expected in (("P", "P파"), ("PR", "PR 간격"),
                                 ("QRS", "QRS파"), ("ST", "ST 분절"), ("T", "T파")):
        page.locator('[data-ecg-component="' + component + '"]').click()
        ck(page.locator("#ecgExplanationTitle").inner_text() == expected,
           "ECG component title translation " + component)
        ck("심" in page.locator("#ecgExplanationText").inner_text() or
           "전" in page.locator("#ecgExplanationText").inner_text(),
           "ECG component explanation translation " + component)
        ck(clocks(page) == before, "ECG explanation mutated simulator state " + component)

    page.get_by_role("button", name="사용 설명서").click()
    ck("위거스 도표" in page.locator("#userGuidePanel").inner_text(),
       "guide terminology lost")
    ck(page.locator("#userGuideHeading").inner_text() == "? 사용 설명서",
       "duplicated user guide title")
    ck(page.locator("#userGuidePanel [data-close-info]").get_attribute("aria-label") ==
       "사용 설명서 닫기", "guide close ARIA name")
    page.locator("#userGuidePanel [data-close-info]").click()
    ck(clocks(page) == before, "help changed model state")

    # Only a deliberate Timeline seek may alter A/B; display-only labels must not.
    page.locator("#timeSlider").evaluate("e=>{e.value='42';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    ck(not page.evaluate("heartState.playing"), "timeline did not pause")
    ck(page.locator("#phaseTitle").inner_text() != "준비", "time seek never activated")
    page.locator("#resetBtn").click()
    ck(page.locator("#phaseTitle").inner_text() == "준비", "reset display not translated")
    ck(page.locator("#ecgExplanationTitle").inner_text() == "설명할 심전도 파형을 선택하세요",
       "reset ECG prompt reverted to English")

    for width in (320, 360, 390, 768, 900, 1024, 1366):
        page.set_viewport_size({"width": width, "height": 850})
        ck(page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"),
           "document overflows at " + str(width))
        page.locator("#v113TabLearning").click()
        ck(page.locator(".v113-unit-title").is_visible(), "Learning hidden at " + str(width))
        ck(page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"),
           "Learning overflows at " + str(width))
        page.locator("#v113TabSimulator").click()
    ck(not errors, "JavaScript errors: " + str(errors))
    browser.close()

print("v1.13 UX Patch 3 Korean terminology/accessibility/regression:", checks, "checks PASS")
