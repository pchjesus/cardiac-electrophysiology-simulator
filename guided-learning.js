/*
 * v1.12 Patch 2 — user-initiated learning step/view/time controls.
 * Runs after dashboard-v111.js and preserves original DOM/event listeners.
 * Previous/next are study-only. Wiggers view and original Timeline seek
 * are invoked by separate, clearly labeled button clicks; no new clock.
 */
(function(root){
  'use strict';
  const dashboard=root.CardiacDashboard;
  const content=root.CardiacGuidedContent;
  const learning=root.CardiacLearning;
  const mech=root.CardiacMechanical,profile=root.CardiacWiggersProfile;
  const inspector=document.querySelector('.dashboard-inspector');
  const heading=inspector?.querySelector('.dashboard-inspector-heading');
  const clinical=inspector?.querySelector('.dashboard-clinical');
  const timeline=document.getElementById('timeSlider');
  if(!dashboard||!content||!learning?.getStageNarrative||!mech||!profile||
     !inspector||!heading||!clinical||!timeline)return;

  const el=(tag,className,text)=>{
    const x=document.createElement(tag);
    if(className)x.className=className;
    if(text!==undefined)x.textContent=text;
    return x;
  };
  const originalHeading=heading.firstChild;
  const toggle=el('button','guided-v112-trigger','5단계 학습');
  toggle.type='button';toggle.id='guidedV112Toggle';
  toggle.setAttribute('aria-expanded','false');
  toggle.setAttribute('aria-controls','guidedV112Panel');
  heading.appendChild(toggle);
  heading.classList.add('guided-v112-heading');

  const panel=el('section','guided-v112');
  panel.id='guidedV112Panel';
  panel.hidden=true;
  panel.setAttribute('aria-label','심장 주기 5단계 학습');
  const top=el('div','guided-v112-top');
  const counter=el('strong','guided-v112-counter');
  counter.id='guidedV112Counter';
  const label=el('label','guided-v112-select-label','학습 단계');
  const select=el('select','guided-v112-select');
  select.id='guidedV112Select';
  for(const [i,stage] of content.stages.entries()){
    const option=document.createElement('option');
    option.value=stage.id;option.textContent=(i+1)+'. '+stage.label;
    select.appendChild(option);
  }
  label.appendChild(select);
  top.append(counter,label);
  const title=el('h3','guided-v112-title');title.id='guidedV112Title';
  title.setAttribute('aria-live','polite');
  const current=el('p','guided-v112-current');current.id='guidedV112Live';
  const note=el('p','guided-v112-note','학습 단계 선택은 현재 재생 위치를 변경하지 않습니다.');
  const nav=el('div','guided-v112-navigation');
  nav.setAttribute('role','group');
  nav.setAttribute('aria-label','학습 단계 탐색');
  const prev=el('button','guided-v112-action','← 이전 단계');
  prev.id='guidedV112Previous';
  prev.type='button';
  const next=el('button','guided-v112-action','다음 단계 →');
  next.id='guidedV112Next';
  next.type='button';
  nav.append(prev,next);
  const observe=el('div','guided-v112-observe');
  observe.setAttribute('role','group');
  observe.setAttribute('aria-label','사용자가 직접 실행하는 관찰 동작');
  const view=el('button','guided-v112-action','Wiggers에서 보기');
  view.id='guidedV112ViewWiggers';
  view.type='button';
  view.setAttribute('aria-label','Wiggers 시각화로 전환 · 현재 시간 유지');
  const seek=el('button','guided-v112-action guided-v112-seek','이 단계 관찰 시점으로 이동');
  seek.id='guidedV112Seek';
  seek.type='button';
  seek.setAttribute('aria-describedby','guidedV112SeekNotice');
  observe.append(view,seek);
  const seekNotice=el('p','guided-v112-seek-notice',
    '관찰 시점으로 이동을 누르면 재생이 일시 정지되고, 기존 Timeline이 해당 단계로 이동합니다.');
  seekNotice.id='guidedV112SeekNotice';
  const summary=el('dl','guided-v112-summary');
  const fields=[
    ['ECG 전기 활동','electrical'],
    ['판막·압력의 관계','hemodynamics'],
    ['좌심실 상대 용적','volume'],
    ['간호학적 관찰','nursing']
  ];
  const nodes={};
  for(const [name,id] of fields){
    const dt=el('dt','',name),dd=el('dd','');
    dd.id='guidedV112'+id[0].toUpperCase()+id.slice(1);
    nodes[id]=dd;
    summary.append(dt,dd);
  }
  const model=el('p','guided-v112-model');model.id='guidedV112Model';
  const limits=el('p','guided-v112-limits');
  limits.id='guidedV112Limits';
  panel.append(top,title,current,note,nav,observe,seekNotice,summary,model,limits);
  clinical.before(panel);

  let open=false,selectedIndex=0,lastKey='';
  const trimSentence=value=>{
    const text=String(value||'').trim();
    const i=text.indexOf('다.');
    return i>=0?text.slice(0,i+2):text;
  };
  function renderSelected(){
    const stage=content.stages[selectedIndex];
    const data=learning.getStageNarrative(stage.id);
    if(!data)return;
    const obs=content.getObservation(stage.id,getActiveTiming(),mech,profile);
    select.value=stage.id;
    prev.disabled=selectedIndex===0;
    next.disabled=selectedIndex===content.stages.length-1;
    counter.textContent='학습 중인 단계 '+(selectedIndex+1)+'/5';
    title.textContent=stage.label;
    for(const key of Object.keys(nodes))nodes[key].textContent=trimSentence(data[key]);
    const filling=stage.id==='filling';
    model.textContent='모델 대표 관찰점 '+Math.round(obs.midpointMs)+' / '+
       Math.round(obs.rrMs)+' ms · 단계 선택만으로는 현재 위치가 이동하지 않음';
    limits.textContent=(filling?
       '주의: 여기서 후반은 시뮬레이터 RR의 후반 구간입니다. RR 초반에도 filling 단계가 있으나 모형 상대 용적은 0.88로 일정합니다. ':'')+
       '압력·용적은 교육용 상대 지표이며 mmHg, mL, EF 또는 심박출량을 뜻하지 않습니다.';
  }
  function sync(narrative,ready){
    if(!open)return;
    const live=narrative||learning.getInspectorNarrative();
    if(!live)return;
    const isReady=ready===undefined?dashboard.isReady:ready;
    const key=[isReady,live.phase,live.heartRate].join('|');
    if(lastKey===key)return;
    lastKey=key;
    current.textContent=isReady?'현재 시뮬레이션: Ready · 재생 전':
      '현재 시뮬레이션: '+live.title+
      (live.phase===content.stages[selectedIndex].id?
       ' · 학습 단계와 일치':' · 학습 중인 단계와 다름');
    renderSelected(); // HR-responsive midpoint; does not seek.
  }
  function setOpen(next){
    if(open===next)return;
    open=next;
    panel.hidden=!open;
    clinical.hidden=open;
    toggle.setAttribute('aria-expanded',String(open));
    toggle.textContent=open?'학습 닫기':'5단계 학습';
    originalHeading.textContent=open?'5단계 심장 주기 학습':'실시간 통합 해설';
    if(open){lastKey='';sync();}
    else {lastKey='';toggle.focus();}
  }
  toggle.addEventListener('click',()=>setOpen(!open));
  function chooseStage(index){
    if(index<0||index>=content.stages.length||index===selectedIndex)return;
    selectedIndex=index;
    lastKey='';
    sync();
    // Deliberately do not seek, change view or toggle playback here.
  }
  select.addEventListener('change',()=>{
    chooseStage(content.stages.findIndex(x=>x.id===select.value));
  });
  prev.addEventListener('click',()=>chooseStage(selectedIndex-1));
  next.addEventListener('click',()=>chooseStage(selectedIndex+1));
  view.addEventListener('click',()=>{
    if(!open)return;
    // Separate explicit user action; no Timeline or playback side effects.
    dashboard.setView('wiggers');
  });
  seek.addEventListener('click',()=>{
    if(!open)return;
    const chosen=content.stages[selectedIndex];
    const observation=content.getObservation(
      chosen.id,getActiveTiming(),mech,profile);
    const percent=100*observation.midpointMs/observation.rrMs;
    const step=Number(timeline.step)||0.1;
    const min=Number(timeline.min)||0;
    const max=Number(timeline.max)||100;
    // Match native slider step and clamp inside its supported range.
    const target=Math.max(min,Math.min(max,
      min+Math.round((percent-min)/step)*step));
    timeline.value=String(Number(target.toFixed(8)));
    timeline.dispatchEvent(new Event('input',{bubbles:true}));
    // The existing slider owns Pause/A/B seek and display synchronization.
    // No alternate model updater or time state is created.
    lastKey='';
    sync();
  });
  root.CardiacGuidedLearning=Object.freeze({
    sync,
    get open(){return open;},
    get selectedStageId(){return content.stages[selectedIndex].id;},
    get version(){return 'v1.12 Patch 2';}
  });
})(window);
