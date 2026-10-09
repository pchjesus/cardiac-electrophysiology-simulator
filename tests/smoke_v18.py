"""Lightweight reproducible browser regression for v1.8 FINAL.

Install: pip install playwright && python -m playwright install chromium
Run from repository root: python tests/smoke_v18.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import math

root=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    page=browser.new_page(viewport={"width":1366,"height":900})
    errors=[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.set_content((root/"index.html").read_text(encoding="utf-8"))
    page.add_style_tag(content=(root/"style.css").read_text(encoding="utf-8"))
    page.add_script_tag(content=(root/"script.js").read_text(encoding="utf-8"))
    assertions=0
    for hr in range(30,181):
        output=page.evaluate("""(hr) => {
            heartRate=hr; updateHeartRateUI();
            const t=getActiveTiming();
            const measurements=getECGMeasurements();
            const eventList=ecgEvents.map(e=>({id:e.id,start:e.start,end:e.end}));
            reset(); heartState.physiologicalTime=0.55*t.rr;
            heartState.ecgTime=heartState.physiologicalTime;
            updateConduction(true); updateTimeline();
            return {t,measurements,eventList,percent:Number(slider.value),
              current:heartState.currentECGEvent,phase:getPhysiologicalCyclePhase()};
        }""",hr)
        t=output["t"]
        assert math.isclose(t["rr"],60000/hr,abs_tol=1e-7)
        assert 0<=t["pStart"]<t["pEnd"]<t["qrsStart"]<t["qrsEnd"]<t["stEnd"]<t["tEnd"]<t["rr"]
        assert math.isclose(t["qrsDuration"],80)
        assert 125<=t["prInterval"]<=200
        assert math.isclose(t["qtInterval"],t["tEnd"]-t["qrsStart"])
        assert math.isclose(output["measurements"]["qtc"],t["qtInterval"]/math.sqrt(t["rr"]/1000))
        assert math.isclose(output["phase"],t["rr"]*0.55,abs_tol=1e-5)
        assert abs(output["percent"]-55)<0.2
        assert all(math.isclose(output["eventList"][i]["end"],output["eventList"][i+1]["start"],abs_tol=1e-7) for i in range(6))
        assertions+=9
    page.evaluate("reset()")
    assert page.evaluate("heartState.physiologicalTime===0 && heartState.visualizationTime===0 && !heartState.playing")
    page.locator("#playBtn").click()
    page.wait_for_timeout(200)
    page.locator("#pauseBtn").click()
    assert page.evaluate("heartState.physiologicalTime>0 && !heartState.playing")
    assert not errors,errors
    print("PASS:",assertions+2,"assertions; JS errors:",errors)
    browser.close()
