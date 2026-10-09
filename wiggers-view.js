/*
 * v1.10 Patch 3 — OPTIONAL Wiggers teaching diagram.
 * Read-only adapter of the existing A clock and ECG / Patch 2 profile.
 * There is NO rAF, interval, timeout, second clock, or simulation state owner.
 */
(function(root) {
    'use strict';
    const details=document.getElementById('wiggersDetails');
    const chart=document.getElementById('wiggersChart');
    const markerGroup=document.getElementById('wiggersMarkers');
    const phaseLabel=document.getElementById('wiggersCurrentStage');
    const timeLabel=document.getElementById('wiggersCurrentTime');
    const valveLabel=document.getElementById('wiggersCurrentValves');
    const cursor=document.getElementById('wiggersCursor');

    if(!details || !chart || !markerGroup || !root.CardiacWiggersProfile ||
       !root.CardiacWiggers) return;

    const NS='http://www.w3.org/2000/svg';
    const LEFT=64, RIGHT=955, SPAN=RIGHT-LEFT, SAMPLES=480;
    const STAGE_NAMES={
        filling:'Ventricular filling',
        atrial_systole:'Atrial systole',
        isovolumetric_contraction:'Isovolumetric contraction',
        ejection:'Ventricular ejection',
        isovolumetric_relaxation:'Isovolumetric relaxation'
    };
    const plot=(id,values)=>{
        const node=document.getElementById(id);
        node.setAttribute('d',values.map(([x,y],i)=>
            (i===0?'M':'L')+x.toFixed(2)+' '+y.toFixed(2)).join(' '));
    };
    const xAt=(phase,rr)=>LEFT+SPAN*phase/rr;
    const pressureY=p=>200-1.23*p;          // 0..130 relative index; NOT mmHg.
    const ecgY=v=>267-v*0.37;               // existing ECG waveform in one RR.
    const volumeY=v=>408-(v-0.45)*132;     // normalized relative volume.
    let plottedRR=null;
    let plottedTimingKey='';
    let buildCount=0;

    function getTimingKey(t) {
        return [t.rr,t.pStart,t.pEnd,t.qrsStart,t.qrsEnd,t.stEnd,t.tEnd].join('|');
    }
    function drawModel(t) {
        const profile=root.CardiacWiggersProfile;
        const curves={ecg:[],la:[],lv:[],aorta:[],volume:[]};
        for(let i=0;i<=SAMPLES;i++) {
            // Endpoint = RR (which is equivalent to t=0 for a closed loop).
            const time=t.rr*i/SAMPLES;
            const snapshot=profile.getSnapshot(time,t);
            const x=xAt(time,t.rr);
            curves.ecg.push([x,ecgY(ecgValue(time,t))]);
            curves.la.push([x,pressureY(snapshot.pressure.leftAtrial)]);
            curves.lv.push([x,pressureY(snapshot.pressure.leftVentricular)]);
            curves.aorta.push([x,pressureY(snapshot.pressure.aortic)]);
            curves.volume.push([x,volumeY(snapshot.ventricularVolume.relativeValue)]);
        }
        plot('wiggersPathECG',curves.ecg);
        plot('wiggersPathLA',curves.la);
        plot('wiggersPathLV',curves.lv);
        plot('wiggersPathAorta',curves.aorta);
        plot('wiggersPathVolume',curves.volume);

        markerGroup.replaceChildren();
        const events=profile.getSnapshot(0,t).valveEvents;
        for(const event of events) {
            const x=xAt(event.timeMs,t.rr);
            const group=document.createElementNS(NS,'g');
            group.setAttribute('data-event',event.id);
            const line=document.createElementNS(NS,'line');
            line.setAttribute('x1',x.toFixed(2));
            line.setAttribute('x2',x.toFixed(2));
            line.setAttribute('y1','35');
            line.setAttribute('y2','421');
            line.setAttribute('class','wiggers-event-line');
            const dot=document.createElementNS(NS,'circle');
            dot.setAttribute('cx',x.toFixed(2));
            dot.setAttribute('cy','429');
            dot.setAttribute('r','4');
            dot.setAttribute('class','wiggers-event-dot');
            const title=document.createElementNS(NS,'title');
            const label={'mitral-close':'Mitral closes / S1',
                         'aortic-open':'Aortic opens',
                         'aortic-close':'Aortic closes / S2',
                         'mitral-open':'Mitral opens'}[event.id] || event.id;
            title.textContent=label+' — '+Math.round(event.timeMs)+' ms';
            group.append(line,dot,title);
            markerGroup.appendChild(group);
        }
        plottedRR=t.rr;
        plottedTimingKey=getTimingKey(t);
        ++buildCount;
    }

    function sync() {
        if(!details.open) return; // zero graph work while collapsed
        const timing=getActiveTiming();
        if(plottedTimingKey!==getTimingKey(timing)) drawModel(timing);
        const current=root.CardiacWiggersProfile.getSnapshot(
            getPhysiologicalCyclePhase(),timing
        );
        const x=xAt(current.cycle.phaseMs,timing.rr);
        cursor.setAttribute('x1',x.toFixed(2));
        cursor.setAttribute('x2',x.toFixed(2));
        phaseLabel.textContent=STAGE_NAMES[current.mechanical.stage]||current.mechanical.stage;
        timeLabel.textContent='Physiological phase '+
            Math.round(current.cycle.phaseMs)+' / '+Math.round(timing.rr)+' ms · '+
            Math.round(current.cycle.heartRateBpm)+' bpm';
        valveLabel.textContent='Mitral: '+(current.valves.mitral?'Open':'Closed')+
            ' · Aortic: '+(current.valves.aortic?'Open':'Closed');
    }

    function reset() {
        if(!details.open) return;
        sync();
        // Match v1.9 reset semantics: controls return to Ready, not active phase.
        phaseLabel.textContent='Ready';
    }

    details.addEventListener('toggle',()=>{
        if(details.open) sync();
    });
    // Runtime owns neither the open state nor an animation timer.
    // Sync is called only by script.js's existing conduction update path.
    root.CardiacWiggersView=Object.freeze({
        sync,reset,
        get open(){return details.open;},
        get buildCount(){return buildCount;},
        get currentPhaseMs(){
            return details.open ? root.CardiacWiggersProfile.getSnapshot(
                getPhysiologicalCyclePhase(),getActiveTiming()).cycle.phaseMs : null;
        }
    });
})(window);
