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
        filling:'심실 충만',
        atrial_systole:'심방 수축',
        isovolumetric_contraction:'등용적 수축',
        ejection:'심실 박출',
        isovolumetric_relaxation:'등용적 이완'
    };
    // Read-only educational interpretation of the existing Patch 2 profile.
    const STAGE_LESSONS=Object.freeze({
        filling:'심실 충만: 좌심실 압력이 좌심방 압력보다 낮아지면 승모판이 열리고 혈액이 들어옵니다. 이 모형의 RR 초반에는 상대 용적 0.88이 평탄하게 표시되고, RR 후반에는 용적이 증가합니다. 평탄한 구간은 충만이 멈춘다는 뜻이 아니라 표현상의 단순화입니다.',
        atrial_systole:'심방 수축: 심전도 P파가 먼저 나타난 뒤 심방이 수축하여 승모판이 열린 심실에 혈액을 더 채웁니다.',
        isovolumetric_contraction:'등용적 수축: QRS파가 나타난 뒤 승모판 닫힘(S1 표지), 대동맥판 열림 순으로 진행됩니다. 두 판막이 닫힌 동안 심실 압력은 증가하지만 상대 용적은 일정합니다.',
        ejection:'심실 박출: 대동맥판이 열리면 혈액이 심실 밖으로 나가고 상대 심실 용적이 감소합니다. T파로 나타나는 심실 재분극은 박출 후반과 시간상 겹칠 수 있습니다.',
        isovolumetric_relaxation:'등용적 이완: 대동맥판 닫힘(S2 표지)으로 박출이 끝납니다. 두 판막이 닫힌 채로 심실 압력은 떨어지고 상대 용적은 일정합니다.'
    });
    const EVENT_LESSONS=Object.freeze({
        'mitral-close':{
            title:'승모판 닫힘 · S1',
            detail:'심실 압력이 높아지면서 승모판이 닫힙니다. 실제 첫 심음(S1)은 주로 승모판·삼첨판 폐쇄와 연관되지만, 이 도표는 좌측의 대표 사건만 표시합니다.'
        },
        'aortic-open':{
            title:'대동맥판 열림',
            detail:'좌심실 압력이 대동맥판 열림 조건에 도달하면 박출이 시작되고 상대 심실 용적이 감소합니다. 사건 경계의 모형 압력은 같게 보일 수 있습니다.'
        },
        'aortic-close':{
            title:'대동맥판 닫힘 · S2',
            detail:'대동맥판이 닫히면 박출이 끝나고 등용적 이완이 시작됩니다. 실제 두 번째 심음(S2)은 대동맥판·폐동맥판 폐쇄와 관련되지만 도표에는 좌측 사건만 표시합니다.'
        },
        'mitral-open':{
            title:'승모판 열림',
            detail:'좌심실 압력이 좌심방 압력보다 낮아지면 승모판이 열려 심실 충만이 이어집니다.'
        }
    });
    const lessonStage=document.getElementById('wiggersLearningStage');
    const lessonEvent=document.getElementById('wiggersLearningEvent');
    function updateLessons(snapshot){
        if(!lessonStage || !lessonEvent)return;
        const stage=STAGE_LESSONS[snapshot.mechanical.stage]||'모형에 표시된 심장주기 단계입니다.';
        if(lessonStage.textContent!==stage)lessonStage.textContent=stage;
        // Use Patch 2's canonical event ties, not v1.9's floating-point states.
        const phase=snapshot.cycle.phaseMs;
        const recent=snapshot.valveEvents.filter(e=>e.timeMs<=phase).at(-1);
        let story='이 박동의 첫 판막 표지 전에는 승모판이 열려 심실 충만이 진행됩니다.';
        if(recent){
            const info=EVENT_LESSONS[recent.id];
            const atMarker=Math.abs(phase-recent.timeMs)<=1e-8;
            story=(atMarker?'현재 판막 사건: ':'직전 판막 사건: ')+
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
        timeLabel.textContent='생리학적 시간(A) '
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
        if(lessonStage)lessonStage.textContent='시간 막대를 움직이거나 재생을 눌러 심장주기를 관찰하세요.';
        if(lessonEvent)lessonEvent.textContent='판막·S1·S2 사건의 해설은 도표의 사건 표지와 연결됩니다.';
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
