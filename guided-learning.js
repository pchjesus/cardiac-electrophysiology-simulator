/*
 * v1.12 Patch 4 — novice-first progressive learning: essentials, nursing links,
 * optional full-source additional learning. Preserves question and A/B isolation.
 * Runs after dashboard-v111.js and preserves original DOM/event listeners.
 * Learner-initiated stage navigation uses native Timeline Pause/Seek once.
 * Reading stays fixed during live playback; no additional clock.
 */
(function(root){
  'use strict';
  const dashboard=root.CardiacDashboard;
  const content=root.CardiacGuidedContent;
  const learning=root.CardiacLearning;
  const questions=root.CardiacGuidedQuestions;
  const mech=root.CardiacMechanical,profile=root.CardiacWiggersProfile;
  const inspector=document.querySelector('.dashboard-inspector');
  const heading=inspector?.querySelector('.dashboard-inspector-heading');
  const clinical=inspector?.querySelector('.dashboard-clinical');
  const timeline=document.getElementById('timeSlider');
  if(!dashboard||!content||!questions||!learning?.getStageNarrative||!mech||!profile||
     !inspector||!heading||!clinical||!timeline)return;

  const el=(tag,className,text)=>{
    const x=document.createElement(tag);
    if(className)x.className=className;
    if(text!==undefined)x.textContent=text;
    return x;
  };
  const originalHeading=heading.firstChild;
  const toggle=el('button','guided-v112-trigger','5단계 학습 시작');
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
  const note=el('p','guided-v112-note','학습 모드에서 이전·다음 단계를 누르면 재생을 멈추고 해당 관찰 시점으로 이동합니다.');
  const levelLine=el('div','guided-v112-level-row');
  const levelLabel=el('label','guided-v112-level-label','학습 수준');
  const levelSelect=el('select','guided-v112-level-select');
  levelSelect.id='guidedV112Level';
  const learningLevels=Object.freeze(['basic','intermediate','advanced']);
  for(const [value,label] of [['basic','1. 기초 이해'],['intermediate','2. 간호 연결'],['advanced','3. 추가학습']]){
    const item=el('option','',label);
    item.value=value;
    levelSelect.appendChild(item);
  }
  levelLabel.appendChild(levelSelect);
  const levelHint=el('p','guided-v112-level-hint',
    '먼저 심장주기 핵심을 익혀요. 다음 수준에서 간호 관찰을 연결합니다.');
  levelHint.id='guidedV112LevelHint';
  const promote=el('button','guided-v112-action guided-v112-promote','다음 수준: 간호 연결 →');
  promote.type='button';
  promote.id='guidedV112Promote';
  levelLine.append(levelLabel,levelHint);
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
  const seek=el('button','guided-v112-action guided-v112-seek','이 단계 다시 관찰');
  seek.id='guidedV112Seek';
  seek.type='button';
  seek.setAttribute('aria-describedby','guidedV112SeekNotice');
  observe.append(view,seek);
  const seekNotice=el('p','guided-v112-seek-notice',
    '재관찰 버튼을 누르면 재생이 일시 정지되고, 기존 Timeline이 현재 학습 단계의 관찰점으로 이동합니다.');
  seekNotice.id='guidedV112SeekNotice';
  // Optional controls remain original nodes; prioritize the reading path.
  const tools=el('details','guided-v112-tools');
  tools.id='guidedV112Tools';
  tools.append(el('summary','guided-v112-tools-heading','추가 도구 · 학습 수준 / Wiggers / 재관찰'),
    levelLine,observe,seekNotice,note);
  const gist=el('p','guided-v112-gist');
  gist.id='guidedV112Gist';
  const gistLabel=el('strong','','한 문장으로 이해하기 · ');
  const gistText=el('span','');
  gist.append(gistLabel,gistText);
  const noviceText=Object.freeze({
    atrial_systole:'P파가 나타난 뒤 심방이 수축해 심실에 혈액을 더 채워요.',
    isovolumetric_contraction:'심실에 힘이 생기고 압력이 올라가지만 두 판막은 닫혀 있어요.',
    ejection:'대동맥판이 열리고 심실에서 혈액이 밖으로 나가요.',
    isovolumetric_relaxation:'심실이 이완하며 압력이 떨어지고 두 판막은 잠시 닫혀 있어요.',
    filling:'모델 RR 후반에는 승모판이 열리고 심실의 상대 용적이 증가해요.'
  });
  const summary=el('dl','guided-v112-summary');
  const fields=[
    ['ECG 전기 활동','electrical'],
    ['판막·압력의 관계','hemodynamics'],
    ['좌심실 상대 용적','volume'],
    ['간호학적 관찰','nursing']
  ];
  const nodes={},sections={};
  for(const [name,id] of fields){
    const dt=el('dt','',name),dd=el('dd','');
    dd.id='guidedV112'+id[0].toUpperCase()+id.slice(1);
    nodes[id]=dd;
    sections[id]=[dt,dd];
    summary.append(dt,dd);
  }
  const model=el('p','guided-v112-model');model.id='guidedV112Model';
  const limits=el('p','guided-v112-limits');
  limits.id='guidedV112Limits';
  // Detailed wording is the exact original PHASES/RATE source, never
  // shortened or independently re-authored.
  const advanced=el('details','guided-v112-advanced');
  advanced.id='guidedV112Advanced';
  advanced.hidden=true;
  advanced.appendChild(el('summary','','추가학습: 의학·간호 원문과 모델 한계 펼치기'));
  const advancedList=el('dl','guided-v112-full-list');
  const longFields=[
    ['ECG·전기 활동','electrical'],['판막·혈역학','hemodynamics'],
    ['상대 용적','volume'],['간호 관찰','nursing'],
    ['현재 모델 한계','caution'],['HR별 비교·주의','comparison']
  ];
  const longNodes={};
  for(const [name,key] of longFields){
    const dt=el('dt','',name),dd=el('dd','');
    dd.id='guidedV112Full'+key[0].toUpperCase()+key.slice(1);
    longNodes[key]=dd;
    advancedList.append(dt,dd);
  }
  advanced.appendChild(advancedList);

  // Answers live only in this in-page study session. No storage,
  // clinical score, or modification of simulation/Timeline state.
  const answers=Object.create(null);
  let detailLevel='basic';
  const quiz=el('details','guided-v112-quiz');
  quiz.id='guidedV112Quiz';
  quiz.appendChild(el('summary','','이해도 확인 (선택)'));
  const quizIntro=el('p','guided-v112-quiz-intro',
    '각 문항은 학습용 개념 확인입니다. 정답·해설은 답을 제출한 뒤 표시됩니다.');
  quiz.appendChild(quizIntro);
  const quizCards={};
  for(const level of questions.levels){
    const card=el('section','guided-v112-question');
    card.id=level==='basic'?'guidedV112BasicQuestion':'guidedV112AdvancedQuestion';
    const heading=el('h4','guided-v112-question-heading',
      level==='basic'?'초급 확인':'심화 확인');
    const fieldset=el('fieldset','guided-v112-choices');
    const legend=el('legend','guided-v112-prompt');
    legend.id='guidedV112Prompt'+(level==='basic'?'Basic':'Advanced');
    fieldset.appendChild(legend);
    const choices=[];
    for(let i=0;i<3;i++){
      const label=el('label','guided-v112-option');
      const input=document.createElement('input');
      input.type='radio';
      input.name='guided-v112-'+level;
      input.value=String(i);
      input.setAttribute('aria-label','보기 '+('ABC'[i]));
      const wording=el('span','');
      label.append(input,wording);
      fieldset.appendChild(label);
      choices.push({input,wording});
    }
    const actions=el('div','guided-v112-question-actions');
    const submit=el('button','guided-v112-action','정답 확인');
    submit.type='button';
    submit.disabled=true;
    submit.id='guidedV112Submit'+(level==='basic'?'Basic':'Advanced');
    const retry=el('button','guided-v112-action','다시 풀기');
    retry.type='button';
    retry.hidden=true;
    retry.id='guidedV112Retry'+(level==='basic'?'Basic':'Advanced');
    actions.append(submit,retry);
    const feedback=el('p','guided-v112-feedback');
    feedback.id='guidedV112Feedback'+(level==='basic'?'Basic':'Advanced');
    feedback.setAttribute('role','status');
    feedback.hidden=true;
    card.append(heading,fieldset,actions,feedback);
    quiz.appendChild(card);
    quizCards[level]={card,legend,choices,submit,retry,feedback};
  }
  panel.append(top,title,current,gist,nav,summary,promote,tools,
    model,limits,advanced,quiz);

  clinical.before(panel);

  let open=false,selectedIndex=0,lastKey='',lastRenderedSelection='',hasStarted=false;
  const trimSentence=value=>{
    const text=String(value||'').trim();
    const i=text.indexOf('다.');
    return i>=0?text.slice(0,i+2):text;
  };
  const currentStage=()=>content.stages[selectedIndex].id;
  const questionFor=level=>questions.get(currentStage(),level);
  function renderQuestion(level){
    const ui=quizCards[level];
    const item=questionFor(level);
    if(!item)throw new Error('Missing v1.12 educational question: '+currentStage());
    const saved=answers[item.id]||{choice:null,submitted:false};
    ui.card.hidden=level==='advanced'&&detailLevel!=='advanced';
    ui.legend.textContent=item.prompt;
    for(let i=0;i<ui.choices.length;i++){
      const {input,wording}=ui.choices[i];
      wording.textContent=item.options[i];
      input.checked=saved.choice===i;
      input.disabled=saved.submitted;
    }
    ui.submit.disabled=saved.choice===null||saved.submitted;
    ui.retry.hidden=!saved.submitted;
    ui.feedback.hidden=!saved.submitted;
    if(saved.submitted){
      const correct=saved.choice===item.correctIndex;
      ui.feedback.dataset.result=correct?'correct':'incorrect';
      ui.feedback.textContent=(correct?'정답입니다. ':
        '다시 확인해보세요. '+item.wrong[saved.choice]+' 정답은 '+
        item.options[item.correctIndex]+'. ')+item.explanation;
    }else{
      ui.feedback.textContent='';
      delete ui.feedback.dataset.result;
    }
  }
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
    gistText.textContent=noviceText[stage.id];
    for(const [id,pair] of Object.entries(sections)){
      const visible=id!=='nursing'||detailLevel!=='basic';
      for(const node of pair)node.hidden=!visible;
    }
    levelSelect.value=detailLevel;
    const currentLevel=learningLevels.indexOf(detailLevel);
    levelHint.textContent=[
      '1단계 · P파/QRS, 판막, 혈액 흐름의 핵심부터 살펴봐요.',
      '2단계 · ECG와 혈액 흐름을 간호 관찰에 연결해요.',
      '추가학습 · 필요할 때 원문 설명, 모델 한계와 응용 문제를 살펴봐요.'
    ][currentLevel];
    promote.hidden=currentLevel===learningLevels.length-1;
    if(!promote.hidden){
      promote.textContent=currentLevel===0?'다음 수준: 간호 연결 →':
        '다음 수준: 추가학습 →';
    }
    model.hidden=detailLevel!=='advanced';
    advanced.hidden=detailLevel!=='advanced';
    if(detailLevel==='advanced'){
      for(const key of Object.keys(longNodes))longNodes[key].textContent=data[key];
    }
    for(const level of questions.levels)renderQuestion(level);
    const filling=stage.id==='filling';
    model.textContent='모델 대표 관찰점 '+Math.round(obs.midpointMs)+' / '+
       Math.round(obs.rrMs)+' ms · 학습 단계 이동 시 기존 Timeline으로 자동 관찰';
    limits.textContent=(filling?
       (detailLevel==='basic'?
         '이 앱에서는 RR 주기의 앞부분과 뒷부분에 충만 단계가 나타나며, 용적의 변화가 서로 다릅니다. ':
         '모형 주의: 시뮬레이터 RR의 앞 충만 구간은 상대 용적 0.88로 평탄하며, 뒤 충만 구간은 증가합니다. '):'')+
       (detailLevel==='advanced'?
       '압력·용적은 교육용 상대 지표이며 mmHg, mL, EF 또는 심박출량을 뜻하지 않습니다.':
       '이 그림은 교육용 모형입니다. 수치는 실제 환자의 혈압·심실 용적이 아닙니다.');
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
    const readingKey=[selectedIndex,live.heartRate,detailLevel].join('|');
    if(lastRenderedSelection!==readingKey){
      renderSelected();
      lastRenderedSelection=readingKey;
    }
  }
  function setOpen(next){
    if(open===next)return;
    open=next;
    panel.hidden=!open;
    clinical.hidden=open;
    if(open)lastRenderedSelection='';
    toggle.setAttribute('aria-expanded',String(open));
    toggle.textContent=open?'학습 닫기':(hasStarted?'5단계 학습 이어보기':'5단계 학습 시작');
    originalHeading.textContent=open?'5단계 심장 주기 학습':'실시간 통합 해설';
    if(open){
      lastKey='';sync();
      // First explicit course entry from Ready gives a visible first stage.
      // Reopening during playback/after leaving a study does not secretly seek.
      if(!hasStarted){
        const startAtReady=dashboard.isReady;
        hasStarted=true;
        if(startAtReady)observeSelected();
      }
    }else {lastKey='';toggle.focus();}
  }
  toggle.addEventListener('click',()=>setOpen(!open));
  function chooseStage(index){
    if(index<0||index>=content.stages.length||index===selectedIndex)return;
    selectedIndex=index;
    lastKey='';
    sync();
    // Guided navigation is the deliberate learner action: pause/seek once.
    // The free-observation controls and original A/B driver remain untouched.
    if(open)observeSelected();
  }
  select.addEventListener('change',()=>{
    chooseStage(content.stages.findIndex(x=>x.id===select.value));
  });
  function chooseLevel(value){
    if(!learningLevels.includes(value)||value===detailLevel)return;
    detailLevel=value;
    if(detailLevel!=='advanced')advanced.open=false;
    // Level is educational UI state, never an implicit seek/pause.
    renderSelected();
    lastRenderedSelection=[selectedIndex,heartRate,detailLevel].join('|');
  }
  levelSelect.addEventListener('change',()=>chooseLevel(levelSelect.value));
  promote.addEventListener('click',()=>{
    const index=learningLevels.indexOf(detailLevel);
    if(index>=0&&index<learningLevels.length-1)
      chooseLevel(learningLevels[index+1]);
  });
  for(const level of questions.levels){
    const ui=quizCards[level];
    for(const [i,{input}] of ui.choices.entries()){
      input.addEventListener('change',()=>{
        if(!input.checked)return;
        const item=questionFor(level);
        const before=answers[item.id];
        if(before?.submitted)return;
        answers[item.id]={choice:i,submitted:false};
        ui.submit.disabled=false;
      });
    }
    ui.submit.addEventListener('click',()=>{
      const item=questionFor(level);
      const saved=answers[item.id];
      if(!open||!saved||saved.choice===null||saved.submitted)return;
      answers[item.id]={choice:saved.choice,submitted:true};
      renderQuestion(level);
    });
    ui.retry.addEventListener('click',()=>{
      const item=questionFor(level);
      if(!open)return;
      delete answers[item.id];
      renderQuestion(level);
    });
  }
  prev.addEventListener('click',()=>chooseStage(selectedIndex-1));
  next.addEventListener('click',()=>chooseStage(selectedIndex+1));
  view.addEventListener('click',()=>{
    if(!open)return;
    // Separate explicit user action; no Timeline or playback side effects.
    dashboard.setView('wiggers');
  });
  function observeSelected(){
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
  }
  seek.addEventListener('click',observeSelected);
  root.CardiacGuidedLearning=Object.freeze({
    sync,
    get open(){return open;},
    get selectedStageId(){return content.stages[selectedIndex].id;},
    get detailLevel(){return detailLevel;},
    get submittedAnswerCount(){
      return Object.values(answers).filter(x=>x.submitted).length;
    },
    get version(){return 'v1.12 Patch 12';}
  });
})(window);
