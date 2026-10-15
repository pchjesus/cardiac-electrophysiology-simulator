/*
 * v1.13 Patch 1 — top-level route adapter (not a second simulator).
 * Clinical and Learning are preview-only until their real content ships.
 * DO NOT start Guided, seek Timeline, duplicate native DOM, or own A/B time.
 */
(function(root){
  'use strict';
  const app=document.querySelector('.app');
  const header=app?.querySelector('.header');
  const simulator=app?.querySelector('.main-container');
  if(!app||!header||!simulator||!root.CardiacDashboard||
     typeof root.pause!=='function'||typeof heartState==='undefined')return;

  // Visual QA entry only, not a security boundary or a public feature release.
  const preview=new URLSearchParams(root.location.search).get('v113Preview')==='1';
  simulator.id='v113SimulatorScreen';
  simulator.setAttribute('aria-label','시뮬레이터 화면');

  const nav=document.createElement('nav');
  nav.className='v113-main-nav';
  nav.setAttribute('aria-label','교육 플랫폼 상위 화면');
  const group=document.createElement('div');
  group.className='v113-main-nav-buttons';
  group.setAttribute('role','group');
  group.setAttribute('aria-label','시뮬레이터·학습·임상 적용');
  const screens={simulator};
  const buttons={};
  const labels={
    simulator:'① 시뮬레이터',
    learning:'② 학습',
    clinical:'③ 임상 적용'
  };
  const descriptions={
    learning:[
      '기존 5단계 심장주기 학습과 10개 개념 문항은 학습 탭에서 이용할 수 있습니다.',
      '학습 주제와 심장주기 5단계는 별개이며, 단원을 고르는 것만으로 시간은 이동하지 않습니다.'
    ],
    clinical:[
      '임상 적용에서는 가상 환자의 심전도(ECG), 검사 결과를 토대로 간호 판단을 연습합니다.',
      '현재 가상 임상 사례는 전문가 검토 전이므로 일반 사용자에게 비활성화되어 있습니다.'
    ]
  };
  function previewPanel(name,title){
    const section=document.createElement('section');
    section.className='v113-preview-screen';
    section.id='v113'+(name==='learning'?'Learning':'Clinical')+'Screen';
    section.hidden=true;
    section.setAttribute('aria-label',title+' 개발 미리보기');
    const card=document.createElement('div');
    card.className='card v113-preview-card';
    const heading=document.createElement('h2');
    heading.textContent=title;
    const status=document.createElement('p');
    status.className='v113-preview-status';
    status.textContent='v1.13 개발 검증용 미리보기 · 정식 임상 콘텐츠 승인 전';
    card.append(heading,status);
    for(const sentence of descriptions[name]){
      const p=document.createElement('p');p.textContent=sentence;card.append(p);
    }
    section.append(card);
    return section;
  }
  screens.learning=previewPanel('learning','학습');
  screens.clinical=previewPanel('clinical','임상 적용');

  let activeMainTab='simulator',guideWasMoved=false;
  const guideToggle=document.getElementById('guidedV112Toggle');
  const guidePanel=document.getElementById('guidedV112Panel');
  const inspectorHeading=document.querySelector('.dashboard-inspector-heading');
  const liveClinical=document.querySelector('.dashboard-clinical');
  const guideState=root.CardiacGuidedLearning;
  function relocateGuide(next){
    const host=root.CardiacCourseV113?.guideHost;
    if(!host||!guideToggle||!guidePanel||!inspectorHeading||!liveClinical)return;
    if(next==='learning'){
      guideWasMoved=true;
      host.append(guideToggle,guidePanel);
      guidePanel.hidden=!guideState.open;
      guideToggle.textContent=guideState.open?'학습 닫기':
        guideState.hasStarted?'5단계 학습 이어보기':'5단계 학습 시작';
      guideToggle.setAttribute('aria-expanded',String(guideState.open));
      liveClinical.hidden=false;
      if(inspectorHeading.firstChild?.nodeType===3)
        inspectorHeading.firstChild.textContent='실시간 통합 해설';
    }else if(guideWasMoved){
      inspectorHeading.append(guideToggle);
      liveClinical.before(guidePanel);
      guidePanel.hidden=true;
      liveClinical.hidden=false;
      guideToggle.textContent='5단계 학습으로 이동 →';
      guideToggle.setAttribute('aria-expanded','false');
      if(inspectorHeading.firstChild?.nodeType===3)
        inspectorHeading.firstChild.textContent='실시간 통합 해설';
    }
  }
  guideToggle?.addEventListener('click',event=>{
    if(guideWasMoved&&activeMainTab==='simulator'){
      event.stopImmediatePropagation();
      switchMainTab('learning');
    }
  },true);
  function switchMainTab(next){
    if(!Object.hasOwn(screens,next)||next===activeMainTab)return false;
    if(!preview&&next==='learning'&&!root.CardiacCourseV113?.ready)return false;
    if(!preview&&next==='clinical'&&!root.CardiacClinicalV113?.publicReady)return false;
    // Canonical script.js pause invalidates RAF without seeking either clock.
    if(heartState.playing)root.pause();
    relocateGuide(next);
    for(const [id,screen] of Object.entries(screens)){
      const selected=id===next;
      screen.hidden=!selected;
      buttons[id].setAttribute('aria-pressed',String(selected));
      buttons[id].classList.toggle('v113-active',selected);
    }
    activeMainTab=next;
    // Never leave keyboard focus in a newly hidden screen.
    buttons[next]?.focus({preventScroll:true});
    if(next==='simulator'){
      // Reuse existing read-only presentation sync. No Reset, Play or Seek.
      root.CardiacDashboard?.sync();
    }
    return true;
  }
  for(const [id,label] of Object.entries(labels)){
    const button=document.createElement('button');
    button.type='button';
    button.className='v113-main-tab';
    button.id='v113Tab'+id.charAt(0).toUpperCase()+id.slice(1);
    button.textContent=label;
    button.setAttribute('aria-controls',id==='simulator'?'v113SimulatorScreen':
      id==='learning'?'v113LearningScreen':'v113ClinicalScreen');
    button.setAttribute('aria-pressed',String(id==='simulator'));
    if(!preview&&((id==='learning'&&!root.CardiacCourseV113?.ready)||
      (id==='clinical'&&!root.CardiacClinicalV113?.publicReady))){
      button.disabled=true;
      button.setAttribute('aria-disabled','true');
      button.title=id==='clinical'?'임상 전문가의 콘텐츠 검토 전이므로 현재 공개되지 않습니다':'학습 화면 준비 중';
      const suffix=document.createElement('small');
      suffix.textContent=' 준비 중';
      button.append(suffix);
    }
    button.addEventListener('click',()=>switchMainTab(id));
    buttons[id]=button;
    group.append(button);
  }
  nav.append(group);
  app.insertBefore(nav,simulator);
  app.append(screens.learning,screens.clinical);
  root.CardiacCourseV113?.mount(screens.learning);
  root.CardiacClinicalV113?.mount(screens.clinical);
  root.CardiacMainTabs=Object.freeze({
    switchTo:switchMainTab,
    get active(){return activeMainTab;},
    get preview(){return preview;}
  });
})(window);
