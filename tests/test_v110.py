"""v1.10 Patch 1: passive Wiggers data-contract and v1.9 behavioral equivalence."""
from pathlib import Path
import math
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
baseline = root / "backups/v1.9/FINAL"
checks = 0


def check(condition, message):
    global checks
    checks += 1
    assert condition, message


def load(page, folder, include_wiggers):
    page.set_content((folder / "index.html").read_text(encoding="utf-8"))
    page.add_style_tag(content=(folder / "style.css").read_text(encoding="utf-8"))
    page.add_script_tag(content=(folder / "script.js").read_text(encoding="utf-8"))
    page.add_script_tag(content=(folder / "mechanics.js").read_text(encoding="utf-8"))
    if include_wiggers:
        page.add_script_tag(content=(folder / "wiggers.js").read_text(encoding="utf-8"))


with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium",
                                 args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={"width": 1366, "height": 900})
    old = browser.new_page(viewport={"width": 1366, "height": 900})
    errors = {"current": [], "baseline": []}
    page.on("pageerror", lambda e: errors["current"].append(str(e)))
    old.on("pageerror", lambda e: errors["baseline"].append(str(e)))
    load(page, root, True)
    load(old, baseline, False)

    check(page.evaluate("typeof window.CardiacWiggers.getSnapshot") == "function",
          "Wiggers module not registered after mechanics.js")
    check(old.evaluate("typeof window.CardiacWiggers") == "undefined",
          "Backup does not represent the v1.9 baseline")
    check(page.locator("#heartSVG").is_visible(), "Electrical mode changed on load")
    check(not page.locator("#mechanicalView").is_visible(), "Mechanical mode changed on load")
    check(page.locator("#phaseTitle").text_content() == old.locator("#phaseTitle").text_content(),
          "Initial Ready feedback changed")

    for hr in range(30, 181):
        for tab in (page, old):
            tab.locator("#heartRateSlider").evaluate(
                """(node, value) => {
                    node.value = value;
                    node.dispatchEvent(new Event('input', {bubbles: true}));
                }""", hr)

        result = page.evaluate("""() => {
            const e = getActiveTiming(), mech = window.CardiacMechanical;
            const wig = window.CardiacWiggers, b = mech.getMechanicalTiming(e);
            const before = JSON.stringify({
                heartState, heartRate, animationSpeed,
                mechanical: mech.currentState, mode: mech.mode
            });
            const events = wig.getValveEvents(e), sounds = wig.getHeartSoundEvents(e);
            const sampleTimes = [
                0, b.atrialStart, b.contractionStart, b.ejectionStart,
                b.ejectionEnd, b.relaxationEnd, e.rr - 0.0001
            ];
            const samples = sampleTimes.map(p => {
                const snapshot = wig.getSnapshot(p, e);
                const original = mech.getMechanicalState(p, e);
                return {
                    snapshot,
                    source: {
                        pressure: original.pressure,
                        volume: original.ventricularVolume,
                        valves: original.valves,
                        flow: original.flow,
                        stage: original.stage
                    }
                };
            });
            const again = JSON.stringify(wig.getSnapshot(b.ejectionStart, e));
            const same = JSON.stringify(wig.getSnapshot(b.ejectionStart + e.rr, e));
            const after = JSON.stringify({
                heartState, heartRate, animationSpeed,
                mechanical: mech.currentState, mode: mech.mode
            });
            return {events, sounds, samples, audit: wig.inspectPressureBoundaries(e),
                    unchanged: before === after, repeatable: again === same,
                    rr:e.rr, boundaries:b};
        }""")
        b = result["boundaries"]
        check(result["unchanged"], f"Wiggers mutated simulation state at HR {hr}")
        check(result["repeatable"], f"Phase-wrapped samples not deterministic at HR {hr}")
        check(math.isclose(result["rr"], 60000 / hr, abs_tol=1e-7),
              f"RR disagreement at HR {hr}")
        check(0 < b["atrialStart"] < b["contractionStart"] < b["ejectionStart"] <
              b["ejectionEnd"] < b["relaxationEnd"] < b["rr"],
              f"Mechanical timing out of order at HR {hr}: {b}")
        events = result["events"]
        sounds = result["sounds"]
        check([x["id"] for x in events] ==
              ["mitral-close", "aortic-open", "aortic-close", "mitral-open"],
              f"Valve event IDs at HR {hr}")
        check([x["timeMs"] for x in events] ==
              [b["contractionStart"], b["ejectionStart"],
               b["ejectionEnd"], b["relaxationEnd"]],
              f"Valve event boundaries differ at HR {hr}")
        check([(x["id"], x["timeMs"], x["linkedValveEvent"]) for x in sounds] ==
              [("S1", b["contractionStart"], "mitral-close"),
               ("S2", b["ejectionEnd"], "aortic-close")],
              f"S1/S2 marker coupling at HR {hr}")
        check(len(result["audit"]) == 6 and any(x["discontinuous"] for x in result["audit"]),
              f"Missing boundary pressure discontinuity disclosure at HR {hr}")
        for item in result["samples"]:
            s = item["snapshot"]
            legacy = item["source"]
            check(s["metadata"]["calibratedForPatients"] is False and
                  s["pressure"]["representation"] == "discontinuous-relative-index",
                  f"Clinical unit disclaimer missing at HR {hr}")
            check(s["mechanical"]["stage"] == legacy["stage"] and
                  s["flow"] == legacy["flow"], f"Mechanical disagreement HR {hr}")
            check(s["pressure"]["leftAtrial"] == legacy["pressure"]["atrial"] and
                  s["pressure"]["leftVentricular"] == legacy["pressure"]["ventricular"] and
                  s["pressure"]["aortic"] == legacy["pressure"]["arterial"],
                  f"Pressure changed at HR {hr}")
            check(s["ventricularVolume"]["relativeValue"] == legacy["volume"],
                  f"Volume changed at HR {hr}")
            check(s["valves"]["mitral"] == legacy["valves"]["mitral"] and
                  s["valves"]["aortic"] == legacy["valves"]["aortic"],
                  f"Valve mismatch at HR {hr}")
        # Event boundaries are modeled as step transitions, not fake continuous
        # pressure crossings. Inspect before/after each valve switch.
        event_switches = page.evaluate("""(times) => {
            const e=getActiveTiming(), w=window.CardiacWiggers;
            return times.map(t => ({
                before:w.getSnapshot(t-0.0001,e).valves,
                after:w.getSnapshot(t,e).valves
            }));
        }""", [x["timeMs"] for x in events])
        check(event_switches[0]["before"]["mitral"] and
              not event_switches[0]["after"]["mitral"], f"Mitral close HR {hr}")
        check(not event_switches[1]["before"]["aortic"] and
              event_switches[1]["after"]["aortic"], f"Aortic open HR {hr}")
        check(event_switches[2]["before"]["aortic"] and
              not event_switches[2]["after"]["aortic"], f"Aortic close HR {hr}")
        check(not event_switches[3]["before"]["mitral"] and
              event_switches[3]["after"]["mitral"], f"Mitral open HR {hr}")

    # Compare actual v1.10 runtime with archived v1.9 at matched A/B and UI states.
    for hr in (30, 50, 72, 80, 100, 120, 150, 180):
        for tab in (page, old):
            tab.locator("#heartRateSlider").evaluate(
                "(el, val) => {el.value=val; el.dispatchEvent(new Event('input',{bubbles:true}));}", hr)
        for percentage in (0, 4, 20, 37, 65, 90, 100):
            for tab in (page, old):
                tab.locator("#timeSlider").evaluate(
                    "(el, val) => {el.value=val; el.dispatchEvent(new Event('input',{bubbles:true}));}",
                    percentage)
                tab.evaluate("updateSimulation(24)")
            state_js = """() => ({
                A: heartState.physiologicalTime,
                B: heartState.visualizationTime,
                cycleStart: heartState.cycleStartTime,
                speed: animationSpeed,
                sweep: heartState.sweepPosition,
                event: heartState.currentECGEvent,
                step: heartState.currentStep,
                measures: getECGMeasurements(),
                mechanical: window.CardiacMechanical.getMechanicalState(getPhysiologicalCyclePhase()),
                waveform: [0, 20, 75, 120, 200, 275].map(x => ecgValue(x))
            })"""
            check(page.evaluate(state_js) == old.evaluate(state_js),
                  f"v1.9 A/B, ECG or Mechanical regression at HR {hr}, seek {percentage}")

    for tab in (page, old):
        tab.locator("#mechanicalModeBtn").click()
        tab.locator("#resetBtn").click()
    check(page.locator("#mechanicalModeBtn").get_attribute("aria-pressed") == "true",
          "Reset changed Mechanical mode")
    check(page.locator("#mechanicalPhase").text_content() == "Ready",
          "Mechanical Ready not preserved")
    check(page.locator("#mechanicalPhase").text_content() ==
          old.locator("#mechanicalPhase").text_content(), "Reset feedback differs")
    page.locator("#playBtn").click()
    page.wait_for_timeout(150)
    page.locator("#pauseBtn").click()
    check(page.evaluate("heartState.physiologicalTime > 0 && !heartState.playing"),
          "Play/Pause no longer advance and stop A")
    page.locator("#electricalModeBtn").click()
    check(page.locator("#heartSVG").is_visible(), "Electrical view not restored")

    page.set_viewport_size({"width": 390, "height": 844})
    old.set_viewport_size({"width": 390, "height": 844})
    check(page.evaluate("document.documentElement.scrollWidth") ==
          old.evaluate("document.documentElement.scrollWidth"),
          "Patch 1 changed narrow-width overflow")
    check(errors["current"] == [] and errors["baseline"] == [],
          f"Page JS errors: {errors}")

    for expression in ("window.CardiacWiggers.getSnapshot(Infinity, getActiveTiming())",
                       "window.CardiacWiggers.getSnapshot(0, {rr:0})"):
        check(page.evaluate(f"""() => {{ try {{ {expression}; return false; }}
                               catch(e) {{ return e instanceof Error; }} }}"""),
              f"Invalid timing accepted: {expression}")

    print(f"PASS {checks} v1.10 Patch 1 checks: HR 30-180, ECG/Mechanical baseline "
          f"equivalence, pressure/valve events, S1/S2, seek, UI modes, play/pause/reset, "
          f"responsive width. JS errors={errors}")
    browser.close()
