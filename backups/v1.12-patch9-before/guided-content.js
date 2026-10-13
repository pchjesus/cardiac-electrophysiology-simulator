/*
 * v1.12 Patch 1 — read-only curriculum identifiers and representative
 * model intervals. No DOM, timers, clinical predictions or simulation state.
 * Event boundaries come from the unmodified CardiacMechanical timing model;
 * representative midpoints are checked against the Wiggers profile.
 */
(function(root){
  'use strict';
  const data=[
    {id:'atrial_systole',label:'심방 수축',
     range:['atrialStart','contractionStart'],tag:'P파 이후 심방 수축 · 모델 상대 용적 증가'},
    {id:'isovolumetric_contraction',label:'등용적 수축',
     range:['contractionStart','ejectionStart'],tag:'QRS 이후 압력 상승 · 두 판막 닫힘 · 상대 용적 일정'},
    {id:'ejection',label:'심실 박출',
     range:['ejectionStart','ejectionEnd'],tag:'대동맥판 개방 · 상대 용적 감소'},
    {id:'isovolumetric_relaxation',label:'등용적 이완',
     range:['ejectionEnd','relaxationEnd'],tag:'대동맥판 폐쇄(S2 대표 사건) · 상대 용적 일정'},
    {id:'filling',label:'심실 충만 · 모델 RR 후반',
     range:['relaxationEnd','rr'],tag:'승모판 개방 후 상대 용적 증가. 모델 RR 초반 충만은 상대 용적이 평탄함'}
  ].map(d=>Object.freeze({...d,range:Object.freeze(d.range)}));
  const stages=Object.freeze(data);
  function getObservation(stageId,timing,mechanical,profile){
    const stage=stages.find(x=>x.id===stageId);
    if(!stage||!timing||!mechanical||!profile)return null;
    const bounds=mechanical.getMechanicalTiming(timing);
    const start=bounds[stage.range[0]],end=bounds[stage.range[1]];
    if(!Number.isFinite(start)||!Number.isFinite(end)||end<=start)
      throw new Error('Invalid v1.12 guided interval: '+stageId);
    const middle=(start+end)/2;
    const snapshot=profile.getSnapshot(middle,timing);
    if(snapshot.mechanical.stage!==stageId)
      throw new Error('Guide/profile stage mismatch: '+stageId+' vs '+snapshot.mechanical.stage);
    return Object.freeze({
      id:stageId, startMs:start,endMs:end,midpointMs:middle,
      rrMs:bounds.rr,
      modeledStage:snapshot.mechanical.stage,
      relativeLVVolume:snapshot.ventricularVolume.relativeValue
    });
  }
  root.CardiacGuidedContent=Object.freeze({stages,getObservation});
})(window);
