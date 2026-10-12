/*
 * v1.12 Patch 1 — optional inline learning inspector.
 * Runs after dashboard-v111.js and preserves original DOM/event listeners.
 * Never seeks, pauses, selects Wiggers, changes HR, or starts another clock.
 * Patch 2 will own explicit user-invoked navigation / viewing / seek.
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
  if(!dashboard||!content||!learning?.getStageNarrative||!mech||!profile||
     !inspector||!heading||!clinical)return;

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
  panel.append(top,title,current,note,summary,model,limits);
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
    counter.textContent='학습 중인 단계 '+(selectedIndex+1)+'/5';
    title.textContent=stage.label;
    for(const key of Object.keys(nodes))nodes[key].textContent=trimSentence(data[key]);
    const filling=stage.id==='filling';
    model.textContent='모델 대표 관찰점 '+Math.round(obs.midpointMs)+' / '+
       Math.round(obs.rrMs)+' ms · 현재 위치는 이동하지 않음';
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
  select.addEventListener('change',()=>{
    const index=content.stages.findIndex(x=>x.id===select.value);
    if(index<0)return;
    selectedIndex=index;
    lastKey='';sync();
  });
  root.CardiacGuidedLearning=Object.freeze({
    sync,
    get open(){return open;},
    get selectedStageId(){return content.stages[selectedIndex].id;},
    get version(){return 'v1.12 Patch 1';}
  });
})(window);
