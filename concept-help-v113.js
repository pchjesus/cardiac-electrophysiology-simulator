/*
 * v1.13 Korean-language concept explanations.
 * Informational, student-invoked modal only: never changes heartState,
 * A/B time, Guided Learning, case/session, native views or Timeline.
 */
(function(root){
'use strict';
const source={
 physiology:{label:'OpenStax · 심장주기',url:'https://openstax.org/books/anatomy-and-physiology/pages/19-3-cardiac-cycle'},
 wiggers:{label:'NCBI Bookshelf · 심장주기와 위거스 도표',url:'https://www.ncbi.nlm.nih.gov/books/NBK459327/'},
 ecg:{label:'NCBI Bookshelf · 기본 심전도 해석',url:'https://www.ncbi.nlm.nih.gov/books/NBK594493/'}
};
const content=Object.freeze({
 wiggers:{
  title:'위거스 도표(Wiggers diagram)',
  meaning:'심장 한 번의 박동에서 심전도, 심방·심실·대동맥의 압력 변화, 심실 용적, 판막 개폐와 심음 사건을 같은 시간축 위에 함께 배치한 도표입니다.',
  reason:'심전도에서 QRS가 나타난 뒤 심실이 수축하고, 심실 압력이 올라 판막이 열리면 혈액이 박출되는 흐름을 한눈에 연결할 수 있습니다. 각각의 그래프를 따로 외우기보다 사건의 순서를 이해하는 데 유용합니다.',
  method:'① 위쪽 압력 곡선에서 어느 쪽 압력이 높은지 살펴봅니다. ② ECG의 P·QRS·T와 심방·심실 수축·이완을 연결합니다. ③ 판막이 열리고 닫히는 시점과 심실 용적의 증가·감소를 비교합니다. ④ S1·S2 표지로 판막 폐쇄와 심음을 연결합니다.',
  caution:'이 앱의 압력과 용적은 실제 혈압(mmHg)이나 심실 용적(mL)이 아닌 상대 지표입니다. S1·S2는 녹음된 심음이 아니라 교육용 사건 표지입니다. 그래프를 환자 검사 결과처럼 해석하면 안 됩니다.',
  reference:source.wiggers
 },
 ecg:{
  title:'심전도(ECG)',
  meaning:'심장이 뛰는 동안 나타나는 전기 활동을 피부에 부착한 전극으로 기록한 파형입니다. P파는 심방 탈분극, QRS파는 심실 탈분극, T파는 심실 재분극과 관련됩니다.',
  reason:'맥박의 빠르기뿐 아니라 전기 신호가 어떤 순서로 나타나는지 살피는 데 도움이 됩니다. 다만 ECG의 전기 신호가 곧 효과적인 심근 수축이나 혈액 순환을 보장하지는 않습니다.',
  method:'P파 → QRS파 → T파를 순서대로 읽고, 각 파형의 간격을 비교합니다. 실제 환자를 평가할 때는 맥박·혈압·의식·호흡·증상과 반드시 함께 판단합니다.',
  caution:'시뮬레이터의 파형은 정상 동율동 교육용 모델입니다. 실제 환자의 병적 부정맥 진단이나 치료 판단에 사용할 수 없습니다.',
  reference:source.ecg
 },
 conduction:{
  title:'심장 전도계(cardiac conduction system)',
  meaning:'심장이 규칙적으로 수축할 수 있도록 전기 신호를 만들어 전달하는 조직입니다. 동방결절(SA) → 심방 → 방실결절(AV) → 히스속(His bundle) → 좌·우 각(bundle branches) → 푸르키녜 섬유(Purkinje fibers) 순으로 전달됩니다.',
  reason:'심방과 심실이 서로 다른 시점에 활성화되는 이유를 이해하고, 심전도 P파와 QRS파의 순서가 만들어지는 원리를 배울 수 있습니다.',
  method:'전도 그림의 불빛이 어떤 구조를 지나는지 관찰한 뒤 ECG의 P파·PR 간격·QRS파와 대조해 보세요.',
  caution:'전기 신호의 이동과 실제 근육 수축에는 시간 차가 있습니다. 이 화면은 모든 전도장애나 부정맥을 재현하지 않습니다.',
  reference:source.physiology
 },
 mechanical:{
  title:'심장 기계 활동(mechanical activity)',
  meaning:'전기 신호를 받은 심근이 실제로 수축·이완하고 판막이 열리거나 닫히면서 혈액이 흐르는 과정입니다.',
  reason:'심전도에서 보이는 전기 변화가 어떻게 혈류와 심음으로 연결되는지 이해할 수 있습니다. 등용적 수축·이완은 판막이 닫힌 동안 심실 용적이 거의 변하지 않는 단계입니다.',
  method:'심방·심실의 모형을 보면서 판막의 열림/닫힘, 혈류 방향, 심실 용적 변화를 순서대로 비교합니다.',
  caution:'그림과 압력·용적 값은 설명을 위한 단순화된 모형이며 실제 해부학적 크기나 환자의 혈역학 검사값을 나타내지 않습니다.',
  reference:source.physiology
 },
 timing:{
  title:'심장주기 시간과 타임라인(timeline)',
  meaning:'심장주기(cardiac cycle)는 심장이 한 번 수축하고 이완해 다음 박동으로 이어지는 과정입니다. RR 간격은 연속한 두 R파 사이의 시간으로 박동 주기를 나타냅니다.',
  reason:'심박수가 빨라지거나 느려질 때 한 박동의 시간이 어떻게 달라지는지 이해할 수 있습니다.',
  method:'타임라인을 직접 움직여 전도·ECG·판막·심장주기 사건이 같은 생리학적 시간(A)을 따라 바뀌는지 관찰하세요.',
  caution:'화면의 ECG가 오른쪽으로 흘러가는 표시 속도(B)는 생리학적 시간(A)과 별도로 관리됩니다. 타임라인 이동은 기존 재생을 멈추고 관찰 시점으로 이동합니다.',
  reference:source.ecg
 },
 intervals:{
  title:'심전도 간격(PR·QRS·QT·QTc)',
  meaning:'PR 간격은 P파 시작부터 QRS 시작까지의 시간, QRS 폭은 심실 탈분극 시간, QT 간격은 심실 탈분극 시작부터 재분극이 끝날 때까지의 시간입니다. QTc는 심박수의 영향을 보정한 QT 값입니다.',
  reason:'전도와 재분극의 시간적 관계를 학습하고, 심박수 변화에 따라 표시값이 달라지는 이유를 이해하는 데 도움이 됩니다.',
  method:'심박수를 바꾼 뒤 RR·PR·QRS·QT·QTc 표시를 비교하세요. 각 값은 같은 종류의 시간이 아니므로 구분해 읽습니다.',
  caution:'앱의 시간 간격과 QTc는 교육용 수학 모델에서 얻은 값입니다. 환자의 실제 심전도 판독값이나 QT 연장 진단 결과가 아닙니다.',
  reference:source.ecg
 },
 heartsound:{
  title:'심음과 판막 사건(S1·S2)',
  meaning:'첫 번째 심음(S1)은 주로 승모판·삼첨판 폐쇄와, 두 번째 심음(S2)은 주로 대동맥판·폐동맥판 폐쇄와 관련됩니다.',
  reason:'청진으로 들리는 심음이 심장주기 중 어느 시점의 판막 사건과 연관되는지 이해하는 데 중요합니다.',
  method:'Wiggers 그래프의 S1·S2 표시와 승모판·대동맥판의 닫힘 사건, 심실 압력 변화의 순서를 함께 보세요.',
  caution:'이 앱에서는 좌측 판막의 대표 사건만 간략히 표시하며 실제 심음 소리, 분열이나 심잡음을 재생하지 않습니다.',
  reference:source.physiology
 },
 clinical:{
  title:'간호 사정(nursing assessment)',
  meaning:'환자의 상태를 파악하기 위해 증상과 의식·호흡·맥박·혈압·산소화·말초관류 등 여러 정보를 함께 확인하는 과정입니다.',
  reason:'심박수만으로 환자가 안정적인지 결정할 수 없습니다. 같은 서맥이라도 증상과 혈압·관류에 따라 신속한 확인과 보고가 필요할 수 있습니다.',
  method:'심전도와 활력징후를 함께 확인하고, 이상 소견이 있을 때는 환자 상태를 재사정해 기관 지침에 따라 보고·대응합니다.',
  caution:'임상 탭의 환자는 가상 사례이며 내용은 아직 전문가 검토 전입니다. 앱은 독립적인 처방·시술 판단 도구가 아닙니다.',
  reference:source.physiology
 }
});
const el=(tag,cls,text)=>{
 const e=document.createElement(tag);
 if(cls)e.className=cls;
 if(text!==undefined)e.textContent=text;
 return e;
};
const dialog=el('dialog','v113-concept-dialog');
dialog.id='v113ConceptDialog';
dialog.setAttribute('aria-labelledby','v113ConceptTitle');
dialog.setAttribute('aria-describedby','v113ConceptMeaning');
const header=el('div','v113-concept-heading');
const title=el('h2','', '용어 설명');title.id='v113ConceptTitle';
const closeBtn=el('button','v113-concept-close','닫기 ×');
closeBtn.type='button';closeBtn.setAttribute('aria-label','용어 설명 팝업 닫기');
header.append(title,closeBtn);
const area=el('div','v113-concept-body');
dialog.append(header,area);
document.body.append(dialog);
let invoking=null;
function open(id,trigger){
 const info=content[id];if(!info)return false;
 invoking=trigger||document.activeElement;
 title.textContent=info.title;
 area.replaceChildren();
 for(const [heading,text] of [
  ['무슨 뜻인가요?',info.meaning],
  ['왜 중요한가요?',info.reason],
  ['어떻게 살펴보나요?',info.method],
  ['학습할 때 주의할 점',info.caution]
 ]){
  const section=el('section','v113-concept-section');
  const h=el('h3','',heading);
  const p=el('p','',text);
  if(heading==='무슨 뜻인가요?')p.id='v113ConceptMeaning';
  section.append(h,p);area.append(section);
 }
 const a=el('a','v113-concept-source','더 읽기: '+info.reference.label);
 a.href=info.reference.url;a.target='_blank';a.rel='noopener noreferrer';
 area.append(a);
 if(dialog.open)dialog.close();
 dialog.showModal();closeBtn.focus();
 return true;
}
function close(){if(dialog.open)dialog.close();}
closeBtn.addEventListener('click',close);
dialog.addEventListener('click',event=>{
 if(event.target===dialog)close();
});
dialog.addEventListener('close',()=>{
 if(invoking?.isConnected)invoking.focus({preventScroll:true});
 invoking=null;
});
document.addEventListener('click',event=>{
 const trigger=event.target.closest?.('[data-concept-help]');
 if(!trigger)return;
 event.preventDefault();
 open(trigger.getAttribute('data-concept-help'),trigger);
});
root.CardiacConceptHelpV113=Object.freeze({open,get keys(){return Object.keys(content);}});
})(window);
