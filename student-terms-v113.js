/* v1.13 UX Patch 2: one Korean-first educational concept dialog.
 * Read-only; no A/B engine, Timeline, HR, quiz or clinical session mutations.
 */
(function(root){
'use strict';
const terms=Object.freeze({
 wiggers:{title:'위거스 도표(Wiggers diagram)',
  meaning:'한 번의 심장주기에서 심전도, 심방·심실·대동맥의 압력 변화, 심실 용적 변화, 판막 개폐와 심음 발생 시점을 시간 순서대로 비교하는 그림입니다.',
  important:'심전도에서 보이는 전기적 사건이 언제 실제 심장 수축·이완, 혈액의 이동과 연결되는지 이해하는 데 도움이 됩니다. 간호학에서는 파형과 맥박·혈압·심음의 의미를 구별하는 연습에 유용합니다.',
  method:'먼저 P파·QRS파·T파를 찾고, 이어서 승모판과 대동맥판의 개폐, 심실 압력과 용적이 증가하거나 감소하는 구간을 같은 시간축에서 비교해 보세요.',
  caution:'이 앱의 압력·용적 곡선은 교육용 상대값입니다. 실제 환자의 혈압(mmHg), 심실 용적(mL), 박출률(EF) 또는 심박출량이 아니며, S1·S2는 실제 녹음 소리가 아닌 사건 표시입니다.'},
 ecg:{title:'심전도(ECG, electrocardiogram)',
  meaning:'심장의 전기적 활동을 몸 표면에서 기록한 파형입니다. P파는 주로 심방 탈분극, QRS파는 주로 심실 탈분극, T파는 주로 심실 재분극을 나타냅니다.',
  important:'심박수와 리듬, 전기 전도 과정의 단서를 관찰할 수 있습니다. 하지만 심전도에 전기 신호가 보인다는 사실만으로 실제 맥박이나 장기 관류가 충분하다고 단정할 수 없습니다.',
  method:'P파 → QRS파 → T파의 순서와 간격을 살펴보고, 실제 환자 사정에서는 맥박·혈압·의식·증상·관류 상태를 함께 확인합니다.',
  caution:'시뮬레이터는 정상 동율동의 교육용 모형이며 모든 부정맥이나 환자 상태를 진단하지 않습니다.'},
 electrical:{title:'전기적 전도(Electrical conduction)',
  meaning:'동방결절(SA)에서 만들어진 전기적 자극이 심방, 방실결절(AV), 히스다발 및 푸르키녜 섬유를 거쳐 심실로 전달되는 과정입니다.',
  important:'전기 신호의 순서가 심장 수축의 순서를 이끕니다. 심전도 파형과 기계적 수축이 왜 동시에 발생하지 않는지 이해할 수 있습니다.',
  method:'전기 전도 화면의 점등 순서와 심전도 P파·QRS파를 비교하세요.',
  caution:'전기적 활성화와 실제 판막 움직임·혈액 박출의 시점은 같지 않습니다.'},
 mechanical:{title:'기계적 심장주기(Mechanical cardiac cycle)',
  meaning:'전기적 자극 이후 심장근육이 수축·이완하고 판막이 열리거나 닫히며 혈액이 이동하는 과정입니다.',
  important:'심음, 판막 개폐, 심실 충만과 박출을 연결해 이해하는 데 도움 됩니다. ECG 신호만 보고 혈류를 직접 측정한 것처럼 해석하지 않도록 합니다.',
  method:'등용적 수축·심실 박출·등용적 이완·충만 단계에서 판막과 상대 용적이 어떻게 변하는지 관찰하세요.',
  caution:'그림과 수치는 교육용 상대 모형으로 실제 환자의 심실 용적이나 심박출량을 계산하지 않습니다.'},
 timeline:{title:'심장주기 시간축(Timeline)',
  meaning:'하나의 심장주기(RR 간격) 중 어디를 보고 있는지 나타내는 조절 도구입니다.',
  important:'전기 신호와 기계적 사건의 앞뒤 관계를 같은 주기 안에서 비교할 수 있습니다.',
  method:'시간축을 직접 움직이거나 기존 5단계 학습에서 관찰 버튼을 누르면 해당 시점으로 이동합니다.',
  caution:'시간축을 움직이면 재생이 일시정지되고 기존 생리학적 시간(A)과 화면 표시 시간(B)의 상태가 갱신됩니다. 단원 목록을 고르는 것만으로는 시간이 이동하지 않습니다.'},
 measurements:{title:'심전도 측정값(ECG measurements)',
  meaning:'심박수(HR), RR·PR·QRS·QT·QTc 등 심전도에 나타나는 주요 시간 간격을 표시합니다.',
  important:'심장이 얼마나 자주 뛰는지와 전기적 흥분이 어느 정도 시간에 걸쳐 전달·회복되는지 이해할 수 있습니다.',
  method:'심박수를 바꾸며 RR·QT 등의 교육용 표시값이 어떻게 달라지는지 비교하세요.',
  caution:'QTc는 심박수에 따른 보정 추정값이며 이 앱의 표시값은 실제 환자 진단이나 약물 처방 기준이 아닙니다.'},
 nursing:{title:'환자 사정(Nursing assessment)',
  meaning:'심전도 숫자뿐 아니라 환자의 증상, 혈압, 의식, 호흡, 맥박과 말초관류를 함께 살피는 과정입니다.',
  important:'같은 심박수에서도 환자의 상태는 다를 수 있으므로 모니터 수치만으로 임상적 안정성을 단정하지 않도록 합니다.',
  method:'심전도를 보며 환자가 어지러운지, 혈압이 낮은지, 호흡이나 의식 변화가 있는지 함께 확인한다고 생각해 보세요.',
  caution:'이 앱의 가상 시나리오는 교육용이며 실제 응급처치·처방 판단을 대신하지 않습니다.'}
});
const dialog=document.createElement('section');
dialog.id='v113TermDialog';dialog.className='v113-term-dialog';dialog.hidden=true;
dialog.setAttribute('role','dialog');dialog.setAttribute('aria-modal','false');
dialog.setAttribute('aria-labelledby','v113TermTitle');
const top=document.createElement('div');top.className='v113-term-heading';
const title=document.createElement('h2');title.id='v113TermTitle';
const closeButton=document.createElement('button');closeButton.type='button';
closeButton.className='v113-term-close';closeButton.textContent='닫기 ×';
closeButton.setAttribute('aria-label','용어 설명 닫기');
top.append(title,closeButton);
const body=document.createElement('div');body.id='v113TermBody';
dialog.append(top,body);document.body.append(dialog);
let opener=null;
function close(restore){
 if(dialog.hidden)return;
 dialog.hidden=true;const prior=opener;opener=null;
 if(restore&&prior?.isConnected)prior.focus();
}
function open(key,source){
 const item=terms[key];if(!item)return false;
 if(!dialog.hidden)close(false);
 opener=source||document.activeElement;
 title.textContent=item.title;body.replaceChildren();
 for(const [heading,content] of [['무엇인가요?',item.meaning],['왜 중요한가요?',item.important],
  ['어떻게 살펴보나요?',item.method],['학습 시 주의',item.caution]]){
  const section=document.createElement('section');
  const h=document.createElement('h3');h.textContent=heading;
  const p=document.createElement('p');p.textContent=content;
  section.append(h,p);body.append(section);
 }
 dialog.hidden=false;closeButton.focus();
 return true;
}
// Add short educational triggers beside established controls.
for(const [selector,key,label] of [
 ['.dashboard-inspector-heading','nursing','환자 사정 설명'],
 ['.ecg-panel h2','ecg','심전도 설명'],
 ['.dashboard-wiggers-button','wiggers','위거스 도표 설명'],
 ['#electricalModeBtn','electrical','전기 전도 설명'],
 ['#mechanicalModeBtn','mechanical','심장 수축·판막 설명'],
 ['.measurements-panel h2','measurements','측정값 설명'],
 ['.timeline .control-title','timeline','시간축 설명']
]){
 const host=document.querySelector(selector);
 if(!host)continue;
 const b=document.createElement('button');b.type='button';b.className='v113-term-trigger';
 b.dataset.termHelp=key;b.textContent='?';b.setAttribute('aria-label',label);
 host.insertAdjacentElement('afterend',b);
}
document.addEventListener('click',event=>{
 const trigger=event.target.closest('[data-term-help]');
 if(trigger){event.preventDefault();open(trigger.dataset.termHelp,trigger);return;}
 if(!dialog.hidden&&!dialog.contains(event.target))close(false);
});
closeButton.addEventListener('click',()=>close(true));
document.addEventListener('keydown',event=>{
 if(event.key==='Escape'&&!dialog.hidden){event.preventDefault();close(true);}
});
root.CardiacTermsV113=Object.freeze({open,close,get openKey(){return dialog.hidden?null:
 Object.keys(terms).find(k=>terms[k].title===title.textContent)||null;}});
})(window);
