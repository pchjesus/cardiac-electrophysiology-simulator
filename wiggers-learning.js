/*
 * v1.10 Patch 5 — read-only scientific/nursing scenario interpretation.
 * Uses the existing physiological A clock and Patch 2 Wiggers snapshot.
 * Preset buttons delegate to the ORIGINAL HR slider; no alternate clock,
 * hemodynamic model, animation driver or clinical-patient estimates.
 */
(function(root){
 'use strict';
 const panel=document.getElementById('wiggersDetails');
 const dive=document.getElementById('wiggersDeepDive');
 const slider=document.getElementById('heartRateSlider');
 const summary=document.getElementById('learningScenarioSummary');
 const intro=document.getElementById('learningScenarioIntro');
 const duration=document.getElementById('learningDuration');
 const stageTitle=document.getElementById('learningPhaseTitle');
 const electrical=document.getElementById('learningElectrical');
 const hemo=document.getElementById('learningHemodynamics');
 const volume=document.getElementById('learningVolume');
 const nursing=document.getElementById('learningNursing');
 const compare=document.getElementById('learningRateComparison');
 const caution=document.getElementById('learningCaution');
 const buttons=[...document.querySelectorAll('[data-learning-preset]')];
 if(!panel||!dive||!slider||!summary||!root.CardiacWiggersProfile||
    !buttons.length)return;
 const PRESETS=Object.freeze({normal:72,bradycardia:50,tachycardia:120});
 const LABELS=Object.freeze({
   filling:'Ventricular filling · 심실 충만',
   atrial_systole:'Atrial systole · 심방 수축',
   isovolumetric_contraction:'Isovolumetric contraction · 등용적 수축',
   ejection:'Ventricular ejection · 심실 박출',
   isovolumetric_relaxation:'Isovolumetric relaxation · 등용적 이완'
 });
 const PHASES=Object.freeze({
  filling:{
   electrical:'심실 이완기에 해당하는 부분이다. 이 시기 ECG는 직전 심실 재분극 이후의 기저선과 다음 심방 전기활동으로 이어질 수 있다. ECG의 평탄한 선이 곧 수축·이완 정지를 뜻하지는 않는다.',
   hemo:'이전 박동에서 대동맥판이 닫힌 뒤 심실 압력이 떨어지고, 좌심방 압력이 좌심실보다 우세해지면 승모판이 열려 충만이 시작된다. 그림의 승모판 열림은 모델 사건 시점에 의해 결정된다.',
   volume:'승모판이 열려 혈액이 좌심방에서 좌심실로 흐르는 생리학적 충만 동안 심실 용적은 일반적으로 증가한다. 단, 이 시뮬레이터의 RR 초반 filling 구간은 상대 LV 용적 0.88로 평탄하게 그려지며, RR 후반 filling 구간에서만 0.48에서 0.88로 증가한다. 이 교육용 상대값은 실제 충만량, 전부하나 EF를 정량화하지 않는다.',
   nursing:'임상에서는 심박수만 보지 않고 혈압, 의식·현기증, 말초관류, 호흡곤란, 체액상태를 함께 사정한다. 심첨부·심저부 청진과 맥박·ECG의 시간적 관계를 연결해 생각한다.',
   caution:'모델의 한 박동은 일정한 좌심방·좌심실 관계를 가정한다. 실제 충만은 정맥환류, 심실 순응도, 이완 특성, 전부하 등에 따라 달라지며 여기서는 계산하지 않는다.'
  },
  atrial_systole:{
   electrical:'P파는 심방 탈분극을 나타내며, 심방의 실제 수축은 전기적 활성화 이후에 일어난다. PR 구간은 방실 전도와 심방-심실 활성화의 시간 차를 이해하는 데 도움이 된다.',
   hemo:'승모판이 열린 동안 심방 수축은 심실로의 마지막 충만을 보조한다. 심실 수축이 시작되기 전이며, 심방 수축이 반드시 모든 박동에서 일정한 비율의 충만을 담당하는 것은 아니다.',
   volume:'심실 이완기 말기에 상대 용적이 증가하는 구간이다. '+
     '이 시뮬레이터에서의 증가폭은 교육용 곡선의 선택값이지 임상에서 측정된 atrial kick의 기여량이 아니다.',
   nursing:'P-QRS 순서와 규칙성을 확인하되, P파가 있다고 기계적 심방 수축이나 적절한 심실 충만이 완전히 보장된다고 단정하지 않는다. 환자의 맥박과 혈압·증상을 함께 본다.',
   caution:'전기적-기계적 지연은 단순화되어 있다. 실제 방실 동기, 심방기능 및 승모판 질환의 영향은 모델에 포함되지 않는다.'
  },
  isovolumetric_contraction:{
   electrical:'QRS 복합체는 심실 탈분극이며, 이후 심근의 장력 발달과 압력 상승이 뒤따른다. ECG 신호와 실제 수축의 시작은 동일 시각의 사건이 아니다.',
   hemo:'좌심실 압력이 좌심방 쪽을 넘어서며 승모판이 닫히고 S1에 대응하는 대표 사건이 표시된다. 아직 대동맥판은 열리지 않아 두 판막 사이에 유효한 박출 흐름이 없다.',
   volume:'좌심실 압력은 상승하지만 두 판막이 닫혀 상대 용적이 일정하다. 이름의 등용적(isovolumetric)은 압력이 일정하다는 뜻이 아니라 용적이 일정하다는 뜻이다.',
   nursing:'S1을 심실 수축의 시작과 연관 지어 이해한다. 실제 S1은 주로 승모판·삼첨판 폐쇄에 관련되며 심음의 강도·분열이나 잡음은 여기서 재현하지 않는다.',
   caution:'정확한 판막 경계에서는 Patch 2 사건 규칙을 우선한다. Mechanical 모드의 이전 부동소수점 판정과 일순간 차이가 날 수 있다.'
  },
  ejection:{
   electrical:'심실 탈분극 후 발생한 기계적 수축이 이어지는 시기다. 심실 재분극을 나타내는 T파는 기계적 박출의 후반과 겹칠 수 있지만, 박출 종료 순간을 ECG의 한 지점과 동일시하지 않는다.',
   hemo:'좌심실 압력이 대동맥 쪽의 열림 조건을 충족하여 대동맥판이 열린다. 혈액이 대동맥으로 나가며, 이 모델에서는 승모판이 닫힌 상태다.',
   volume:'심실 박출이 진행되는 동안 상대 좌심실 용적이 감소한다. 감소 곡선은 정규화된 교육용 도식으로서 일회박출량, EF, 심박출량으로 환산할 수 없다.',
   nursing:'심장의 전기 신호가 보이더라도 실제 혈류와 조직 관류가 충분한지는 별도로 확인해야 한다. 맥박, 혈압, 피부 상태, 의식, 호흡을 함께 사정하는 이유를 연결한다.',
   caution:'후부하, 수축력, 대동맥 순응도와 심실 압력 절대값을 계산하지 않는다. 심박수가 높다고 이 모형에서 박출량 감소를 수치로 예측할 수 없다.'
  },
  isovolumetric_relaxation:{
   electrical:'심실 재분극과 기계적 이완은 시간상 관련되지만 일치하는 단일 점은 아니다. T파가 끝났다는 사실만으로 승모판이 열린 시점을 판정할 수 없다.',
   hemo:'대동맥판이 닫히는 시점은 S2의 대표적인 대동맥판 관련 사건이다. 승모판이 열리기 전까지 두 판막이 닫힌 상태에서 심실 압력이 하강한다.',
   volume:'혈액의 유출과 유입이 제한되므로 상대 심실 용적은 낮은 상태로 유지된다. 이후 심실 압력이 좌심방 압력 아래로 떨어지면 승모판이 열린다.',
   nursing:'S2는 주로 대동맥판·폐동맥판 폐쇄와 연관된다. 실제 청진에서는 위치, 호흡에 따른 변화, 추가 심음이나 잡음과 임상 징후를 종합한다.',
   caution:'S2는 소리 파일이 아닌 사건 마커이고 좌우 심장의 독립적인 폐쇄 시점이나 생리적 분열은 시뮬레이션하지 않는다.'
  }
 });
 const RATE=Object.freeze({
  bradycardia:{
   title:'서맥 범위의 동성 모형',
   intro:'성인 안정 시 60 bpm 미만은 일반적으로 서맥 범위다. 그러나 수면·운동선수 등에서 생리적일 수 있다. 원인을 모르고 이 수치만으로 관류 저하나 치료 필요성을 판단하면 안 된다.',
   compare:'RR이 길어지면 한 박동에 사용할 수 있는 시간이 커진다. 이는 충만 시간을 관찰하는 기회이지만, 실제 충만량이 항상 늘거나 분당 심박출량이 적절하다는 뜻은 아니다.',
   nursing:'증상, 활력징후, 의식 변화, 어지럼·실신, 흉통·호흡곤란, 약물·기저질환을 확인하는 사고 연습에 활용한다. 이 모형은 방실차단 또는 불안정 서맥을 재현하지 않는다.'
  },
  normal:{
   title:'정상 범위의 동성 모형',
   intro:'성인 안정 시 일반적인 60–100 bpm 범위의 동성 주기를 살핀다. 정상 범위라는 숫자만으로 심장 기능·전도 상태·혈역학이 정상이라는 결론을 내리지는 않는다.',
   compare:'전기적 활성화→심근 수축→판막 전환→충만/박출을 기준 흐름으로 읽는다. 이 도식의 간격은 실제 특정 환자의 심장주기와 일대일로 대응하지 않는다.',
   nursing:'ECG의 P-QRS-T, 맥박수와 규칙성, S1/S2 청진 위치와 환자 증상을 통합해서 해석한다. 심박수가 정상이어도 관류 문제가 있을 수 있다.'
  },
  tachycardia:{
   title:'빈맥 범위의 동성 모형',
   intro:'성인 안정 시 100 bpm 초과는 빈맥 범위다. 운동, 발열, 통증, 탈수 등에 따른 동성 반응일 수도 있어 원인과 안정 상태 여부를 같이 살펴야 한다.',
   compare:'RR이 짧아질 때 이완기 충만에 이용 가능한 절대 시간이 감소할 수 있다. 그러나 심박출량 변화는 전부하·수축력·후부하 등 여러 변수에 달려 있고, 이 모델은 이를 추산하지 않는다.',
   nursing:'체온, 통증, 산소화, 체액 부족·출혈 가능성, 혈압·의식·말초관류와 리듬을 종합한다. 단순히 HR 숫자를 낮추는 것이 언제나 적절한 것은 아니다.'
  }
 });
 let activePreset=null;
 let dispatchingPreset=false;
 let lastKey='';
 let renderCount=0;
 const set=(el,value)=>{if(el&&el.textContent!==value)el.textContent=value;};
 const heartRateCategory=hr=>hr<60?'bradycardia':hr<=100?'normal':'tachycardia';
 function updatePresetButtons(){
  for(const button of buttons){
   const chosen=button.dataset.learningPreset===activePreset;
   button.setAttribute('aria-pressed',String(chosen));
   button.classList.toggle('learning-preset-active',chosen);
  }
 }
 function sync(){
  if(!panel.open&&!root.CardiacDashboard)return;
  const t=getActiveTiming(),hr=Number(slider.value);
  if(!Number.isFinite(hr))return;
  const type=heartRateCategory(hr);
  const tag=RATE[type];
  const chosen=activePreset ? (' · Preset: '+activePreset) : ' · Custom HR';
  set(summary,tag.title+' · '+hr+' bpm'+chosen);
  set(intro,tag.intro);
  const bounds=root.CardiacMechanical.getMechanicalTiming(t);
  const filling=bounds.rr-bounds.relaxationEnd+bounds.contractionStart;
  set(duration,'모델에서 계산한 RR '+Math.round(t.rr)+' ms · 승모판 개방~다음 폐쇄 간격 약 '+
      Math.round(filling)+' ms. 이는 교육 모델의 시간 창이지 측정된 이완기 충만시간이나 실제 충만량이 아니다.');
  updatePresetButtons();
  if(!dive.open)return;
  const ready=!heartState.playing&&heartState.currentStep===-1&&
     heartState.physiologicalTime===0&&heartState.visualizationTime===0;
  if(ready){
   set(stageTitle,'Ready · 시작 전');
   set(electrical,'재생하거나 Timeline을 이동하면 현재 단계의 전기적 활동과 기계적 사건을 설명한다.');
   set(hemo,'압력 및 판막 관계는 실제 환자 수치가 아닌 모형의 사건 경계에 기반한다.');
   set(volume,'좌심실 용적은 상대값이며 mL 또는 EF로 해석하지 않는다.');
   set(nursing,tag.nursing);
   set(compare,tag.compare);
   set(caution,'교육용 동성 박동 모형 · 실제 임상 판단/치료 예측 불가');
   lastKey='';
   return;
  }
  const snapshot=root.CardiacWiggersProfile.getSnapshot(getPhysiologicalCyclePhase(),t);
  const phase=snapshot.mechanical.stage;
  const key=[hr,type,phase,activePreset].join('|');
  if(lastKey===key)return;
  lastKey=key;
  const data=PHASES[phase];
  if(!data)return;
  set(stageTitle,LABELS[phase]+' · '+hr+' bpm');
  set(electrical,data.electrical);
  set(hemo,data.hemo);
  set(volume,data.volume);
  set(nursing,data.nursing+' '+tag.nursing);
  set(compare,tag.compare);
  set(caution,data.caution+' 이 자료는 질환 진단이나 환자 예측을 위한 것이 아니다.');
  renderCount++;
 }
 function reset(){
   lastKey='';
   sync();
 }
 for(const button of buttons){
  button.addEventListener('click',()=>{
   const id=button.dataset.learningPreset,hr=PRESETS[id];
   if(!Number.isFinite(hr))return;
   activePreset=id;dispatchingPreset=true;
   slider.value=String(hr);
   slider.dispatchEvent(new Event('input',{bubbles:true}));
   dispatchingPreset=false;
   sync();
  });
 }
 slider.addEventListener('input',()=>{
  if(!dispatchingPreset){activePreset=null;lastKey='';}
  sync();
 });
 panel.addEventListener('toggle',()=>{lastKey='';sync();});
 dive.addEventListener('toggle',()=>{lastKey='';sync();});
 function getInspectorNarrative(){
   const hr=Number(slider.value);
   const label=heartRateCategory(hr);
   const timing=getActiveTiming();
   const snapshot=root.CardiacWiggersProfile.getSnapshot(getPhysiologicalCyclePhase(),timing);
   const phase=snapshot.mechanical.stage;
   const content=PHASES[phase];
   const rate=RATE[label];
   return {
     phase,heartRate:hr,
     title:LABELS[phase]||phase,
     electrical:content?.electrical||'',
     hemodynamics:content?.hemo||'',
     volume:content?.volume||'',
     nursing:(content?.nursing||'')+' '+rate.nursing,
     comparison:rate.compare,
     caution:content?.caution||'',
     rateCategory:label
   };
 }
 function getStageNarrative(stageId){
   // Single authoritative source for v1.12 learning: no duplicated
   // physiological/nursing descriptions in the presentation adapter.
   const content=PHASES[stageId];
   if(!content)return null;
   const hr=Number(slider.value);
   const category=heartRateCategory(hr);
   return Object.freeze({
     phase:stageId,title:LABELS[stageId],
     electrical:content.electrical,hemodynamics:content.hemo,
     volume:content.volume,nursing:content.nursing,
     caution:content.caution,comparison:RATE[category].compare,
     heartRate:hr,rateCategory:category
   });
 }
 root.CardiacLearning=Object.freeze({
  sync,reset,getInspectorNarrative,getStageNarrative,
  get activePreset(){return activePreset;},
  get renderCount(){return renderCount;},
  get category(){return heartRateCategory(Number(slider.value));}
 });
})(window);
