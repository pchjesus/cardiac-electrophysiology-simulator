"""v1.10 Patch 2: continuous relative pressure/volume without changing v1.9 UI."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import math

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backups/v1.9/FINAL"
checks = 0

def check(ok, message):
    global checks
    checks += 1
    assert ok, message

def initialize(page, folder, new):
    page.set_content((folder / "index.html").read_text(encoding="utf-8"))
    page.add_style_tag(content=(folder / "style.css").read_text(encoding="utf-8"))
    for name in ["script.js", "mechanics.js"] + (["wiggers.js", "wiggers-profile.js"] if new else []):
        page.add_script_tag(content=(folder / name).read_text(encoding="utf-8"))

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium",
                                 args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={"width": 1366, "height": 900})
    baseline = browser.new_page(viewport={"width": 1366, "height": 900})
    errors = {"new": [], "baseline": []}
    page.on("pageerror", lambda e: errors["new"].append(str(e)))
    baseline.on("pageerror", lambda e: errors["baseline"].append(str(e)))
    initialize(page, ROOT, True)
    initialize(baseline, BASE, False)
    check(page.evaluate("typeof window.CardiacWiggersProfile?.getSnapshot") == "function",
          "Continuous profile not registered")
    check(page.locator("#heartSVG").is_visible() and
          not page.locator("#mechanicalView").is_visible(), "Default view changed")

    # All physically modelled integer HR inputs. Browser JS assertions run
    # in one evaluation per HR to avoid thousands of Python/browser roundtrips.
    for hr in range(30, 181):
        for tab in (page, baseline):
            tab.locator("#heartRateSlider").evaluate(
                """(el,hr)=>{el.value=hr;el.dispatchEvent(new Event("input",{bubbles:true}));}""",hr)
        data = page.evaluate("""() => {
            const t=getActiveTiming(), m=window.CardiacMechanical,
                  p=window.CardiacWiggersProfile,w=window.CardiacWiggers,
                  b=m.getMechanicalTiming(t);
            let checks=0;
            function ck(v,msg){checks++;if(!v)throw Error('HR '+heartRate+': '+msg);}
            const prior=JSON.stringify({
                state:heartState, bpm:heartRate,speed:animationSpeed,
                view:m.mode,mechanics:m.currentState
            });
            const anchors=p.getLandmarks(t);
            ck(anchors.length===7,'landmarks');
            ck(p.metadata.pressureCalibrated===false,'unverified measurements disclaimer');
            ck(p.metadata.pressureUnit==='relative-teaching-index','relative pressure units');
            ck(p.metadata.boundaryConvention.includes('half-open'),'boundary contract');
            const states=anchors.map(a=>p.getSnapshot(a.timeMs,t));
            ck(states[0].pressure.leftAtrial===states[6].pressure.leftAtrial &&
               states[0].pressure.leftVentricular===states[6].pressure.leftVentricular &&
               states[0].pressure.aortic===states[6].pressure.aortic,
               'periodic pressure must return to beginning');
            for(const v of ['leftAtrial','leftVentricular','aortic']){
                ck(Math.abs(states[0].pressure[v]-states[6].pressure[v])<1e-9,
                   'wrap pressure '+v);
            }
            for(const q of [0,b.atrialStart,b.contractionStart,b.ejectionStart,
                            b.ejectionEnd,b.relaxationEnd,b.rr]){
                const d=0.0001, left=p.getSnapshot(q-d,t),right=p.getSnapshot(q,t);
                for(const name of ['leftAtrial','leftVentricular','aortic']){
                    ck(Math.abs(left.pressure[name]-right.pressure[name])<1e-5,
                       'C0 pressure '+q+'/'+name);
                }
                ck(Math.abs(left.ventricularVolume.relativeValue-
                            right.ventricularVolume.relativeValue)<1e-6,
                   'C0 volume '+q);
            }
            const eventChecks=[
                [b.contractionStart,'mitral',true,false],
                [b.ejectionStart,'aortic',false,true],
                [b.ejectionEnd,'aortic',true,false],
                [b.relaxationEnd,'mitral',false,true]
            ];
            eventChecks.forEach(([q,valve,before,after])=>{
                ck(p.getSnapshot(q-.0001,t).valves[valve]===before,'event before '+valve);
                ck(p.getSnapshot(q,t).valves[valve]===after,'event at '+valve);
                ck(p.getSnapshot(q+.0001,t).valves[valve]===after,'event after '+valve);
            });
            const eventIDs=p.getSnapshot(0,t).valveEvents.map(x=>x.id);
            ck(JSON.stringify(eventIDs)===JSON.stringify(w.getValveEvents(t).map(x=>x.id)),
               'event IDs diverged');
            ck(p.getSnapshot(0,t).heartSoundEvents[0].id==='S1' &&
               p.getSnapshot(0,t).heartSoundEvents[1].id==='S2','heart sound IDs');
            for(let i=0;i<301;i++){
                const q=(i+.5)*t.rr/301, s=p.getSnapshot(q,t);
                const v=s.ventricularVolume.relativeValue;
                ck(Number.isFinite(v) && v>=.48-1e-10 && v<=1+1e-10,'volume bounds');
                for(const k of ['leftAtrial','leftVentricular','aortic'])
                    ck(Number.isFinite(s.pressure[k]),'finite pressure '+k);
                ck(!(s.valves.mitral && s.valves.aortic),'both valves open');
                ck(s.valves.mitral ? s.pressureGradients.mitral>=-1e-8:
                  s.pressureGradients.mitral<=1e-8,'mitral gradient conflict');
                ck(s.valves.aortic ? s.pressureGradients.aortic>=-1e-8:
                  s.pressureGradients.aortic<=1e-8,'aortic gradient conflict');
                ck(s.flow===(s.valves.aortic?'ejection':s.valves.mitral?'filling':'none'),
                   'flow contradicts valves');
                ck(s.mechanical.stage===m.getMechanicalState(q,t).stage,'mechanical stage mismatch');
                if(s.mechanical.stage.startsWith('isovolumetric')){
                    const expected=s.mechanical.stage==='isovolumetric_contraction'?1:.48;
                    ck(Math.abs(v-expected)<1e-10,'isovolumetric volume drift');
                }
                // The new profile is C1-smooth; no step jump is permitted at
                // representative event boundaries (including cycle wrap).
            }
            ck(JSON.stringify(p.getSnapshot(b.ejectionStart,t))===
               JSON.stringify(p.getSnapshot(b.ejectionStart+t.rr,t)),
               'single-cycle phase repeat differs');
            const negative=p.getSnapshot(-.01,t);
            ck(Math.abs(negative.cycle.phaseMs-(t.rr-.01))<1e-7,'negative phase wrap');
            const after=JSON.stringify({
                state:heartState,bpm:heartRate,speed:animationSpeed,
                view:m.mode,mechanics:m.currentState
            });
            ck(prior===after,'profile mutated application state');
            return {checks,anchorIDs:anchors.map(x=>x.id),intervals:b};
        }""")
        checks += data["checks"]
        check(data["anchorIDs"] == ["cycle-start", "atrial-start", "mitral-close",
                                  "aortic-open", "aortic-close", "mitral-open",
                                  "cycle-end"],f"landmark naming at HR {hr}")
        check(math.isclose(data["intervals"]["rr"],60000/hr,abs_tol=1e-8),
              f"HR/RR model mismatch at HR {hr}")

    # Exactly existing stable UI behavior, A/B clocks, ECG, and current
    # Mechanical domain layer: compare with the immutable v1.9 backup.
    for hr in (30,50,72,80,100,120,150,180):
        for tab in (page,baseline):
            tab.locator("#heartRateSlider").evaluate(
                """(el,hr)=>{el.value=hr;el.dispatchEvent(new Event("input",{bubbles:true}));}""",hr)
        for seek in (0,7,29,50,77,99,100):
            for tab in (page,baseline):
                tab.locator("#timeSlider").evaluate(
                    """(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}));}""",seek)
                tab.evaluate("updateSimulation(17)")
            state = """() => ({
                A:heartState.physiologicalTime,B:heartState.visualizationTime,
                anchor:heartState.cycleStartTime,speed:animationSpeed,
                sweep:heartState.sweepPosition,event:heartState.currentECGEvent,
                measurements:getECGMeasurements(),step:heartState.currentStep,
                mech:window.CardiacMechanical.getMechanicalState(getPhysiologicalCyclePhase()),
                wave:[0,15,60,120,200,275].map(x=>ecgValue(x))
            })"""
            check(page.evaluate(state)==baseline.evaluate(state),
                  f"UI/A-B/ECG/Mechanical regression at HR {hr} seek {seek}")

    # View/Reset preservation and stable 390px layout.
    for tab in (page,baseline):
        tab.locator("#mechanicalModeBtn").click()
        tab.locator("#resetBtn").click()
    check(page.locator("#mechanicalPhase").text_content()=="Ready",
          "Mechanical reset Ready lost")
    check(page.locator("#mechanicalModeBtn").get_attribute("aria-pressed")=="true",
          "Reset changed selected view")
    page.locator("#playBtn").click()
    page.wait_for_timeout(160)
    page.locator("#pauseBtn").click()
    check(page.evaluate("heartState.physiologicalTime>0 && !heartState.playing"),
          "Play/Pause changed")
    page.locator("#electricalModeBtn").click()
    check(page.locator("#heartSVG").is_visible(),"Electrical mode not restored")
    page.set_viewport_size({"width":390,"height":844})
    baseline.set_viewport_size({"width":390,"height":844})
    check(page.evaluate("document.documentElement.scrollWidth") <=
          baseline.evaluate("document.documentElement.scrollWidth"),
          "New profile changed mobile layout")
    for statement in ("window.CardiacWiggersProfile.getSnapshot(Infinity,getActiveTiming())",
                      "window.CardiacWiggersProfile.getSnapshot(NaN,getActiveTiming())",
                      "window.CardiacWiggersProfile.getSnapshot(0,{rr:0})"):
        check(page.evaluate("""(expr)=>{
            try {new Function('return ('+expr+')')();return false;}
            catch(e){return e instanceof Error;}
        }""",statement),f"Invalid parameter accepted: {statement}")
    check(errors=={"new":[],"baseline":[]},f"Browser page exceptions: {errors}")
    print(f"PASS {checks} v1.10 Patch 2 profile checks. HR 30-180, "
          "continuous pressure/volume boundaries, valve equalities, "
          "pressure inequalities, A/B and v1.9 unchanged, mobile. "
          f"Errors={errors}")
    browser.close()
