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
      '5단계 심장주기와 3수준 학습, 기존 10개 개념 문항은 현재 시뮬레이터의 통합 해설에서 정상 작동합니다.',
      '이 화면은 상위 탭과 일시정지·복귀 동작을 검증하기 위한 개발 미리보기입니다. Patch 2에서 기존 학습 DOM과 답안을 안전하게 연결합니다.'
    ],
    clinical:[
      '임상 적용은 가상 환자 자료, ECG·검사 결과, 간호 판단과 재평가를 학습하는 독립 세션으로 개발할 예정입니다.',
      '현재는 사례·환자 수치·문제풀이 기능이 제공되지 않습니다. 개발 미리보기에서는 화면 전환과 A/B 시간 보존만 검증합니다.'
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
    status.textContent='v1.13 Patch 1 · 내부 화면 전환 검증용 · 교육 기능 미출시';
    card.append(heading,status);
    for(const sentence of descriptions[name]){
      const p=document.createElement('p');p.textContent=sentence;card.append(p);
    }
    section.append(card);
    return section;
  }
  screens.learning=previewPanel('learning','학습');
  screens.clinical=previewPanel('clinical','임상 적용');

  let activeMainTab='simulator';
  function switchMainTab(next){
    if(!Object.hasOwn(screens,next)||next===activeMainTab)return false;
    if(!preview && next!=='simulator')return false;
    // Canonical script.js pause invalidates RAF without seeking either clock.
    if(heartState.playing)root.pause();
    for(const [id,screen] of Object.entries(screens)){
      const selected=id===next;
      screen.hidden=!selected;
      buttons[id].setAttribute('aria-pressed',String(selected));
      buttons[id].classList.toggle('v113-active',selected);
    }
    activeMainTab=next;
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
    if(!preview&&id!=='simulator'){
      button.disabled=true;
      button.setAttribute('aria-disabled','true');
      button.title='해당 교육 화면은 후속 패치에서 공개됩니다';
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
  root.CardiacMainTabs=Object.freeze({
    switchTo:switchMainTab,
    get active(){return activeMainTab;},
    get preview(){return preview;}
  });
})(window);
