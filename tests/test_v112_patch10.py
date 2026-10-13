"""Patch 10 ECG past-only annotations and electrical gap semantics."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
n=0
def ck(x,msg):
 global n
 assert x,msg
 n+=1
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={"width":1366,"height":768})
 errors=[]
 page.on("pageerror",lambda e:errors.append(str(e)))
 page.goto((ROOT/"index.html").as_uri())
 page.evaluate("""()=>{window.__labels=[];const old=ctx.fillText.bind(ctx);
   ctx.fillText=(word,x,y)=>{if(['P','QRS','T'].includes(word))window.__labels.push({word,x});return old(word,x,y)}}""")
 page.evaluate("()=>{window.__labels=[];drawECGSweep()}")
 ck(page.evaluate("window.__labels.length")==0,"Ready falsely shows P/QRS/T")
 for hr in (30,80,180):
  page.locator("#heartRateSlider").evaluate("""(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}""",hr)
  t=page.evaluate("""()=>{const t=getActiveTiming();return {rr:t.rr,p:(t.pStart+t.pEnd)/2,qrs:(t.qrsStart+t.qrsEnd)/2,tw:(t.stEnd+t.tEnd)/2}}""")
  for moment in (t["p"]*.5,t["p"]+5,t["qrs"]+5,t["tw"]+5):
   page.locator("#timeSlider").evaluate("""(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}""",moment/t["rr"]*100)
   state=page.evaluate("""()=>{window.__labels=[];drawECGSweep();
    return {labels:window.__labels,cursor:heartState.sweepPosition,phase:getPhysiologicalCyclePhase()}}""")
   ck(all(0<=q["x"]<=state["cursor"] for q in state["labels"]),f"Future label at {hr}/{moment}: {state}")
   if moment<t["p"]:ck(len(state["labels"])==0,f"Predicted label at {hr}: {state}")
   if moment>t["p"]+1:ck(any(q["word"]=="P" for q in state["labels"]),f"Missing P at {hr}: {state}")
   if moment<t["qrs"]:ck(not any(q["word"]=="QRS" for q in state["labels"]),f"Future QRS at {hr}")
   if moment>t["qrs"]+1:ck(any(q["word"]=="QRS" for q in state["labels"]),f"Missing QRS at {hr}")
  page.locator("#timeSlider").evaluate("""e=>{e.value=99.9;e.dispatchEvent(new Event('input',{bubbles:true}))}""")
  s=page.evaluate("""()=>({ready:CardiacDashboard.isReady,phase:phaseTitle.textContent})""")
  ck(not s["ready"] and s["phase"]!="Ready",f"Late-cycle Ready confusion {hr}: {s}")
 page.locator("#resetBtn").click()
 ck(page.evaluate("CardiacDashboard.isReady"),"Reset Ready broken")
 page.evaluate("()=>{window.__labels=[];drawECGSweep()}")
 ck(page.evaluate("window.__labels.length")==0,"Reset shows ECG labels")
 ck(not errors,f"JS page errors: {errors}")
 b.close()
print(f"PASS {n} Patch10 ECG annotation/status checks")
