/*
 * v1.13 Patch 5 — separate, fictional clinical case session. No writes to
 * heartState, native Timeline, Guided answers, or the authored case fixture.
 * Case content remains QA preview until independent medical review.
 */
(function(root){
'use strict';
const bank=root.CardiacClinicalCasesV113;
if(!bank)return;
const caseData=bank.first;
let screen=null,session=null,confirmAction=null,evidenceExpanded=false;
const el=(tag,cls,txt)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e;};
const button=(txt,handler,cls='v113-action')=>{const b=el('button',cls,txt);b.type='button';b.addEventListener('click',handler);return b;};
function focusCurrent(){
 const target=screen?.querySelector('.v113-question-prompt')||
              screen?.querySelector('.v113-review-card h3')||
              screen?.querySelector('.v113-case-card h3');
 if(target){target.tabIndex=-1;target.focus();}
}
function focusConfirm(){screen?.querySelector('.v113-confirm button')?.focus();}

function t(iso){return iso?iso.slice(11,16):'미확인';}
function referenceLinks(parent,ids){
 const wrap=el('div','v113-clinical-refs');
 for(const id of ids){
  const source=caseData.references.find(x=>x.id===id);if(!source)continue;
  const a=el('a','',source.title);a.href=source.url;a.target='_blank';a.rel='noopener noreferrer';wrap.append(a);
 }
 parent.append(wrap);
}
function visibleObservations(){
 const latest=session.questionIndex>=3;
 const o=el('section','v113-case-observations');
 o.setAttribute('aria-label','가상 환자 필수 관찰 및 참고 자료');
 o.append(el('h3','','환자 핵심 정보'),
   el('p','v113-case-complaint',caseData.baseline.context));
 if(latest)o.append(el('p','v113-case-followup',caseData.reassessment.context));
 o.append(el('p','v113-clinical-time',
   (latest?'재평가 ':'초기 사정 ')+t(latest?caseData.reassessment.at:caseData.baseline.at)+' · 가상 환자'));
 const vitals=latest?caseData.reassessment.measurements:caseData.baseline.measurements;
 const grid=el('div','v113-clinical-vitals');
 for(const v of vitals.filter(v=>v.label==='심박수'||v.label==='혈압')){
  const card=el('div','v113-vital');
  card.append(el('span','',v.label),el('strong','',String(v.value)+' '+v.unit),
    el('small','','측정 '+t(v.observedAt)));
  grid.append(card);
 }
 o.append(grid);
 if(latest)o.append(el('p','v113-clinical-hint',
   '초기 심박수 '+caseData.baseline.measurements[0].value+' /min · 초기 혈압 '+
   caseData.baseline.measurements[1].value+' mmHg · '+t(caseData.baseline.at)));
 const details=el('details','v113-case-evidence');
 details.open=evidenceExpanded;
 details.append(el('summary','v113-evidence-summary','심전도·검사 결과·추가 활력징후 확인'),
   el('p','v113-clinical-hint','판단 전에 제공된 자료를 확인하세요. 결과 대기·미시행은 정상 결과가 아닙니다.'));
 const extras=caseData.baseline.measurements.filter(v=>v.label!=='심박수'&&v.label!=='혈압');
 if(extras.length){
  const div=el('div','v113-extra-vitals');
  for(const v of extras){
   const p=el('p','',v.label+' '+v.value+' '+v.unit+' · '+t(v.observedAt));
   div.append(p);
  }
  details.append(div);
 }
 const ecg=el('section','v113-evidence-block');
 ecg.append(el('h4','','별도 심전도(ECG) 관찰 · '+t(caseData.ecg.recordedAt)),
  el('p','',caseData.ecg.text),
  el('p','v113-model-caution',caseData.ecg.limitation));
 details.append(ecg);
 const lab=el('section','v113-evidence-block');
 lab.append(el('h4','','혈액검사(Lab) · 결과 확인 상태'));
 for(const v of caseData.labs){
  const line=el('div','v113-lab');
  if(session.questionIndex<v.availableFromPhase){
   line.append(el('strong','',v.name),el('span','','결과 확인 전 · 채혈 '+t(v.collectedAt)),
    el('small','','현재 단계에서는 결과가 제공되지 않습니다.'));
  }else{
   const value=v.status==='known'?v.value+' '+v.unit:
     v.status==='pending'?'결과 대기 중':'미시행';
   line.append(el('strong','',v.name),el('span','',value),
    el('small','','검체 '+t(v.collectedAt)+' · 결과 '+(v.availableAt?t(v.availableAt):'미확인')),
    el('small','','해당 검사실 참고: '+v.range),el('p','',v.note));
  }
  lab.append(line);
 }
 details.append(lab);
 details.addEventListener('toggle',()=>{if(details.isConnected)evidenceExpanded=details.open;});
 o.append(details);
 return o;
}
function start(){
 session={caseId:caseData.id,questionIndex:0,answers:Object.create(null),status:'active'};
 confirmAction=null;
 evidenceExpanded=root.matchMedia('(min-width:1000px)').matches;
 render();focusCurrent();
}
function restart(){
 if(!session)return;
 confirmAction='restart';render();focusConfirm();
}
function finish(){
 if(!session)return;
 confirmAction='exit';render();focusConfirm();
}
function confirm(){
 if(confirmAction==='restart')start();
 else if(confirmAction==='exit'){session=null;confirmAction=null;render();focusCurrent();}
}
function selectAnswer(q,id){
 if(!session||confirmAction||session.answers[q.id]?.submitted)return;
 session.answers[q.id]={choiceId:id,submitted:false};
}
function submit(){
 if(!session||confirmAction)return;
 const q=caseData.questions[session.questionIndex],ans=session.answers[q.id];
 if(!ans||ans.submitted)return;
 ans.submitted=true;render();
 screen.querySelector('#v113ClinicalFeedback')?.focus();
}
function advance(){
 if(!session||confirmAction)return;
 const q=caseData.questions[session.questionIndex];
 if(!session.answers[q.id]?.submitted)return;
 if(session.questionIndex===caseData.questions.length-1)session.status='completed';
 else session.questionIndex+=1;
 render();focusCurrent();
}
function openStudy(unitId){
 root.CardiacCourseV113?.openFromClinical(unitId,{source:'clinical',caseId:caseData.id,
 questionId:session?.status==='completed'?'review':caseData.questions[session?.questionIndex]?.id});
}
function reviewCard(q,index){
 const answer=session.answers[q.id],chosen=q.choices.find(c=>c.id===answer?.choiceId);
 const correct=q.choices.find(c=>c.id===q.correctChoiceId);
 const ok=chosen?.id===correct?.id;
 const c=el('section','v113-review-card');
 c.append(el('h3','',(index+1)+'. '+q.prompt),
   el('p','v113-review-status',ok?'권장 답안과 일치':'추가 복습 필요'),
   el('p','','내 선택: '+(chosen?.text||'미응답')),
   el('p','','권장 답안: '+(correct?.text||'답안 자료 오류')),
   el('p','','해설: '+(chosen?.feedback||'미응답')+' '+q.rationale));
 referenceLinks(c,q.referenceIds);
 const actions=el('div','v113-course-actions');
 for(const id of q.relatedUnitIds)actions.append(button('관련 학습: '+(root.CardiacCourseV113?.getUnitTitle(id)||id),()=>openStudy(id)));
 c.append(actions);
 return c;
}
function render(){
 if(!screen)return;
 screen.replaceChildren();
 const wrap=el('div','v113-clinical-shell');
 wrap.append(el('h2','','③ 임상 적용 · 가상 환자 사례'));
 const concept=button('간호 사정 개념 알아보기',()=>{},'v113-concept-trigger');
 concept.dataset.conceptHelp='clinical';
 wrap.append(concept);
 wrap.append(el('p','v113-model-caution',
  '개발 검증용: 의료·간호 전문가의 독립 콘텐츠 검토 전인 교육용 가상 사례입니다. 실제 환자 진단·치료 지침으로 사용하지 마세요. 현재 심장 시뮬레이터의 실시간 심전도(ECG)나 혈역학과 연동하지 않습니다.'));
 if(!session){
  const cat=el('div','v113-case-card');
  cat.append(el('h3','',caseData.title),el('p','',caseData.summary),
   el('p','v113-clinical-hint','구성: 환자 사정 → 임상 판단 → 간호 행동 → 재평가 · 총 4문항'),
   button('가상 사례 시작',start,'v113-action v113-primary'));
  wrap.append(cat);screen.append(wrap);return;
 }
 wrap.append(el('p','v113-progress',session.status==='completed'?'4/4단계 · 결과 복습':
  '임상 판단 '+(session.questionIndex+1)+'/'+caseData.questions.length+'단계 · 선택한 답안과 공개된 자료는 탭 전환 후에도 유지됩니다.'));
 const nav=el('div','v113-course-actions');
 nav.append(button('같은 사례 다시 풀기',restart),button('사례 종료 · 목록으로',finish));
 wrap.append(nav);
 if(confirmAction){
  const warning=el('div','v113-confirm');
  warning.setAttribute('role','group');
  warning.setAttribute('aria-label','사례 기록 초기화 확인');
  warning.append(el('p','',confirmAction==='restart'?
    '이 사례의 답안과 진도를 초기화할까요? 시뮬레이터와 기존 10문항은 보존됩니다.':
    '현재 사례의 답안과 진도를 삭제하고 목록으로 돌아갈까요?'),
    button('확인 · 기록 초기화',confirm,'v113-action v113-primary'),
    button('취소',()=>{
     const action=confirmAction;confirmAction=null;render();
     const buttons=[...screen.querySelectorAll('.v113-course-actions button')];
     buttons[action==='restart'?0:1]?.focus();
    }));
  wrap.append(warning);
  screen.append(wrap);
  // Confirmation owns this step until Cancel/Confirm; don't expose an
  // interactive quiz or review beneath the destructive-action question.
  return;
 }
 if(session.status==='completed'){
  const summary=el('section','v113-case-card');
  const correct=caseData.questions.filter(q=>session.answers[q.id]?.choiceId===q.correctChoiceId).length;
  summary.append(el('h3','','결과 · 학습용 판단 복습'),
   el('p','','권장 답안과 일치 '+correct+'/'+caseData.questions.length+
       '문항. 이는 학습용 확인이며 임상 역량 인증 점수가 아닙니다.'));
  wrap.append(summary);
  const wrong=caseData.questions.map((q,i)=>({q,i})).filter(x=>session.answers[x.q.id]?.choiceId!==x.q.correctChoiceId);
  const right=caseData.questions.map((q,i)=>({q,i})).filter(x=>session.answers[x.q.id]?.choiceId===x.q.correctChoiceId);
  for(const {q,i} of [...wrong,...right])wrap.append(reviewCard(q,i));
  screen.append(wrap);return;
 }
 const stageLayout=el('div','v113-case-stage-layout');
 stageLayout.append(visibleObservations());
 const q=caseData.questions[session.questionIndex];
 const article=el('section','v113-case-card'),answered=session.answers[q.id];
 article.append(el('h3','','학습 판단 · '+(session.questionIndex+1)+'단계'),
   el('p','v113-question-prompt',q.prompt));
 const group=el('fieldset','v113-choices'),legend=el('legend','','가장 적절한 선택지 한 가지');
 group.append(legend);
 for(const choice of q.choices){
  const label=el('label','v113-choice'),input=el('input');
  input.type='radio';input.name='v113-clinical-choice';input.value=choice.id;
  input.checked=answered?.choiceId===choice.id;input.disabled=!!answered?.submitted;
  input.addEventListener('change',()=>{selectAnswer(q,choice.id);});
  label.append(input,el('span','',choice.text));group.append(label);
 }
 article.append(group);
 if(!answered?.submitted){
  const submitButton=button('선택한 답안 제출',()=>{
   // Capture selected radio immediately, even if a screenreader/browser
   // suppresses the expected change event.
   const chosen=group.querySelector('input:checked');
   if(chosen)selectAnswer(q,chosen.value);
   submit();
  },'v113-action v113-primary');
  submitButton.disabled=!answered?.choiceId;
  group.addEventListener('change',()=>{
   submitButton.disabled=!group.querySelector('input:checked');
  });
  article.append(submitButton);
 }else{
  const ch=q.choices.find(c=>c.id===answered.choiceId);
  const feedback=el('section','v113-feedback');
  feedback.id='v113ClinicalFeedback';feedback.tabIndex=-1;
  feedback.setAttribute('role','status');
  feedback.append(el('h4','',answered.choiceId===q.correctChoiceId?'권장 답안과 일치':'추가 복습 필요'),
   el('p','',ch?.feedback||'답안을 확인하세요'),el('p','',q.rationale));
  referenceLinks(feedback,q.referenceIds);
  const actions=el('div','v113-course-actions');
  for(const id of q.relatedUnitIds)actions.append(button('관련 학습: '+(root.CardiacCourseV113?.getUnitTitle(id)||id),()=>openStudy(id)));
  actions.append(button(session.questionIndex===3?'결과·복습 보기':'다음 단계',advance,'v113-action v113-primary'));
  feedback.append(actions);article.append(feedback);
 }
 stageLayout.append(article);wrap.append(stageLayout);screen.append(wrap);
}
function mount(target){
 screen=target;screen.classList.add('v113-clinical');screen.setAttribute('aria-label','가상 환자 간호 판단 교육');
 // Read-only disclosure follows responsive space, not simulation time.
 const desktop=root.matchMedia('(min-width:1000px)');
 desktop.addEventListener('change',event=>{
  evidenceExpanded=event.matches;
  const current=screen.querySelector('.v113-case-evidence');
  if(current)current.open=evidenceExpanded;
 });
 render();
}
root.CardiacClinicalV113=Object.freeze({
 mount,get publicReady(){return caseData.status==='clinical-reviewed'&&
   caseData.review?.releaseApproved===true&&Boolean(caseData.review.reviewedBy)&&
   Boolean(caseData.review.reviewedAt);},
 get sessionSnapshot(){if(!session)return null;
  return {caseId:session.caseId,index:session.questionIndex,status:session.status,
   answers:Object.fromEntries(Object.entries(session.answers).map(([k,v])=>[k,{...v}]))};},
 get caseReviewStatus(){return caseData.status;},
 restart,exit:finish
});
})(window);
