/*
 * v1.13 Patch 3 — single course state, original Guided remains authoritative.
 * Course unit selection never touches Timeline/heartState/Guided stage/answers.
 */
(function(root){
'use strict';
const units=Object.freeze([
{id:'unit-cardiac-cycle',title:'1. 심장주기 전체 흐름',
goal:'다섯 기계적 단계와 ECG 사건의 시간적 관계를 설명한다.',
core:'심장주기는 전기적 활성화에 뒤따르는 기계적 수축과 이완이 반복되는 과정입니다. 심방 수축, 등용적 수축, 심실 박출, 등용적 이완, 심실 충만을 구별하여 관찰하세요.',
nursing:'P파와 실제 심방 수축, QRS와 심실 압력 변화는 동일 시점의 사건이 아닙니다. 전기적 관찰과 맥박·혈압·관류는 따로 확인해야 합니다.',
caution:'학습 주제는 총 6개이지만 심장주기의 대표 기계적 단계는 5개입니다. 이 모델의 RR 초반과 후반 filling은 상대 용적 표현이 다릅니다.',
view:'mechanical'},
{id:'unit-conduction',title:'2. 전기전도 경로',
goal:'SA 결절부터 심실 전도계까지의 활성화 순서를 구분한다.',
core:'동방결절(SA)에서 시작된 흥분은 심방으로 퍼지고, 방실결절(AV)의 전달 이후 His–Purkinje 전도계를 통해 심실로 전달됩니다. 실제 파형과 전도 사건은 전기적 표시입니다.',
nursing:'P–QRS의 순서와 규칙성을 관찰하되 ECG만으로 수축력이나 관류의 적절성을 확정하지 않습니다.',
caution:'이 시뮬레이터는 동율동 학습용이며 방실차단이나 모든 부정맥을 생성하지 않습니다.',
view:'electrical'},
{id:'unit-ecg-timing',title:'3. ECG 파형과 시간 간격',
goal:'P·PR·QRS·ST·T 및 RR·QT·QTc의 개념과 한계를 구별한다.',
core:'P파는 심방 탈분극, QRS는 심실 탈분극, T파는 심실 재분극과 관련됩니다. PR·QRS·QT 등 표시값은 모델의 시간적 관계를 읽기 위한 교육용 지표입니다.',
nursing:'파형과 환자의 맥박·증상을 함께 해석해야 하며 QTc 모델값을 독립적인 환자 진단값으로 사용하면 안 됩니다.',
caution:'QTc는 심박수에 따라 보정한 근사 지표입니다. 이 앱의 표시값은 실제 환자의 처방·진단 판단에 쓰지 않습니다.',
view:'electrical'},
{id:'unit-mechanics',title:'4. 수축·판막·혈류',
goal:'등용적 단계와 박출 단계의 판막·상대 용적 변화를 구분한다.',
core:'등용적 수축·이완에서는 승모판과 대동맥판이 닫혀 상대 용적이 일정합니다. 대동맥판이 열리면 박출 단계로 진행하며 상대 용적이 감소합니다.',
nursing:'S1/S2는 기계적 판막 사건에 대응하는 심음 학습 단서이지만, 모델에서는 실제 청진 소리를 녹음해 들려주지 않습니다.',
caution:'전기적 사건과 판막 개폐 시점은 다릅니다. 두 판막 사건을 ECG의 한 점과 자동으로 같게 해석하지 않습니다.',
view:'mechanical'},
{id:'unit-wiggers',title:'5. Wiggers 통합 이해',
goal:'ECG·판막·상대 압력·상대 용적·심음 표지를 함께 읽는다.',
core:'Wiggers 도식은 같은 심장주기에 전기적 사건과 기계적 사건을 나란히 비교합니다. 곡선의 방향과 사건의 전후 관계부터 읽는 것이 핵심입니다.',
nursing:'압력·용적의 절대 수치보다 변화 양상과 실제 환자 관찰 결과를 종합하는 사고를 연습합니다.',
caution:'모델의 압력·용적은 상대 지표로 mmHg·mL·일회박출량·EF가 아닙니다. S1/S2는 사건 마커이며 실제 심음 자료가 아닙니다.',
view:'wiggers'},
{id:'unit-nursing',title:'6. 간호 사정과 연결',
goal:'HR 수치와 증상·의식·혈압·말초관류·호흡을 통합한다.',
core:'서맥·정상·빈맥 범위는 학습의 시작점일 뿐입니다. 같은 HR에서도 증상과 관류, 약물·기저질환, 측정 조건에 따라 임상적 의미가 달라집니다.',
nursing:'환자 상태를 먼저 사정하고 ECG와 활력징후를 비교하여 필요한 보고와 재평가를 결정합니다. 숫자만으로 치료 필요성을 단정하지 않습니다.',
caution:'30–180 bpm으로 조작하는 화면은 동율동 교육 엔진이며 병적 ECG나 개별 환자의 혈압·심박출량을 예측하지 않습니다.',
view:'electrical'}
].map(x=>Object.freeze(x)));
const ids=new Set(units.map(x=>x.id));
let unit=units[0].id,mode='guided';
const completed=new Set();let returnContext=null,ui=null;
const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
function textBlock(parent,title,value){
 const wrap=el('section','v113-reading-block'),h=el('h4','',title),p=el('p','',value);
 wrap.append(h,p);parent.append(wrap);
}
function mount(screen){
 screen.setAttribute('aria-label','6개 주제 심장 전기생리학 학습');
 screen.classList.add('v113-learning');
 screen.replaceChildren();
 const shell=el('div','v113-course-shell');
 const heading=el('h2','','심장 전기생리학 학습 · 6개 주제');
 const intro=el('p','v113-course-intro','6개 학습 주제와 기존 심장주기 5단계·개념 10문항은 서로 다릅니다. 단원을 둘러보는 것만으로 시뮬레이터 시간은 이동하지 않습니다.');
 const modes=el('div','v113-course-modes');
 modes.setAttribute('role','group');modes.setAttribute('aria-label','학습 방법');
 const guided=el('button','v113-action','안내형 학습'),free=el('button','v113-action','자유 탐색');
 for(const b of [guided,free])b.type='button';
 guided.addEventListener('click',()=>{mode='guided';render();});
 free.addEventListener('click',()=>{mode='free';render();});
 modes.append(guided,free);
 const progress=el('p','v113-progress');
 const back=el('button','v113-action v113-return','임상 문제로 돌아가기');
 back.type='button';back.hidden=true;
 back.addEventListener('click',()=>{if(returnContext&&root.CardiacMainTabs?.switchTo('clinical'))returnContext=null;render();});
 const layout=el('div','v113-course-layout'),list=el('nav','v113-unit-list'),article=el('article','v113-unit-reading');
 list.setAttribute('aria-label','학습 주제 선택');
 const guideHost=el('section','v113-guide-host');guideHost.id='v113LearningGuideHost';
 layout.append(list,article);
 shell.append(heading,intro,modes,progress,back,layout,guideHost);
 screen.append(shell);
 ui={screen,list,article,progress,guided,free,back,guideHost};
 render();
}
function render(){
 if(!ui)return;
 const current=units.find(x=>x.id===unit)||units[0];
 ui.guided.setAttribute('aria-pressed',String(mode==='guided'));
 ui.free.setAttribute('aria-pressed',String(mode==='free'));
 ui.guided.classList.toggle('v113-chosen',mode==='guided');
 ui.free.classList.toggle('v113-chosen',mode==='free');
 ui.progress.textContent='내가 완료 표시한 주제 '+completed.size+'/6 · 기존 개념 10문항의 제출 기록과 별개';
 ui.back.hidden=!returnContext;
 ui.list.replaceChildren();
 for(const item of units){
  const b=el('button','v113-unit-button',(completed.has(item.id)?'✓ 완료 · ':'')+item.title);
  b.type='button';b.setAttribute('aria-pressed',String(item.id===unit));
  if(item.id===unit)b.classList.add('v113-chosen');
  b.addEventListener('click',()=>selectUnit(item.id));
  ui.list.append(b);
 }
 const a=ui.article;a.replaceChildren();
 a.append(el('p','v113-eyebrow',mode==='guided'?'안내형 코스 · 단원을 순서대로 공부할 수 있어요':'자유 탐색 · 필요한 단원을 언제든 선택할 수 있어요'),
  el('h3','v113-unit-title',current.title));
 textBlock(a,'이 단원에서 배울 것',current.goal);
 textBlock(a,'핵심 기전',current.core);
 textBlock(a,'간호학적 의미',current.nursing);
 const warning=el('p','v113-model-caution','모형·해석 주의: '+current.caution);a.append(warning);
 const actions=el('div','v113-course-actions');
 const see=el('button','v113-action v113-primary','시뮬레이터에서 직접 관찰하기');
 see.type='button';see.addEventListener('click',()=>{
  if(root.CardiacMainTabs?.switchTo('simulator')){
   root.CardiacDashboard?.setView(current.view);
  }
 });
 const check=el('button','v113-action',completed.has(unit)?'✓ 완료 표시 취소':'이 단원 학습 완료 표시');
 check.type='button';check.addEventListener('click',()=>{
  if(completed.has(unit))completed.delete(unit);else completed.add(unit);
  render();
  ui.article.querySelector('.v113-course-actions button:nth-child(2)')?.focus();
 });
 actions.append(see,check);
 if(mode==='guided'){
  const idx=units.findIndex(x=>x.id===unit);
  const next=el('button','v113-action','다음 단원 →');next.type='button';next.disabled=idx>=5;
  next.addEventListener('click',()=>selectUnit(units[idx+1].id));
  actions.append(next);
 }
 a.append(actions);
 const details=el('details','v113-unit-details');
 details.append(el('summary','','관련 원문·도구·출처 확인'));
 const p=el('p','','기존 ECG, Mechanical, Wiggers와 학습 설명은 시뮬레이터 원본에서 확인합니다. 새 교육 문장은 원래 5단계 질문·정답을 복사하거나 변형하지 않습니다.');
 details.append(p);
 if(unit==='unit-cardiac-cycle'){
  const stages=el('p','','기존 심장주기 5단계: '+(root.CardiacGuidedContent?.stages||[]).map(s=>s.label).join(' → '));
  details.append(stages);
  const button=el('button','v113-action','5단계 심장주기 학습 시작 · 내용으로 이동');
  button.type='button';button.setAttribute('aria-controls','guidedV112Panel');
  button.addEventListener('click',()=>{
   // A second visit to the Guide is navigation, NOT a close/open toggle.
   if(!root.CardiacGuidedLearning?.open)
     document.getElementById('guidedV112Toggle')?.click();
   const title=document.getElementById('guidedV112Title');
   if(title){title.tabIndex=-1;title.focus();}
  });
  a.append(button);
 }
 a.append(details);
 // The ORIGINAL v1.12 Guide is mounted separately, never cloned.
 ui.guideHost.hidden=unit!=='unit-cardiac-cycle';
}
function selectUnit(id){if(!ids.has(id)||id===unit)return false;unit=id;render();
 const heading=ui?.article.querySelector('.v113-unit-title');
 if(heading){heading.tabIndex=-1;heading.focus();}
 return true;}
function openFromClinical(id,context){
 if(!ids.has(id))return false;
 unit=id;returnContext=context||{source:'clinical'};
 render();return !!root.CardiacMainTabs?.switchTo('learning');
}
root.CardiacCourseV113=Object.freeze({
 get ready(){return true;},mount,selectUnit,openFromClinical,
 get activeUnitId(){return unit;},get mode(){return mode;},
 get completedUnitIds(){return [...completed];},get returnContext(){return returnContext;},
 get guideHost(){return ui?.guideHost;},get unitIds(){return [...ids];}
});
})(window);
