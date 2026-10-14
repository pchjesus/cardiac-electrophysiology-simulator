/*
 * v1.13 Patch 4 — illustrative, UNREVIEWED fictional clinical case fixture.
 * No real patient, no clinical approval, no binding to the sinus heartState.
 * Static authored facts; answers cannot alter the patient's observations.
 */
(function(root){
'use strict';
const phaseIds=Object.freeze(['assessment','judgement','nursing-action','reassessment']);
const validUnits=new Set(['unit-cardiac-cycle','unit-conduction','unit-ecg-timing','unit-mechanics','unit-wiggers','unit-nursing']);
const refA='aha-2025-brady',refM='medline-labs';
const caseOne={
 schemaVersion:1,id:'symptomatic-slow-pulse',revision:1,language:'ko',
 status:'draft-human-review-pending',fictional:true,
 title:'증상이 동반된 느린 맥박 · 환자 상태와 관류 사정',
 summary:'환자가 어지럼과 무력감을 호소하고 느린 맥박·낮은 혈압이 확인되었습니다. 심박수만으로 판단하지 않고 환자 상태를 함께 평가하세요.',
 objectives:['증상·활력징후·의식·관류 징후 함께 확인','시급한 보고 및 재평가 우선순위 구분','가상 검사 결과의 시각과 불확실성 확인'],
 baseline:{
  at:'2026-09-01T10:00:00+09:00',
  context:'가상 성인 환자가 오전 중 어지럼과 전신 무력감을 새로 호소함. 의식은 명료하나 일어날 때 어지러움이 지속됨.',
  measurements:[
   {id:'hr-initial',label:'심박수',value:42,unit:'/min',observedAt:'2026-09-01T10:00:00+09:00'},
   {id:'bp-initial',label:'혈압',value:'86/54',unit:'mmHg',observedAt:'2026-09-01T10:00:00+09:00'},
   {id:'rr-initial',label:'호흡수',value:20,unit:'/min',observedAt:'2026-09-01T10:00:00+09:00'},
   {id:'spo2-initial',label:'산소포화도',value:97,unit:'%',observedAt:'2026-09-01T10:00:00+09:00'}
  ]},
 ecg:{kind:'expert-review-pending-text',recordedAt:'2026-09-01T10:05:00+09:00',
  text:'별도로 작성한 교육용 관찰: 약 42회/분의 느린 심박동. 리듬의 세부 분류 및 원인은 아직 독립 판독을 받지 않았습니다.',
  limitation:'실시간 시뮬레이터 ECG와 무관한 가상 사례의 별도 설명입니다. 실제 12유도 ECG 판독이나 부정맥 확진을 대신하지 않습니다.'},
 labs:[
  {id:'potassium',name:'혈청 칼륨(K⁺)',status:'known',value:4.1,unit:'mmol/L',
   range:'3.5–5.0 mmol/L (가상 검사실 예시)',collectedAt:'2026-09-01T10:07:00+09:00',
   availableAt:'2026-09-01T10:12:00+09:00',availableFromPhase:3,
   note:'이 단일 결과로 원인을 확정하거나 다른 관류 문제를 배제할 수 없습니다.',
   referenceIds:[refM]},
  {id:'glucose',name:'혈당',status:'pending',value:null,unit:'mg/dL',
   range:'검사실·측정 조건에 따라 해석',collectedAt:'2026-09-01T10:07:00+09:00',
   availableAt:null,availableFromPhase:0,
   note:'결과 대기 중. 결과 미확인을 정상으로 해석하지 않습니다.',
   referenceIds:[refM]}
 ],
 reassessment:{at:'2026-09-01T10:15:00+09:00',
  context:'시간이 지난 뒤에도 어지럼이 지속됩니다. 아래 값은 선택한 답안과 무관한 사전 작성 가상 경과입니다.',
  measurements:[
   {id:'hr-followup',label:'심박수',value:46,unit:'/min',observedAt:'2026-09-01T10:15:00+09:00'},
   {id:'bp-followup',label:'혈압',value:'90/58',unit:'mmHg',observedAt:'2026-09-01T10:15:00+09:00'}
  ]},
 references:[
  {id:refA,title:'American Heart Association (2025) — Adult bradycardia with a pulse algorithm',
   url:'https://www.heart.org/-/media/CPR-Files/CPR-Guidelines-Files/2025-Algorithms/Algorithm-ACLS-Bradycardia-250514.pdf'},
  {id:refM,title:'MedlinePlus — How to understand your lab results',
   url:'https://medlineplus.gov/lab-tests/how-to-understand-your-lab-results/'}
 ],
 questions:[
  {id:'priority-assessment',phase:'assessment',prompt:'느린 심박수 외에 지금 우선 함께 사정해야 할 정보는?',
   choices:[
    {id:'a',text:'의식·호흡·혈압·말초관류와 증상의 변화를 확인한다.',feedback:'적절합니다. 환자의 관류 문제와 증상을 심박수와 함께 판단합니다.'},
    {id:'b',text:'심박수 42회/분 하나로 환자가 안정적이라고 단정한다.',feedback:'심박수 숫자만으로 안정성을 판단할 수 없습니다. 저혈압과 어지럼이 함께 있습니다.'},
    {id:'c',text:'검사실 결과가 모두 나올 때까지 신체 상태 확인을 미룬다.',feedback:'검사 결과 대기는 현 시점의 증상·혈압·관류 사정을 늦출 근거가 아닙니다.'}
   ],correctChoiceId:'a',rationale:'서맥성 상태는 단순 HR뿐 아니라 저혈압·의식 변화·쇼크·허혈 증상·심부전 등 관류 문제와 연관해 판단해야 합니다.',referenceIds:[refA],relatedUnitIds:['unit-nursing','unit-ecg-timing']},
  {id:'risk-judgement',phase:'judgement',prompt:'제공된 증상과 초기 활력징후를 함께 고려하면 어떤 판단이 가장 적절한가?',
   choices:[
    {id:'a',text:'어지럼이 있어도 맥박이 느릴 뿐이므로 일상 교육만 하고 귀가를 안내한다.',feedback:'어지럼과 낮은 혈압이 있어 신속한 환자 상태 평가 및 보고 필요성을 배제할 수 없습니다.'},
    {id:'b',text:'증상·혈압을 재확인하고 관류 문제 가능성을 팀에 즉시 보고한다.',feedback:'적절합니다. 상황의 시급성을 인지하고 팀 기반 평가·보고를 우선합니다.'},
    {id:'c',text:'칼륨 결과가 아직 없으니 현재 상태에는 문제가 없다고 판단한다.',feedback:'검사 미확인은 정상의 증거가 아니며 현재 활력징후와 증상에 우선 대응해야 합니다.'}
   ],correctChoiceId:'b',rationale:'저혈압과 새로 시작된 증상이 동반되어 있다면 신속한 사정·모니터링·의료진 보고가 필요합니다. 병태생리적 원인을 단정하지 않습니다.',referenceIds:[refA,refM],relatedUnitIds:['unit-nursing']},
  {id:'nursing-response',phase:'nursing-action',prompt:'간호학생의 안전한 우선 대응에 가장 가까운 선택은?',
   choices:[
    {id:'a',text:'직접 약물 처방과 침습적 처치를 결정하고 시행한다.',feedback:'독립적인 처방·시술 결정은 간호학생의 학습상 권한을 넘어섭니다. 정식 지침과 의료진의 지시가 필요합니다.'},
    {id:'b',text:'증상이 있는 동안 추가 사정 없이 상황만 관찰한다.',feedback:'저혈압과 어지럼이 지속되는 상황에서 평가·보고 지연은 적절하지 않습니다.'},
    {id:'c',text:'ABC·맥박·혈압·ECG를 재확인하고 기관 지침에 따라 즉시 보고·대응을 지원한다.',feedback:'적절합니다. 환자 안전을 우선으로 팀과 협력하여 확인·모니터링·보고합니다.'}
   ],correctChoiceId:'c',rationale:'환자의 호흡·순환과 관류를 사정하고 기관의 응급 보고/대응 체계와 처방을 따릅니다. 이 교육용 사례는 약물 투여량이나 처치 효과를 예측하지 않습니다.',referenceIds:[refA],relatedUnitIds:['unit-nursing','unit-conduction']},
  {id:'reassess',phase:'reassessment',prompt:'10:15 재평가에서 어지럼이 지속되고 HR 46회/분, 혈압 90/58 mmHg라면?',
   choices:[
    {id:'a',text:'혈압 수치가 조금 달라졌으므로 증상을 무시하고 안정되었다고 결론 내린다.',feedback:'측정값 일부의 변화만으로 안정화되었다고 판단할 수 없습니다. 지속 증상과 관류 상태를 확인해야 합니다.'},
    {id:'b',text:'환자 증상·관류·추적 활력징후를 재사정하고 문제 지속을 팀에 공유한다.',feedback:'적절합니다. 지속 증상과 추가 결과를 함께 재평가합니다.'},
    {id:'c',text:'혈청 칼륨이 예시 참고범위에 있으므로 모든 위험이 해소되었다고 판단한다.',feedback:'단일 검사값이 참고범위 안에 있어도 환자의 혈압과 지속 증상을 배제하지 않습니다.'}
   ],correctChoiceId:'b',rationale:'임상적 악화/개선 여부는 수치 하나가 아닌 환자 상태와 시계열 관찰을 종합해 평가하며 필요 시 추가 보고합니다.',referenceIds:[refA,refM],relatedUnitIds:['unit-nursing','unit-wiggers']}
 ]
};
function deepFreeze(o){if(o&&typeof o==='object'&&!Object.isFrozen(o)){Object.values(o).forEach(deepFreeze);Object.freeze(o);}return o;}
const frozen=deepFreeze(caseOne);
function validateCase(c){
 const errors=[],check=(ok,s)=>{if(!ok)errors.push(s);};
 const isTime=x=>typeof x==='string'&&!Number.isNaN(Date.parse(x))&&x.includes('+09:00');
 const unique=(arr,key,label)=>{check(new Set(arr.map(o=>o[key])).size===arr.length,'duplicate '+label);};
 check(c.schemaVersion===1,'schema version');check(c.fictional===true,'fictional missing');
 check(c.status==='draft-human-review-pending'||c.status==='clinical-reviewed','review status');
 check(Array.isArray(c.questions)&&c.questions.length>=1,'missing questions');
 const obs=[...c.baseline.measurements,...c.reassessment.measurements];
 unique(obs,'id','vitals');unique(c.labs,'id','labs');unique(c.questions,'id','questions');
 check(isTime(c.baseline.at)&&isTime(c.reassessment.at),'invalid case times');
 check(Date.parse(c.reassessment.at)>Date.parse(c.baseline.at),'reassessment order');
 for(const v of obs){check(isTime(v.observedAt),'vital time '+v.id);check(v.value!==null&&v.unit,'missing vital value/unit '+v.id);}
 check(c.ecg?.kind!=='simulator-derived'&&isTime(c.ecg?.recordedAt)&&Boolean(c.ecg?.limitation),'ECG boundary');
 for(const lab of c.labs){
  check(['known','pending','not-obtained'].includes(lab.status),'lab state '+lab.id);
  check(isTime(lab.collectedAt)&&lab.unit&&lab.range,'lab metadata '+lab.id);
  if(lab.status==='known'){
   check(typeof lab.value==='number'&&Number.isFinite(lab.value)&&isTime(lab.availableAt),'known lab missing number/time '+lab.id);
   check(Date.parse(lab.availableAt)>=Date.parse(lab.collectedAt),'lab available before collection '+lab.id);
  }else check(lab.value===null&&lab.availableAt===null,'pending lab leaks value '+lab.id);
  check(Number.isInteger(lab.availableFromPhase)&&lab.availableFromPhase>=0&&lab.availableFromPhase<phaseIds.length,'lab visibility phase '+lab.id);
 }
 const refs=new Set(c.references.map(x=>x.id));unique(c.references,'id','reference');
 for(const [i,q] of c.questions.entries()){
  check(q.phase===phaseIds[i],'question phase order '+q.id);
  check(q.choices.length>=2,'few choices '+q.id);unique(q.choices,'id','choices '+q.id);
  check(q.choices.filter(x=>x.id===q.correctChoiceId).length===1,'invalid answer '+q.id);
  check(q.choices.every(x=>x.text&&x.feedback),'missing option feedback '+q.id);
  check(Boolean(q.rationale)&&q.referenceIds.length>0&&q.referenceIds.every(x=>refs.has(x)),'unsupported rationale '+q.id);
  check(q.relatedUnitIds.length>0&&q.relatedUnitIds.every(x=>validUnits.has(x)),'broken learning deep link '+q.id);
 }
 return errors;
}
const errors=validateCase(frozen);
if(errors.length)throw new Error('Invalid v1.13 clinical case: '+errors.join(', '));
root.CardiacClinicalCasesV113=Object.freeze({first:frozen,validateCase,phaseIds});
})(window);
