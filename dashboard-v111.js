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
  dashboard.id='dashboardV111';
  dashboard.dataset.density='compact';
  dashboard.setAttribute('aria-label','Integrated cardiac simulation learning dashboard');
  const commands=node('section','dashboard-commands card');
  commands.setAttribute('aria-label','Shared simulation controls');
  commands.appendChild(control);
  const presets=node('div','dashboard-presets');
  const presetLabel=node('span','dashboard-presets-label','학습 시나리오');
  presets.append(presetLabel,scenarios);
  const densityButton=node('button','dashboard-density-button','자료 목록 보기');
  densityButton.id='dashboardDensityBtn';
  densityButton.type='button';
  densityButton.setAttribute('aria-pressed','false');
  densityButton.setAttribute('aria-controls','dashboardResources');
  densityButton.setAttribute('aria-label','선택형 전도·ECG 사건·간호 원문 자료 목록 열기');
  presets.appendChild(densityButton);
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
  const focusButton=node('button','dashboard-focus-button','⤢ Wiggers 확대 보기');
  focusButton.type='button';focusButton.id='dashboardFocusBtn';
  focusButton.setAttribute('aria-pressed','false');
  focusButton.setAttribute('aria-label','Wiggers 그래프 확대 보기 전환');
  left.append(tabs,focusButton,stage);

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
  // Keep the original dynamic nodes intact; native disclosures only govern
  // whether the learner sees the longer explanations.
  const wrapDetails=(className,label,content)=>{
    const disclosure=node('details','dashboard-disclosure '+className);
    const summary=node('summary','dashboard-disclosure-summary');
    summary.textContent=label;
    disclosure.append(summary,content);
    return disclosure;
  };
  const ecgExplanation=$('ecgExplanation');
  const ecgDetails=wrapDetails('dashboard-ecg-details','ECG 구성요소 · 상세 설명',ecgExplanation);
  ecg.querySelector('.ecg-interpretation').after(ecgDetails);
  const phaseDetails=wrapDetails('dashboard-phase-details','전도 단계 · 전체 설명',phasePanel);
  const eventDetails=wrapDetails('dashboard-event-details','ECG Event · 세부 전도 정보',eventPanel);
  statuses.insertAdjacentHTML('beforeend',
    '<div><span>ECG 사건</span><strong id="dashboardEvent">Ready</strong></div>');
  // Relocate the SAME native long-form disclosures below the visual workspace.
  // Do not clone their original nodes, IDs, handlers, or source narratives.
  inspector.append(insHeading,statuses,clinical);
  const resources=node('details','dashboard-resources card');
  resources.id='dashboardResources';
  resources.setAttribute('aria-label','Additional cardiac education and source notes');
  const resourceHint=node('p','dashboard-resources-hint',
    '필요한 주제만 열어 읽으세요. ECG 파형(P·PR·QRS·ST·T) 설명은 ECG Monitor에서 직접 선택할 수 있습니다. 원문과 모델 한계는 아래 항목에 그대로 보존됩니다.');
  resources.append(node('summary','dashboard-resources-heading','자료 찾아보기 · 전도 단계 / ECG 사건 / 간호 원문'),
    resourceHint,phaseDetails,eventDetails,deepDive);
  workspace.append(left);
  // Left observation column shares one layout parent; a long right Inspector
  // cannot redistribute row height between ECG and the original heart SVG.
  // Move original nodes rather than cloning Canvas/SVG/handlers.
  const primary=node('section','dashboard-primary');
  primary.setAttribute('aria-label','ECG and synchronized cardiac visualization');
  primary.append(ecg,workspace);
  dashboard.append(commands,primary,inspector,measurements,resources);
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
      narrative.phase,$('phaseTitle').textContent,$('ecgEventIndicator').textContent].join('|');
    root.CardiacGuidedLearning?.sync(narrative,ready);
    if(key===latestKey)return;
    latestKey=key;
    $('dashboardElectrical').textContent=ready?'Ready':($('phaseTitle').textContent||'—');
    $('dashboardMechanical').textContent=ready?'Ready':narrative.title;
    $('dashboardEvent').textContent=ready?'Ready':($('ecgEventIndicator').textContent||'—');
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
  // A deliberate user selection of P, PR, QRS, ST or T reveals its
  // unchanged detailed explanation even while the rest remains compact.
  ecg.querySelectorAll('[data-ecg-component]').forEach(button=>{
    button.addEventListener('click',()=>{ecgDetails.open=true;});
  });
  // The top control opens a categorized index, not every long passage.
  // Native source disclosures keep their original content and independent state.
  function reflectResourceDensity(expanded){
    dashboard.dataset.density=expanded?'expanded':'compact';
    densityButton.textContent=expanded?'핵심 보기로 전환':'자료 목록 보기';
    densityButton.setAttribute('aria-pressed',String(expanded));
    densityButton.setAttribute('aria-expanded',String(expanded));
    densityButton.setAttribute('aria-label',expanded?
      '자료 목록을 접고 핵심 보기로 돌아가기':
      '선택형 전도·ECG 사건·간호 원문 자료 목록 열기');
  }
  densityButton.setAttribute('aria-expanded','false');
  densityButton.addEventListener('click',()=>{
    const expanded=!resources.open;
    resources.open=expanded;
    if(!expanded){
      // Compact means the long ECG/conduction/event explanations are folded.
      // Do not erase the independent six-part clinical source disclosure state.
      for(const disclosure of [ecgDetails,phaseDetails,eventDetails])
        disclosure.open=false;
    }
    reflectResourceDensity(expanded);
  });
  resources.addEventListener('toggle',()=>{
    // Keyboard/native summary clicks must not leave the header toggle stale.
    const expanded=resources.open;
    if(!expanded){
      for(const disclosure of [phaseDetails,eventDetails])
        disclosure.open=false;
    }
    reflectResourceDensity(expanded);
  });
  focusButton.addEventListener('click',()=>{
    const expanded=dashboard.dataset.wiggersFocus!=='true';
    dashboard.dataset.wiggersFocus=String(expanded);
    focusButton.setAttribute('aria-pressed',String(expanded));
    focusButton.textContent=expanded?'⤢ 분할 보기':'⤢ Wiggers 확대 보기';
  });
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
    get density(){return dashboard.dataset.density;},
    get view(){return view;},
    get isReady(){return isReady();}
  });
  setView('electrical');
})(window);
