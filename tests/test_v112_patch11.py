"""Patch11 student first study from Ready, grouped optional controls and preserved native A/B."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
n=0
def ck(v,m):
 global n
 assert v,m
 n+=1
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={"width":1366,"height":768})
 errors=[]
 page.on("pageerror",lambda e:errors.append(str(e)))
 page.goto((ROOT/"index.html").as_uri())
 page.evaluate("""()=>{window.__seekCount=0;document.getElementById('timeSlider')
   .addEventListener('input',()=>window.__seekCount++)}""")
 ck(page.evaluate("CardiacDashboard.isReady"),"Expected Ready")
 ck(page.locator("#guidedV112Toggle").inner_text()=="5단계 학습 시작","Entry CTA unclear")
 ck(not page.locator("#guidedV112Panel").is_visible(),"Guidance opt-in lost")
 page.locator("#guidedV112Toggle").click()
 ck(page.evaluate("window.__seekCount")==1,"First entry should seek exactly once")
 ck(not page.evaluate("heartState.playing"),"First study should pause")
 ck(page.evaluate("CardiacGuidedLearning.selectedStageId")=="atrial_systole","Initial stage wrong")
 ck(page.evaluate("CardiacMechanical.currentState.stage")=="atrial_systole","First heartbeat observation wrong")
 ck(not page.locator("#guidedV112Tools").evaluate("(e)=>e.open"),"Optional controls expanded by default")
 ck(page.locator("#guidedV112Gist").is_visible(),"Gist missing")
 ck(page.locator("#guidedV112Previous").is_disabled(),"First boundary wrong")
 # Every original tool is still present, but no longer competes with the basic reading path.
 for sel in ("#guidedV112Level","#guidedV112Seek","#guidedV112ViewWiggers","#guidedV112Promote","#guidedV112Quiz"):
  ck(page.locator(sel).count()==1,f"Original student tool lost: {sel}")
 page.locator("#guidedV112Next").click()
 ck(page.evaluate("window.__seekCount")==2,"Next triggered extra seek")
 ck(page.evaluate("CardiacMechanical.currentState.stage")=="isovolumetric_contraction","Next stage wrong")
 page.locator("#guidedV112Tools>summary").click()
 ck(page.locator("#guidedV112Level").is_visible(),"Advanced controls inaccessible")
 before=page.evaluate("window.__seekCount")
 page.locator("#guidedV112Level").select_option("intermediate")
 ck(page.evaluate("window.__seekCount")==before,"Changing learning level altered Timeline")
 page.locator("#guidedV112Toggle").click()
 ck(page.locator("#guidedV112Toggle").inner_text()=="5단계 학습 이어보기","Reentry label misleading")
 page.locator("#playBtn").click()
 page.wait_for_timeout(100)
 before=page.evaluate("window.__seekCount")
 page.locator("#guidedV112Toggle").click()
 ck(page.evaluate("window.__seekCount")==before,"Reopening study auto-seeked")
 ck(page.evaluate("heartState.playing"),"Reopening study stopped playback")
 ck(page.locator("#guidedV112Gist").is_visible(),"Fixed learning missing")
 page.locator("#pauseBtn").click()
 ck(not errors,f"JS page errors {errors}")
 b.close()
print(f"PASS {n} Patch11 first-study/controls checks")
