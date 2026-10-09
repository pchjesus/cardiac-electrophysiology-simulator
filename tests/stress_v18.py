from pathlib import Path
from playwright.sync_api import sync_playwright
p=Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((p/'index.html').read_text());page.add_style_tag(content=(p/'style.css').read_text());page.add_script_tag(content=(p/'script.js').read_text())
 result=page.evaluate('''() => {
    let checks=0, samples=0, changes=0;
    const assert=(val,reason)=>{checks++;if(!val)throw new Error(reason)};
    for(let hr=30;hr<=180;hr++){
        heartRate=hr;updateHeartRateUI(); const t=getActiveTiming();
        assert(Math.abs(t.rr-60000/hr)<1e-8, 'RR '+hr);
        assert(t.prInterval>=125 && t.prInterval<=200,'PR '+hr);
        assert(t.qrsDuration===80,'QRS '+hr);
        assert(t.qrsStart>=t.pEnd && t.tEnd<t.rr,'cycle order '+hr);
        assert(Math.abs(t.qtInterval-(t.tEnd-t.qrsStart))<1e-8,'QT '+hr);
        const ev=ecgEvents;
        assert(ev[0].start===0 && Math.abs(ev.at(-1).end-t.rr)<1e-8,'event coverage '+hr);
        for(let i=0;i<ev.length;i++){
            assert(ev[i].end>=ev[i].start,'nonempty event '+hr+':'+i);
            if(i)assert(Math.abs(ev[i-1].end-ev[i].start)<1e-7,'no gap '+hr+':'+i);
        }
        assert(Math.abs(conductionSteps[4].end-t.qrsEnd)<1e-8,'Purkinje ends QRS '+hr);
        const expectedEvents=['Baseline','P','PR','QRS','ST','T','Baseline'];
        for(let i=0;i<ev.length;i++){
            const mid=(ev[i].start+ev[i].end)/2;
            assert(getCurrentECGEvent(mid).id===expectedEvents[i],'event mid '+hr+':'+i);
            samples++;
        }
        // Exact and immediately adjacent event boundaries: no undefined step.
        for(const e of ev){
            for(const dt of [-1e-5,0,1e-5]){
                let phase=e.start+dt;if(phase<0)continue;
                let id=getCurrentECGEvent(phase).id;
                assert(['Baseline','P','PR','QRS','ST','T'].includes(id),'boundary event '+hr);
                let value=ecgValue(phase,t);
                assert(Number.isFinite(value),'nonfinite ECG '+hr);
                samples++;
            }
        }
        for(const x of [0.02,0.1,0.2,0.35,0.5,0.65,0.85,0.97]){
            heartState.physiologicalTime=x*t.rr;heartState.cycleStartTime=0;
            heartState.visualizationTime=x*baseCycleLength;
            heartState.ecgTime=heartState.physiologicalTime;
            updateConduction(true);updateTimeline();
            assert(Math.abs(getPhysiologicalCyclePhase()/t.rr-x)<1e-7,'timeline phys '+hr);
            assert(Number.isFinite(Number(slider.value)),'slider '+hr);
            assert(heartState.currentECGEvent===getCurrentECGEvent(x*t.rr).id,'event UI '+hr);
            changes++;
        }
        reset();
    }
    return {checks,samples,seekStates:changes};
}''')
 print('P10 stress:',result,'page errors:',errors)
 assert errors==[]
 b.close()
