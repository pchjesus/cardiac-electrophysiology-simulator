/*
 * Cardiac Electrophysiology Simulator v1.9 — educational mechanical model.
 * No independent clocks / rAF / timers. Every output is a pure function of
 * the active physiological beat, built on script.js's A clock.
 * Pressure units here are relative teaching indexes, never mmHg.
 */
(() => {
    'use strict';
    const BY_ID = id => document.getElementById(id);
    const clamp = (n,lo,hi)=>Math.max(lo,Math.min(hi,n));
    const labels = {
        filling: ['심실 충만','방실판막이 열린 상태에서 심방의 혈액이 이완된 심실로 흘러 들어옵니다.'],
        atrial_systole: ['심방 수축','심방이 수축하여 심실의 마지막 충만을 돕습니다.'],
        isovolumetric_contraction: ['등용적 수축','판막이 닫힌 상태에서 심실 압력은 증가하지만 심실 용적은 일정합니다.'],
        ejection: ['심실 박출','심실 압력이 동맥 쪽 압력을 넘으면 반월판막이 열리고 혈액이 박출됩니다.'],
        isovolumetric_relaxation: ['등용적 이완','판막이 닫힌 상태에서 심실이 이완하며 압력은 떨어지고 심실 용적은 일정합니다.']
    };

    function getMechanicalTiming(electrical = getActiveTiming()) {
        const rr=electrical.rr;
        // Delays follow electrical activation, not the clipped QT endpoint.
        // v1.8 high-HR QT truncation therefore cannot truncate ejection.
        const atrialStart=clamp(electrical.pStart+Math.min(20,0.028*rr),1,rr);
        const contractionStart=electrical.qrsStart+Math.min(18,0.04*rr);
        const ejectionStart=contractionStart+clamp(0.075*rr,20,55);
        const ejectionEnd=Math.min(rr-clamp(0.15*rr,40,150),ejectionStart+clamp(0.32*rr,65,380));
        const relaxationEnd=Math.min(rr-8,ejectionEnd+clamp(0.045*rr,14,45));
        return {rr, atrialStart,contractionStart,ejectionStart,ejectionEnd,relaxationEnd};
    }

    // Pure, deterministic domain model. No DOM or mutable app state here.
    function getMechanicalState(phase, electrical = getActiveTiming()) {
        const t=getMechanicalTiming(electrical);
        const p=((phase%t.rr)+t.rr)%t.rr;
        let stage,progress,volume;
        if(p<t.atrialStart){
            stage='filling';progress=clamp(p/t.atrialStart,0,1);volume=0.88;
        }else if(p<t.contractionStart){
            stage='atrial_systole';progress=(p-t.atrialStart)/(t.contractionStart-t.atrialStart);
            volume=0.88+0.12*progress;
        }else if(p<t.ejectionStart){
            stage='isovolumetric_contraction';progress=(p-t.contractionStart)/(t.ejectionStart-t.contractionStart);
            volume=1;
        }else if(p<t.ejectionEnd){
            stage='ejection';progress=(p-t.ejectionStart)/(t.ejectionEnd-t.ejectionStart);
            volume=1-0.52*progress;
        }else if(p<t.relaxationEnd){
            stage='isovolumetric_relaxation';progress=(p-t.ejectionEnd)/(t.relaxationEnd-t.ejectionEnd);
            volume=0.48;
        }else{
            stage='filling';progress=(p-t.relaxationEnd)/(t.rr-t.relaxationEnd);
            volume=0.48+0.40*progress;
        }
        // Qualitative relative pressures; only comparisons are used for valve rules.
        let atrial,ventricular,arterial;
        switch(stage){
            case 'atrial_systole': atrial=16;ventricular=10;arterial=85;break;
            case 'isovolumetric_contraction': atrial=12;ventricular=20+62*progress;arterial=85;break;
            case 'ejection': atrial=10;ventricular=105+7*Math.sin(Math.PI*progress);arterial=88+4*Math.sin(Math.PI*progress);break;
            case 'isovolumetric_relaxation': atrial=12;ventricular=78-64*progress;arterial=88;break;
            default: atrial=12;ventricular=8;arterial=85;
        }
        const avOpen=atrial>ventricular;
        const semilunarOpen=ventricular>arterial;
        // Pressure comparisons define the states. Invalid valve combinations
        // are treated as implementation errors by the regression suite.
        return {
            stage,progress,phase:p,rr:t.rr,boundaries:t,
            pressure:{atrial,ventricular,arterial},
            valves:{mitral:avOpen,tricuspid:avOpen,aortic:semilunarOpen,pulmonary:semilunarOpen},
            flow:semilunarOpen?'ejection':avOpen?'filling':'none',
            ventricularVolume:volume,
            atrialContracting:stage==='atrial_systole',
            ventricularContracting:stage==='isovolumetric_contraction'||stage==='ejection'
        };
    }

    const electricBtn=BY_ID('electricalModeBtn');
    const mechanicalBtn=BY_ID('mechanicalModeBtn');
    const electricalSvg=BY_ID('heartSVG');
    const mechanicalView=BY_ID('mechanicalView');
    const currentTitle=BY_ID('heartVisualTitle');
    const particleNodes=[...document.querySelectorAll('.flow-dot')];
    let mode='electrical';
    let lastState=null;

    function selectMode(next) {
        if(next!=='electrical'&&next!=='mechanical')return;
        mode=next;
        const showing=mode==='mechanical';
        if(showing) electricalSvg.setAttribute("hidden", "");
        else electricalSvg.removeAttribute("hidden");
        mechanicalView.hidden=!showing;
        electricBtn.classList.toggle('mode-active',!showing);
        mechanicalBtn.classList.toggle('mode-active',showing);
        electricBtn.setAttribute('aria-pressed',String(!showing));
        mechanicalBtn.setAttribute('aria-pressed',String(showing));
        currentTitle.textContent=showing?'심장 수축·판막·혈류':'심장 전기전도';
        sync();
        if(showing && heartState.physiologicalTime===0 && !heartState.playing && heartState.currentStep===-1){
            reset();
        }
    }

    function setValve(id,open) {
        BY_ID(id).classList.toggle('valve-open',open);
        BY_ID(id).classList.toggle('valve-closed',!open);
    }

    function renderState(state){
        const {stage,progress,valves,flow}=state;
        const [title,explanation]=labels[stage];
        BY_ID('mechanicalPhase').textContent=title;
        BY_ID('mechanicalExplanation').textContent=explanation;
        BY_ID('avValveState').textContent=`방실판막: ${valves.mitral?'열림':'닫힘'}`;
        BY_ID('outflowValveState').textContent=`반월판막: ${valves.aortic?'열림':'닫힘'}`;
        BY_ID('flowState').textContent=`혈류: ${flow==='ejection'?'심실 → 동맥':flow==='filling'?'심방 → 심실':'뚜렷한 판막 통과 혈류 없음'}`;
        const vol=state.ventricularVolume;
        BY_ID('volumeState').textContent=`심실 상대 용적: ${Math.round(vol*100)}% (학습용)`;
        for(const [id,opened] of Object.entries(valves))setValve(`${id}Valve`,opened);
        const ry=44+12*vol;
        for(const id of ['leftVentricleShape','rightVentricleShape'])BY_ID(id).setAttribute('ry',ry.toFixed(3));
        const raRy=state.atrialContracting?42:48;
        for(const id of ['leftAtrialShape','rightAtrialShape'])BY_ID(id).setAttribute('ry',String(raRy));
        // Particles are placed deterministically along SVG paths; no CSS
        // keyframes, new timers, or independently advancing animation loops.
        const activePaths = flow==='filling' ? ['flowRightAV','flowLeftAV'] : flow==='ejection' ? ['flowPulmonary','flowAortic'] : [];
        particleNodes.forEach((dot,index)=>{
            const pathId=dot.dataset.flow;
            const active=activePaths.includes(pathId);
            dot.style.opacity=active?'1':'0';
            if(!active)return;
            const path=BY_ID(pathId);
            const stagger=(index%2)*0.45;
            const fraction=(progress*0.85+stagger)%1;
            const point=path.getPointAtLength(path.getTotalLength()*fraction);
            dot.setAttribute('cx',point.x.toFixed(2));
            dot.setAttribute('cy',point.y.toFixed(2));
        });
    }
    function sync(){
        // Electrical mode continues to update normally behind the other view.
        const current=getMechanicalState(getPhysiologicalCyclePhase());
        lastState=current;
        // Render when displayed, or on first-ever activation of this view.
        if(mode==='mechanical')renderState(current);
        return current;
    }
    function reset(){
        lastState=getMechanicalState(0);
        if(mode==='mechanical'){
            renderState(lastState);
            BY_ID('mechanicalPhase').textContent='Ready';
            BY_ID('mechanicalExplanation').textContent='재생하거나 시간 막대를 움직여 심장 수축·판막·혈류 변화를 관찰하세요.';
            BY_ID('avValveState').textContent='방실판막: —';
            BY_ID('outflowValveState').textContent='반월판막: —';
            BY_ID('flowState').textContent='혈류: —';
            BY_ID('volumeState').textContent='심실 상대 용적: —';
            particleNodes.forEach(dot=>dot.style.opacity='0');
        }
    }
    electricBtn.addEventListener('click',()=>selectMode('electrical'));
    mechanicalBtn.addEventListener('click',()=>selectMode('mechanical'));
    window.CardiacMechanical={getMechanicalTiming,getMechanicalState,sync,reset,selectMode,get mode(){return mode;},get currentState(){return lastState;}};
    selectMode('electrical');
})();
