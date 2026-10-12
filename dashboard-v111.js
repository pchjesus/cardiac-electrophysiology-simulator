/*
 * Cardiac Electrophysiology Simulator v1.11 — dashboard presentation adapter.
 * DOM relocation runs AFTER v1.10 modules initialize; moves original elements
 * (not clones), preserving event listeners, public IDs and reference objects.
 * Rendering is read-only from the original A/B simulation and Wiggers profile.
 * No timers, no requestAnimationFrame, no new physiological state.
 */
(function(root){
  'use strict';
  const $=id=>document.getElementById(id);
  const app=document.querySelector('.app'),main=document.querySelector('.main-container');
  const ecg=document.querySelector('.ecg-panel');
  const control=document.querySelector('.embedded-control-panel');
  const heart=document.querySelector('.heart-panel');
  const tabs=document.querySelector('.heart-mode-switch');
  const wiggers=document.querySelector('.wiggers-shell');
  const wiggersDetails=$('wiggersDetails');
  const measurements=document.querySelector('.measurements-panel');
  const eventPanel=document.querySelector('.event-panel');
  const phasePanel=document.querySelector('.phase-panel');
  const deepDive=$('wiggersDeepDive');
  const scenarios=document.querySelector('.learning-preset-row');
  const oldVisual=document.querySelector('.visual-grid');
  const oldInfo=document.querySelector('.info-grid');
  if(!app||!main||!ecg||!control||!heart||!tabs||!wiggers||!wiggersDetails||
     !measurements||!eventPanel||!phasePanel||!deepDive||!scenarios||
     !oldVisual||!oldInfo||!root.CardiacWiggersProfile||!root.CardiacLearning||
     !root.CardiacMechanical)return;
  const node=(tag,cls,html)=>{
    const x=document.createElement(tag);if(cls)x.className=cls;
    if(html!==undefined)x.innerHTML=html;
    return x;
  };
  const dashboard=node('div','dashboard-v111');
  dashboard.setAttribute('aria-label','Integrated cardiac simulation learning dashboard');
  const commands=node('section','dashboard-commands card');
  commands.setAttribute('aria-label','Shared simulation controls');
  commands.appendChild(control);
  const presets=node('div','dashboard-presets');
  const presetLabel=node('span','dashboard-presets-label','학습 시나리오');
  presets.append(presetLabel,scenarios);
  commands.appendChild(presets);

  const workspace=node('section','dashboard-workspace');
  workspace.setAttribute('aria-label','Synchronized cardiac visualization and study');
  const left=node('section','dashboard-visual card');
  left.setAttribute('aria-label','Selected cardiac visualization');
  const stage=node('div','dashboard-stage');
  const wiggersButton=node('button','dashboard-wiggers-button','Wiggers');
  wiggersButton.type='button';
  wiggersButton.id='dashboardWiggersBtn';
  wiggersButton.setAttribute('aria-pressed','false');
  wiggersButton.setAttribute('aria-controls','wiggersDetails');
  const electrical=$('electricalModeBtn'),mechanical=$('mechanicalModeBtn');
  tabs.setAttribute('role','group');
  tabs.setAttribute('aria-label','Visualization view: Electrical, Mechanical, or Wiggers');
  tabs.appendChild(wiggersButton);
  stage.append(heart,wiggers);
  left.append(tabs,stage);

  const inspector=node('aside','dashboard-inspector card');
  inspector.setAttribute('aria-label','Live physiological and nursing explanation');
  const insHeading=node('h2','dashboard-inspector-heading','실시간 통합 해설');
  const statuses=node('div','dashboard-statuses');
  statuses.innerHTML=
    '<div><span>전기적 단계</span><strong id="dashboardElectrical">Ready</strong></div>'+
    '<div><span>기계적 단계</span><strong id="dashboardMechanical">Ready</strong></div>';
  const clinical=node('section','dashboard-clinical');
  clinical.innerHTML=
    '<h3>생리학적 변화</h3><p id="dashboardPhysiology">Play 또는 Timeline을 움직이면 현재 심장 주기를 설명합니다.</p>'+
    '<h3>간호학적 관찰</h3><p id="dashboardNursing">맥박·혈압·증상·관류를 함께 사정하는 관점으로 이해합니다.</p>'+
    '<p class="dashboard-caution">교육용 상대 지표 · 실제 혈압·박출량·EF·심박출량 예측 불가</p>';
  inspector.append(insHeading,statuses,phasePanel,clinical,eventPanel,deepDive);
  workspace.append(left,inspector);
  dashboard.append(commands,ecg,workspace,measurements);
  main.insertBefore(dashboard,oldVisual);
  oldVisual.remove();oldInfo.remove();
  app.classList.add('dashboard-active');

  let view='electrical';
  let latestKey=null;
  const buttons={electrical,mechanical,wiggers:wiggersButton};
  const isReady=()=>heartState.currentStep===-1 &&
    heartState.physiologicalTime===0 && heartState.visualizationTime===0 &&
    !heartState.playing;
  function brief(value){
    const text=String(value||'').trim();
    // Preserve source clinical wording: show the first complete sentence,
    // keep the full exact material in the native optional deep-dive.
    const idx=text.indexOf('다.');
    return idx>=0 ? text.slice(0,idx+2) : text;
  }
  function sync(){
    const ready=isReady();
    const narrative=root.CardiacLearning.getInspectorNarrative?.();
    if(!narrative)return;
    const key=[view,ready,heartRate,heartState.currentStep,
      narrative.phase,$('phaseTitle').textContent].join('|');
    if(key===latestKey)return;
    latestKey=key;
    $('dashboardElectrical').textContent=ready?'Ready':($('phaseTitle').textContent||'—');
    $('dashboardMechanical').textContent=ready?'Ready':narrative.title;
    $('dashboardPhysiology').textContent=ready ?
      '재생하거나 Timeline을 이동하면 ECG·압력·판막·용적의 관계가 표시됩니다.' :
      brief(narrative.hemodynamics);
    $('dashboardNursing').textContent=ready ?
      '심박수만으로 환자의 혈역학적 안정성을 판단하지 않습니다.' :
      brief(narrative.nursing);
  }
  function setView(next,{focus=false}={}){
    if(!buttons[next])return;
    const before=view;
    view=next;
    stage.dataset.view=next;
    dashboard.dataset.view=next;
    // The native details remains the source of truth for Wiggers profile
    // visibility. Closing it offscreen avoids unnecessary SVG frame work.
    if(next==='wiggers' && !wiggersDetails.open)wiggersDetails.open=true;
    else if(next!=='wiggers' && wiggersDetails.open)wiggersDetails.open=false;
    for(const [id,button] of Object.entries(buttons)){
      const chosen=id===next;
      button.classList.toggle('mode-active',chosen);
      button.setAttribute('aria-pressed',String(chosen));
    }
    if(next==='wiggers'){
      root.CardiacWiggersView?.sync();
      root.CardiacLearning?.sync();
    }
    latestKey=null;sync();
    if(focus)buttons[next].focus();
    if(before!==next){
      workspace.setAttribute('data-active-visualization',next);
    }
  }
  electrical.addEventListener('click',()=>setView('electrical'));
  mechanical.addEventListener('click',()=>setView('mechanical'));
  wiggersButton.addEventListener('click',()=>setView('wiggers'));
  tabs.addEventListener('keydown',event=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    const order=['electrical','mechanical','wiggers'];
    const current=order.indexOf(view);
    const next=event.key==='Home'?0:event.key==='End'?2:
      (current+(event.key==='ArrowRight'?1:2))%3;
    event.preventDefault();
    // Reuse native mode control for Electrical/Mechanical, so it retains
    // its own UI state and pure physiological state updates.
    buttons[order[next]].click();buttons[order[next]].focus();
  });
  wiggersDetails.addEventListener('toggle',()=>{
    // Only respond to user-initiated expansion if the view is otherwise
    // hidden; do not force a tab change when dashboard itself closes it.
    if(wiggersDetails.open && view!=='wiggers')setView('wiggers');
  });
  root.CardiacDashboard=Object.freeze({
    sync,
    setView,
    get view(){return view;},
    get isReady(){return isReady();}
  });
  setView('electrical');
})(window);
