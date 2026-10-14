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
        filling:'심실 충만(Ventricular filling)',
        atrial_systole:'심방 수축(Atrial systole)',
        isovolumetric_contraction:'등용적 수축(Isovolumetric contraction)',
        ejection:'심실 박출(Ventricular ejection)',
        isovolumetric_relaxation:'등용적 이완(Isovolumetric relaxation)'
    };
    // Read-only educational interpretation of the existing Patch 2 profile.
    const STAGE_LESSONS=Object.freeze({
        filling:'심실 충만(Ventricular filling): 좌심실 압력이 좌심방보다 낮아지면 승모판이 열리고 심실에 혈액이 들어옵니다. 이 모델에서는 RR 후반 충만 구간의 상대 좌심실 용적이 증가하지만, RR 초반에는 상대 용적 0.88로 평탄하게 표현됩니다. 이는 모형의 단순화이며 실제 생리학적 충만이 멈춘다는 뜻은 아닙니다. 이어지는 심방 수축은 충만을 보조합니다.',
        atrial_systole:'심방 수축(Atrial systole): 심전도 P파는 심방의 실제 수축보다 먼저 나타납니다. 승모판이 열린 상태에서 심방 수축은 심실 충만의 마지막 부분을 보조합니다.',
        isovolumetric_contraction:'등용적 수축(Isovolumetric contraction): QRS 탈분극 후 승모판 닫힘(S1 표시)이 대동맥판 열림보다 앞섭니다. 두 판막이 모두 닫혀 좌심실 압력은 상승하지만 상대 용적은 변하지 않습니다.',
        ejection:'심실 박출(Ventricular ejection): 대동맥판이 열리면 혈액이 심실에서 동맥으로 나가며 상대 심실 용적이 감소합니다. 심실 재분극을 나타내는 T파는 박출 후반과 일부 겹칠 수 있습니다.',
        isovolumetric_relaxation:'등용적 이완(Isovolumetric relaxation): 대동맥판 닫힘(S2 표시)으로 박출이 끝납니다. 두 판막이 닫힌 채 심실 압력은 감소하고 상대 심실 용적은 일정하게 유지됩니다.'
    });
    const EVENT_LESSONS=Object.freeze({
        'mitral-close':{
            title:'승모판 닫힘(Mitral closes / S1)',
            detail:'심실 압력이 높아지면서 승모판이 닫힙니다. 첫 번째 심음(S1)은 주로 승모판과 삼첨판 닫힘에 관련되며, 이 도표에서는 왼쪽 심장의 대표적인 사건만 표시합니다.'
        },
        'aortic-open':{
            title:'대동맥판 열림(Aortic opens)',
            detail:'심실 압력이 대동맥판 열림 조건에 도달하면 박출이 시작되고 상대 좌심실 용적이 감소합니다. 사건 표시 시점에는 모형의 두 압력이 같을 수 있으며, 판막 사건 규칙에 따라 열림 상태를 정합니다.'
        },
        'aortic-close':{
            title:'대동맥판 닫힘(Aortic closes / S2)',
            detail:'대동맥판이 닫히면 박출이 끝나고 등용적 이완이 시작됩니다. 두 번째 심음(S2)은 대동맥판과 폐동맥판 닫힘에 관련되지만, 이 단순화된 도표에서는 왼쪽 심장의 사건만 표시합니다.'
        },
        'mitral-open':{
            title:'승모판 열림(Mitral opens)',
            detail:'좌심실이 이완하여 그 압력이 좌심방보다 낮아지면 승모판이 열리고 심실 충만이 다시 시작됩니다.'
        }
    });
    const lessonStage=document.getElementById('wiggersLearningStage');
    const lessonEvent=document.getElementById('wiggersLearningEvent');
    function updateLessons(snapshot){
        if(!lessonStage || !lessonEvent)return;
        const stage=STAGE_LESSONS[snapshot.mechanical.stage]||'교육용 심장주기 단계입니다.';
        if(lessonStage.textContent!==stage)lessonStage.textContent=stage;
        // Use Patch 2's canonical event ties, not v1.9's floating-point states.
        const phase=snapshot.cycle.phaseMs;
        const recent=snapshot.valveEvents.filter(e=>e.timeMs<=phase).at(-1);
        let story='이 RR 구간의 첫 판막 사건 표시 전에는 승모판이 열려 있어 심실 충만이 가능합니다.';
        if(recent){
            const info=EVENT_LESSONS[recent.id];
            const atMarker=Math.abs(phase-recent.timeMs)<=1e-8;
            story=(atMarker?'현재 판막 사건: ':'최근 판막 사건: ')+
                info.title+' ('+Math.round(recent.timeMs)+' ms). '+info.detail;
        }
        if(lessonEvent.textContent!==story)lessonEvent.textContent=story;
    }

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
            const label=EVENT_LESSONS[event.id]?.title || event.id;
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
        timeLabel.textContent='생리학적 주기 시점(A) '+
            Math.round(current.cycle.phaseMs)+' / '+Math.round(timing.rr)+' ms · '+
            Math.round(current.cycle.heartRateBpm)+' bpm';
        valveLabel.textContent='승모판: '+(current.valves.mitral?'열림':'닫힘')+
            ' · 대동맥판: '+(current.valves.aortic?'열림':'닫힘');
        updateLessons(current);
    }

    function reset() {
        if(!details.open) return;
        sync();
        // Match v1.9 reset semantics: controls return to Ready, not active phase.
        phaseLabel.textContent='Ready';
        if(lessonStage)lessonStage.textContent='재생하거나 심장주기 시간축을 움직여 심장 단계의 변화를 살펴보세요.';
        if(lessonEvent)lessonEvent.textContent='판막과 심음(S1/S2) 설명은 그래프의 사건 표시와 같은 심장주기 시간축을 따릅니다.';
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
