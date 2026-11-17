/* CARDIA v8 / Inquiry-first learning and motion layer.
   This is a presentation adapter. The native engine, timelines, lesson source,
   completion persistence, gated clinical content and Wiggers calculations remain authoritative. */
(function (root) {
  'use strict';
  const $ = id => document.getElementById(id);
  const app = $('v7App'), screen = $('v113LearningScreen');
  const course = root.CardiacCourseV113;
  if (!app || !screen || !course || !root.CardiaV7?.ready) return;

  const curriculum = [
    {
      id:'unit-cardiac-cycle', number:'01', name:'심장주기', question:'한 번의 심장 박동에는 어떤 순서가 있을까?',
      brief:'전기적 활성화와 기계적 사건은 같은 시계 위에서 서로 연결돼 있어요. 한 장면만 보지 말고 전후 관계를 살펴보세요.',
      label:'한 박동의 시간적 연결', watch:'일시정지한 다음 시간축을 조금씩 움직여 심장의 단계와 ECG가 함께 바뀌는 순간을 찾아보세요.',
      steps:['전기적 활성화','압력과 수축 변화','판막·혈류 반응','ECG와 연결'], view:'electrical',
      quiz:'전기적 활성화와 실제 심장 수축을 어떻게 이해해야 할까요?',
      options:['서로 무관한 두 사건이다','전기적 활성화가 기계적 반응에 앞선다','판막이 열려야 전기 자극이 시작된다'], correct:1,
      why:'전기적 활성화가 먼저 나타나고 이어서 수축과 압력 변화가 발생해요. 이 관계를 하나의 생리학적 시간축에서 관찰하는 것이 핵심이에요.'
    },
    {
      id:'unit-conduction', number:'02', name:'전기전도', question:'전기 신호는 어디에서 시작해 어디로 퍼질까?',
      brief:'전도계는 여러 구조가 무작위로 반응하는 것이 아니라, 일정한 순서로 흥분을 전달하는 경로예요.',
      label:'전도 경로 추적', watch:'전기전도 보기를 선택한 다음 동방결절에서 시작하는 활성 표시를 단계별로 따라가 보세요.',
      steps:['동방결절 SA','방실결절 AV','히스다발·좌우각','푸르키녜 섬유'], view:'electrical',
      quiz:'정상 전도 경로의 일반적인 시작 지점은 어디일까요?',
      options:['동방결절(SA node)','방실결절(AV node)','푸르키녜 섬유'], correct:0,
      why:'정상 동율동에서는 동방결절에서 자극이 시작해 방실결절, 히스-푸르키녜계를 거쳐 심실로 전달돼요.'
    },
    {
      id:'unit-ecg-timing', number:'03', name:'ECG 읽기', question:'P파와 QRS파는 각각 어떤 사건을 뜻할까?',
      brief:'심전도는 심장 근육이 직접 움직이는 그림이 아니라, 전기적 활성화의 변화를 기록한 신호예요.',
      label:'파형과 사건 연결', watch:'ECG 파형을 살피면서 심방 탈분극과 심실 탈분극에 대응하는 부분을 찾아보세요.',
      steps:['P파','PR 간격','QRS 복합파','ST·T 구간'], view:'electrical',
      quiz:'일반적으로 QRS 복합파가 나타내는 현상은 무엇일까요?',
      options:['심방 재분극만을 기록','심실 탈분극','심실 기계적 박출 완료'], correct:1,
      why:'QRS 복합파는 심실 탈분극을 반영해요. 심실의 실제 수축·박출과는 의미와 시간이 같지 않다는 점을 구분해야 해요.'
    },
    {
      id:'unit-mechanics', number:'04', name:'판막과 수축', question:'판막은 근육처럼 직접 열리고 닫히는 걸까?',
      brief:'심장 판막은 압력 차이에 따라 수동적으로 열리고 닫혀요. 수축과 혈류를 함께 보면 역할이 더 분명해져요.',
      label:'압력 변화와 판막의 반응', watch:'수축·판막 보기에서 삼첨판·승모판·폐동맥판·대동맥판의 상태가 바뀌는 구간을 찾아보세요.',
      steps:['심방과 심실','방실판막','반월판막','압력 차이와 혈류'], view:'mechanical',
      quiz:'정상 판막의 개폐를 직접 결정하는 주요 원리는 무엇일까요?',
      options:['판막 자체의 능동적 수축','심장 방과 혈관 사이의 압력 차이','ECG 전극에서 나오는 신호'], correct:1,
      why:'판막은 각 공간의 압력 차이에 따라 수동적으로 움직여요. 교육용 그림은 이 관계를 단순화한 것으로 실제 판엽의 운동을 정밀 재현한 것은 아니에요.'
    },
    {
      id:'unit-wiggers', number:'05', name:'위거스 도표', question:'전기·압력·용적·심음을 한 시간축에 겹치면?',
      brief:'위거스 도표는 여러 생리학적 변화를 시간 순서로 나란히 비교하는 통합 그림이에요. 이 주제는 선택 학습이에요.',
      label:'시간축에서의 동시 비교', watch:'설정에서 위거스 학습을 켜고 해당 보기를 연 후, 같은 시점의 여러 변화가 어떻게 연결되는지 살펴보세요.',
      steps:['ECG','압력 변화','심실 용적','판막·심음'], view:'wiggers',
      quiz:'위거스 도표의 주된 목적은 무엇일까요?',
      options:['ECG만 더 크게 표시','서로 다른 심장 사건의 시간 관계 비교','새로운 심전도 진단 공식 제공'], correct:1,
      why:'위거스 도표는 ECG, 압력, 용적, 판막 사건 등 서로 다른 변화를 공통 시간축에 놓고 비교하도록 도와요.'
    },
    {
      id:'unit-nursing', number:'06', name:'간호 관찰', question:'파형을 읽었다면 환자에게서는 무엇을 확인해야 할까?',
      brief:'시뮬레이터의 정상 생리 모형을 이해한 다음, 실제 임상에서는 관찰과 사정을 어떻게 연결할지 구분해 보세요.',
      label:'생리 현상에서 간호 사정으로', watch:'심장주기와 ECG를 다시 관찰한 뒤 실제 환자 사정에는 증상·활력징후·관류 상태가 함께 필요함을 확인하세요.',
      steps:['리듬·파형','맥박·혈압','증상·관류','상황에 맞는 보고'], view:'electrical',
      quiz:'교육용 심전도 모형만으로 판단할 수 없는 것은 무엇일까요?',
      options:['전도 경로의 일반적인 순서','ECG 파형의 개념적 의미','실제 환자의 임상적 안정성'], correct:2,
      why:'환자의 상태는 파형 외에도 의식, 증상, 혈역학, 관류 상태 등 임상 사정이 필요해요. 교육용 시뮬레이터가 환자 평가를 대신하지 않아요.'
    }
  ];

  const base = $('v7Learn');
  const source = $('v7NativeCourse');
  if (!base || !source) return;
  const sourceHost = source.parentNode;
  const rootEl = document.createElement('section'); rootEl.id = 'v8Learning'; rootEl.className = 'v8-learning';
  rootEl.innerHTML = `
   <div class="v8-learn-hero">
     <div><p class="v8-eyebrow">CARDIA / LEARNING STUDIO</p><h1>읽는 공부에서,<br><em>발견하는 공부로.</em></h1><p class="v8-hero-desc">질문 하나를 고르고, 직접 심장 박동을 관찰한 다음, 내 언어로 이해해보세요.</p></div>
     <div class="v8-progress-panel"><span>YOUR JOURNEY / 실제 완료 기록</span><strong id="v8ProgressText">0 <small>/ 5</small></strong><div class="v8-progress-track"><i id="v8ProgressFill"></i></div><p>아래 이해 확인은 연습용이며 공식 완료 기록과 별개예요.</p></div>
   </div>
   <div class="v8-course-layout">
     <nav class="v8-path" aria-label="개념별 학습 경로"><header><div class="v8-section-kicker">YOUR PATH <span>01 — 06</span></div><h2>어디부터 탐구할까?</h2><p>관심 있는 질문부터 시작해도 좋아요.</p></header><div id="v8LessonList" class="v8-lesson-list"></div><div class="v8-path-foot">● 현재 탐구 중인 주제는 강조돼요.<br>원하는 순서로 이동할 수 있어요.</div></nav>
     <div class="v8-main">
       <div class="v8-lesson-top"><span id="v8LessonOverline">LESSON 01</span><div class="v8-lesson-tools"><button type="button" id="v8Previous" aria-label="이전 주제">← 이전</button><button type="button" id="v8Next">다음 주제 →</button></div></div>
       <h2 id="v8Question"></h2><p class="v8-intro" id="v8Intro"></p>
       <div class="v8-stepper" role="tablist" aria-label="학습 활동 선택"><button type="button" role="tab" id="v8StepDiscover" aria-selected="true" data-phase="discover"><i>01</i> 이해의 시작</button><button type="button" role="tab" id="v8StepObserve" aria-selected="false" data-phase="observe"><i>02</i> 직접 관찰</button><button type="button" role="tab" id="v8StepCheck" aria-selected="false" data-phase="check"><i>03</i> 이해 확인</button><span class="v8-step-indicator" aria-hidden="true"></span></div>
       <div class="v8-activity" id="v8Activity" role="tabpanel" aria-live="polite"></div>
       <div class="v8-lesson-bottom"><button type="button" id="v8ActivityBack" class="v8-text-control">← 이전 활동</button><button type="button" id="v8ActivityNext" class="v8-next-control">다음 활동 <span aria-hidden="true">→</span></button></div>
       <details class="v8-source" id="v8Source"><summary><span><b>원문 교재와 심화 설명</b><small>기존 학습 본문 · 근거 · 공식 학습 완료 기록</small></span><span class="v8-source-plus">+</span></summary><div id="v8NativeHost"></div></details>
       <div class="v8-lesson-fineprint">CARDIA 교육용 모형 · 실제 환자 진단이나 임상적 판단을 대신하지 않습니다.</div>
     </div>
   </div>`;
  screen.insertBefore(rootEl, base);
  $('v8NativeHost').append(source);
  base.hidden = true;
  let activeIndex = Math.max(0,curriculum.findIndex(x=>x.id===course.activeUnitId));
  let phase = 'discover';
  let answers = Object.create(null);
  const safeText = s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const enabled = x=> x.id !== 'unit-wiggers' || app.closest('.ps6-app')?.dataset.ps6Wiggers === 'on';
  const available = ()=>curriculum.filter(enabled);
  const motionReduced=()=>root.matchMedia('(prefers-reduced-motion: reduce)').matches || app.closest('.ps6-app')?.dataset.ps6LessMotion==='true';
  const item = ()=>curriculum[activeIndex];
  const phaseSequence=['discover','observe','check'];

  function updateNav() {
    const old=document.querySelector('#v8LessonList .v8-current');
    const current=item();
    $('v8LessonList').innerHTML='';
    for (const chapter of available()) {
      const complete=(course.completedUnitIds||[]).includes(chapter.id);
      const b=document.createElement('button');
      b.type='button';b.className='v8-path-item'+(chapter.id===current.id?' v8-current':'');
      b.dataset.unit=chapter.id;b.setAttribute('aria-current',chapter.id===current.id?'step':'false');
      b.innerHTML=`<span class="v8-path-num">${chapter.number}</span><span class="v8-path-text"><strong>${safeText(chapter.name)}</strong><small>${safeText(chapter.question)}</small></span><span class="v8-path-status">${complete?'✓':chapter.id===current.id?'↗':'·'}</span>`;
      b.addEventListener('click',()=>choose(chapter.id));
      $('v8LessonList').append(b);
    }
    const complete=(course.completedUnitIds||[]).filter(id=>available().some(x=>x.id===id)).length;
    const total=available().length;
    $('v8ProgressText').innerHTML=`${complete} <small>/ ${total}</small>`;
    $('v8ProgressFill').style.width=Math.round(100*complete/total)+'%';
  }

  function choose(id){
    const idx=curriculum.findIndex(x=>x.id===id);
    if(idx<0||!enabled(curriculum[idx]))return;
    activeIndex=idx;phase='discover';
    course.selectUnit(id); render(true);
  }
  function switchPhase(next) {
    if(!phaseSequence.includes(next) || phase===next)return;
    phase=next;renderActivity(true);
  }
  const goLab=()=>{
    document.documentElement.dataset.v8Direction='reverse';
    // Native v7 action preserves the existing timeline, route pause, view and opt-in gate.
    $('v7ObserveNow').click();
  };

  function renderActivity(animate=false){
    const c=item(), panel=$('v8Activity');
    for (const b of $('v8Learning').querySelectorAll('.v8-stepper [role=tab]')) {
      b.setAttribute('aria-selected',String(b.dataset.phase===phase));
      b.tabIndex=b.dataset.phase===phase?0:-1;
    }
    $('v8StepDiscover').parentElement.dataset.active=phase;
    const nextIndex=phaseSequence.indexOf(phase);
    $('v8ActivityBack').hidden=nextIndex===0;
    $('v8ActivityNext').innerHTML=(nextIndex===2?'관찰실에서 확인하기':'다음 활동')+' <span aria-hidden="true">→</span>';
    let content='';
    if(phase==='discover') {
      content=`<div class="v8-activity-kicker">THINK FIRST / 생각해 보기</div><h3>${safeText(c.label)}</h3><p>먼저 다음 네 요소가 어떻게 연결될지 생각해봐요. 순서를 무조건 암기하기보다는 <b>사건 사이의 관계</b>를 살펴보는 게 목표예요.</p><div class="v8-sequence">${c.steps.map((s,i)=>`<div class="v8-seq-item"><span>${String(i+1).padStart(2,'0')}</span><strong>${safeText(s)}</strong></div>`).join('')}</div><div class="v8-insight"><span class="v8-insight-icon">✦</span><p><b>학습 포인트</b><br>${safeText(c.brief)}</p></div>`;
    } else if(phase==='observe') {
      content=`<div class="v8-activity-kicker">OBSERVE / 직접 실험하기</div><h3>직접 움직이며 확인해요.</h3><p>${safeText(c.watch)}</p><div class="v8-experiment"><div class="v8-experiment-glyph" aria-hidden="true"><span class="v8-circle a"></span><span class="v8-circle b"></span><span class="v8-circle c"></span><span class="v8-exp-line"></span></div><div><b>실험 도구로 이동</b><small>원본 엔진의 시간축 · ECG · 심장 도식 사용</small></div><button type="button" id="v8LaunchLab">심장 관찰실 열기 ↗</button></div><p class="v8-note">시뮬레이터에서 재생·일시정지·시간 이동을 자유롭게 해봐요. 학습 화면으로 돌아와도 선택했던 주제는 유지돼요.</p>`;
    } else {
      const answer=answers[c.id];
      content=`<div class="v8-activity-kicker">RECALL / 이해 확인 · 연습용</div><h3>${safeText(c.quiz)}</h3><p>세 가지 중 하나를 골라봐요. 결과를 바로 확인할 수 있지만, 공식 학습 완료 기록은 자동 변경되지 않아요.</p><div class="v8-answers">${c.options.map((x,i)=>`<button type="button" class="v8-answer${answer===i?' v8-answer-picked':''}${answer!==undefined&&i===c.correct?' v8-answer-correct':''}" data-answer="${i}" aria-pressed="${answer===i}"><span>${String.fromCharCode(65+i)}</span><strong>${safeText(x)}</strong><i>${answer===i?(i===c.correct?'✓':'↺'):'↗'}</i></button>`).join('')}</div>${answer===undefined?'<div class="v8-answer-hint">정답을 선택하면 설명이 나타납니다.</div>':`<div class="v8-feedback" role="status"><b>${answer===c.correct?'정확해요.':'다시 연결해볼까요?'}</b><p>${safeText(c.why)}</p></div>`}`;
    }
    const previousHeight=panel.offsetHeight;
    panel.innerHTML=content;
    if(phase==='observe') $('v8LaunchLab').addEventListener('click',goLab);
    if(phase==='check') for(const btn of panel.querySelectorAll('[data-answer]'))btn.addEventListener('click',()=>{answers[c.id]=Number(btn.dataset.answer);renderActivity(false)});
    if(animate&&!motionReduced()){
      panel.getAnimations().forEach(x=>x.cancel());
      panel.animate([{opacity:.25,transform:'translateY(9px)'},{opacity:1,transform:'translateY(0)'}],{duration:350,easing:'cubic-bezier(.22,1,.36,1)'});
    }
  }
  function render(animate=false){
    const c=item();
    $('v8LessonOverline').textContent=`LESSON ${c.number} / ${c.name}`;
    $('v8Question').textContent=c.question;
    $('v8Intro').textContent=c.brief;
    updateNav();renderActivity(animate);
    const list=available();let index=list.findIndex(x=>x.id===c.id);
    $('v8Previous').disabled=index===0;
    $('v8Next').disabled=index===list.length-1;
    if(animate&&!motionReduced()){
      const title=$('v8Question');title.getAnimations().forEach(x=>x.cancel());title.animate([{opacity:.3,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:460,easing:'cubic-bezier(.22,1,.36,1)'});
    }
  }
  for(const b of $('v8Learning').querySelectorAll('.v8-stepper [role=tab]')){
    b.addEventListener('click',()=>switchPhase(b.dataset.phase));
    b.addEventListener('keydown',e=>{
      if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft'&&e.key!=='Home'&&e.key!=='End')return;
      e.preventDefault();const idx=phaseSequence.indexOf(phase);
      const newIdx=e.key==='Home'?0:e.key==='End'?2:(idx+(e.key==='ArrowRight'?1:2))%3;
      switchPhase(phaseSequence[newIdx]);$('v8Learning').querySelector(`[data-phase="${phase}"]`).focus();
    });
  }
  $('v8ActivityNext').addEventListener('click',()=>{const i=phaseSequence.indexOf(phase);if(i===2)goLab();else switchPhase(phaseSequence[i+1]);});
  $('v8ActivityBack').addEventListener('click',()=>{const i=phaseSequence.indexOf(phase);if(i>0)switchPhase(phaseSequence[i-1]);});
  const navLesson=direction=>{const list=available(),i=list.findIndex(x=>x.id===item().id);const next=list[i+direction];if(next)choose(next.id);};
  $('v8Previous').addEventListener('click',()=>navLesson(-1));$('v8Next').addEventListener('click',()=>navLesson(1));
  const nativeCourse=$('v8NativeHost');
  const monitor=new MutationObserver(()=>{
    const current=course.activeUnitId;
    if(current&&current!==item().id){const idx=curriculum.findIndex(x=>x.id===current);if(idx>=0&&enabled(curriculum[idx])){activeIndex=idx;phase='discover';render();return;}}
    const active=available().map(x=>x.id).join('/');
    if(rootEl.dataset.available!==active){rootEl.dataset.available=active;if(!enabled(item())){activeIndex=0;course.selectUnit(item().id);render();}else updateNav();}else updateNav();
  });
  monitor.observe(nativeCourse,{childList:true,subtree:true});
  const appObserver=new MutationObserver(()=>{const next=available().map(x=>x.id).join('/');if(rootEl.dataset.available!==next){rootEl.dataset.available=next;if(!enabled(item())){activeIndex=0;course.selectUnit(item().id);}render();}});
  appObserver.observe(app.closest('.ps6-app'),{attributes:true,attributeFilter:['data-ps6-wiggers']});

  // Active navigation backdrop follows the actual route rather than a fake timer.
  const nav=$('v7Nav');
  if(nav){
    const slider=document.createElement('span');slider.className='v8-nav-slider';slider.setAttribute('aria-hidden','true');nav.prepend(slider);
    const placeSlider=()=>{
      const selected=nav.querySelector('.v113-main-tab.v113-active');if(!selected)return;
      const navRect=nav.getBoundingClientRect(),r=selected.getBoundingClientRect();
      slider.style.top=(r.top-navRect.top)+'px';slider.style.height=r.height+'px';
    };
    new MutationObserver(placeSlider).observe(nav,{subtree:true,attributes:true,attributeFilter:['class']});
    root.addEventListener('resize',placeSlider,{passive:true});
    root.requestAnimationFrame(placeSlider);
  }
  // Route direction used by main-tab View Transition animations.
  for(const [id,direction] of [['v113TabLearning','forward'],['v113TabSimulator','reverse'],['v7Study','forward'],['v7GoTheory','forward'],['v8Previous','reverse'],['v8Next','forward']])$(id)?.addEventListener('click',()=>{document.documentElement.dataset.v8Direction=direction;},{capture:true});
  rootEl.dataset.available=available().map(x=>x.id).join('/');
  render();
  root.CardiaV8=Object.freeze({ready:true,version:'inquiry-studio-v8',get activeUnit(){return item().id},get phase(){return phase},get wiggersEnabled(){return available().some(x=>x.id==='unit-wiggers')},get practiceAnswer(){return answers[item().id]},selectUnit:choose,selectPhase:switchPhase});
})(window);
