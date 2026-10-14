"""v1.13 UX Patch 2: Korean-first explanations, Wiggers help and glossary regression."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"preview-v113-korean-help"
OUT.mkdir(exist_ok=True)
n=0
def ck(ok,message):
 global n
 assert ok,message
 n+=1

with sync_playwright() as p:
 browser=p.chromium.launch()
 for width in (360,390,768,1366):
  page=browser.new_page(viewport={"width":width,"height":900})
  errors=[]
  page.on("pageerror",lambda x:errors.append(str(x)))
  page.goto((ROOT/"index.html").as_uri())
  ck(page.evaluate("!!window.CardiacConceptHelpV113"),"concept help did not load")
  ck(page.evaluate("CardiacConceptHelpV113.keys.length===8"),"lost key concepts")
  ck(page.locator("#playBtn").inner_text().find("재생")>=0,"native playback label still English")
  ck("심박수" in page.locator("#heartRateDisplay").inner_text(),"live HR still English")
  ck("심전도" in page.locator(".ecg-panel h2").inner_text(),"ECG heading not Korean")
  ck("심전도" in page.locator("#ecgExplanationTitle").inner_text(),"ECG initial helper not Korean")
  initial=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,playing:heartState.playing,hr:heartRate})")
  page.locator("[data-concept-help='ecg']").first.click()
  dlg=page.locator("#v113ConceptDialog")
  ck(dlg.is_visible(),"ECG help modal not visible")
  ck("심전도" in dlg.locator("h2").inner_text(),"ECG help missing title")
  ck(dlg.get_by_text("왜 중요한가요?").is_visible(),"why important section missing")
  ck(dlg.get_by_text("학습할 때 주의할 점").is_visible(),"model limitations missing")
  ck("심근 수축" in dlg.inner_text(),"ECG clinical meaning missing")
  ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,playing:heartState.playing,hr:heartRate})")==initial,
     "opening concept popup altered simulator state")
  page.keyboard.press("Escape")
  ck(not dlg.is_visible(),"Escape did not close concept help")
  ck(page.evaluate("document.activeElement?.getAttribute('data-concept-help')==='ecg'"),"modal focus did not return to opener")
  page.locator("#dashboardWiggersBtn").click()
  ck("위거스" in page.locator("#dashboardWiggersBtn").inner_text(),"Wiggers tab still English")
  page.locator("#wiggersHelpButton").click()
  w=page.locator("#wiggersHelp")
  ck(w.is_visible(),"original Wiggers help not available")
  ck("왜 중요" in w.inner_text(),"Wiggers popup lacks learning rationale")
  ck("판막" in w.inner_text() and "압력" in w.inner_text(),"Wiggers popup does not teach interpretation")
  ck("실제" in w.inner_text(),"Wiggers limits not explained")
  ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,playing:heartState.playing,hr:heartRate})")==initial,
     "Wiggers help altered simulator state")
  page.keyboard.press("Escape")
  ck(not w.is_visible(),"Wiggers Escape close failed")
  page.locator("#v113TabLearning").click()
  ck("위거스 도표" in page.locator(".v113-unit-button").nth(4).inner_text(),"fifth unit lacks Korean name")
  ck(page.locator(".v113-glossary-shortcuts").count()==1,"in-learning glossary missing")
  glossary=page.locator(".v113-glossary-shortcuts")
  glossary.locator("summary").click()
  ck(glossary.locator("[data-concept-help]").count()>=6,"insufficient student glossary entries")
  glossary.locator("[data-concept-help='wiggers']").click()
  ck(dlg.is_visible(),"Wiggers glossary did not open")
  ck(dlg.get_by_text("무슨 뜻인가요?").is_visible(),"Wiggers definition missing")
  ck(dlg.get_by_text("어떻게 살펴보나요?").is_visible(),"Wiggers reading guide missing")
  ck("같은 시간축" in dlg.inner_text(),"Wiggers shared time axis missing")
  ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,playing:heartState.playing,hr:heartRate})")==initial,
     "Wiggers glossary changed A/B")
  page.get_by_role("button",name="용어 설명 팝업 닫기").click()
  for idx in range(6):
   if width<=900 and not page.locator(".v113-unit-picker").evaluate("e=>e.open"):
    page.locator(".v113-unit-picker>summary").click()
   page.locator(".v113-unit-button").nth(idx).click()
   ck(page.locator(".v113-concept-unit").count()==1,f"missing unit concept button {idx}")
   ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,playing:heartState.playing,hr:heartRate})")==initial,
      f"chapter {idx} changed A/B")
   page.locator(".v113-concept-unit").click()
   ck(dlg.is_visible(),f"unit {idx} help did not open")
   ck("왜 중요한가요?" in dlg.inner_text(),f"unit {idx} lacks rationale")
   page.keyboard.press("Escape")
  ck(page.evaluate("document.querySelectorAll('#guidedV112Panel').length===1"),"original Guide duplicated")
  ck("심장" in page.locator("#heartVisualTitle").inner_text(),"heart area does not use Korean label")
  ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),f"horizontal overflow at {width}")
  page.screenshot(path=str(OUT/f"korean-learning-{width}.png"),full_page=True)
  page.locator(".v113-concept-unit").click()
  page.screenshot(path=str(OUT/f"korean-popup-{width}.png"),full_page=True)
  page.keyboard.press("Escape")
  ck(not errors,f"browser JS exceptions: {errors}")
  page.close()
 browser.close()
print(f"v1.13 UX Patch 2 Korean/help: {n} assertions passed")
