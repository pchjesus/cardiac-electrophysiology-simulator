/*
 * Cardiac Experience v2 — presentation adapter for the review-only experience.html.
 * Authoritative engine, A/B clocks, controller listeners, Guided, Course and Clinical
 * are initialized by their original modules BEFORE this adapter.
 * No new simulation clock, polling, RAF, duplicated original controls or clinical state.
 */
(function(root){
  'use strict';
  const $=id=>document.getElementById(id);
  const app=document.querySelector('.app');
  const main=app?.querySelector('.main-container');
  const dashboard=$('dashboardV111');
  const siteHeader=app?.querySelector('.header');
  const navigation=app?.querySelector('.v113-main-nav');
  const primary=dashboard?.querySelector('.dashboard-primary');
  const workspace=dashboard?.querySelector('.dashboard-workspace');
  const commands=dashboard?.querySelector('.dashboard-commands');
  const inspector=dashboard?.querySelector('.dashboard-inspector');
  const measurements=dashboard?.querySelector('.measurements-panel');
  const resources=dashboard?.querySelector('.dashboard-resources');
  if(!app||!main||!dashboard||!siteHeader||!navigation||!primary||
     !workspace||!commands||!inspector||!measurements||!resources||
     !root.CardiacDashboard||!root.CardiacMainTabs||
     !root.CardiacCourseV113||!root.CardiacClinicalV113){
    // Avoid partially rehosting the source DOM when a dependency is absent.
    document.documentElement.dataset.cxError='dependency';
    return;
  }

  const make=(tag,cls,txt)=>{
    const x=document.createElement(tag);
    if(cls)x.className=cls;
    if(txt!==undefined)x.textContent=txt;
    return x;
  };
  const section=(cls,eyebrow,title,description)=>{
    const box=make('section',cls);
    const heading=make('div','cx-section-heading');
    heading.append(make('span','cx-eyebrow',eyebrow),make('h2','',title));
    if(description)heading.append(make('p','',description));
    box.append(heading);
    return box;
  };
  const elementsToPreserve=[
    'ecgCanvas','playBtn','pauseBtn','resetBtn','timeSlider','heartRateSlider',
    'heartSVG','mechanicalSVG','wiggersChart','guidedV112Panel'
  ];
  // Verify original authoritative nodes exist before moving any of them.
  if(!elementsToPreserve.every(id=>$(id)&&document.querySelectorAll('#'+id).length===1)){
    document.documentElement.dataset.cxError='original-node';
    return;
  }

  document.documentElement.classList.add('cx-enabled');
  document.body.classList.add('cx-enabled');
  app.classList.add('cx-experience');

  const heading=siteHeader.querySelector('h1');
  const description=siteHeader.querySelector('p');
  const support=siteHeader.querySelector('.header-tools');
  siteHeader.classList.add('cx-masthead');
  if(heading){
    heading.textContent='CARDIAC';
    heading.setAttribute('aria-label','Cardiac 심장 전기생리 학습실');
  }
  if(description)description.textContent='INTERACTIVE PHYSIOLOGY LAB';
  if(support)support.classList.add('cx-support-tools');
  navigation.classList.add('cx-primary-nav');
  const firstTab=siteHeader.querySelector('.header-tools');
  if(firstTab)siteHeader.insertBefore(navigation,firstTab);
  else siteHeader.append(navigation);

  // Keep original tab buttons and routing/gate handlers; change labels only.
  for(const [id,label] of [['Simulator','탐구'],['Learning','학습'],['Clinical','임상 적용']]){
    const button=$('v113Tab'+id);
    if(!button)continue;
    if(button.firstChild?.nodeType===Node.TEXT_NODE){
      button.firstChild.textContent=label;
    }
    if(id==='Clinical'&&button.disabled)
      button.setAttribute('aria-label','임상 적용 · 전문가 검토 전 비공개');
  }

  const intro=make('section','cx-intro');
  const introText=make('div','cx-intro-copy');
  introText.append(
    make('p','cx-overline','STUDY THE HEARTBEAT  /  심장 전기생리'),
    make('h2','cx-intro-title','심장의 한 주기를, 연결해서 이해하다.'),
    make('p','cx-intro-description',
      '심전도의 전기 신호가 심장 수축과 판막 움직임으로 이어지는 과정을 같은 시간축에서 살펴보세요.')
  );
  const introGuide=make('div','cx-intro-guide');
  introGuide.setAttribute('aria-label','탐구의 순서');
  for(const [num,head,copy] of [
    ['01','파형을 본다','P · QRS · T'],
    ['02','움직임을 비교한다','전도 · 수축 · 위거스'],
    ['03','의미를 해석한다','생리 변화 · 간호 사정']
  ]){
    const item=make('div','cx-intro-guide-item');
    item.append(make('span','cx-intro-num',num),make('strong','',head),make('small','',copy));
    introGuide.append(item);
  }
  intro.append(introText,introGuide);

  const trace=section('cx-trace','01  /  ELECTRICAL SIGNAL','심전도 파형',
    '전기적 변화와 심장주기 시간을 함께 관찰하세요. 아래 파형 버튼은 원래의 상세 설명을 엽니다.');
  trace.append(primary);
  // The original concept-popup buttons were inside legacy headings. Move those
  // exact nodes beside new visible section titles instead of hiding their aids.
  const ecgTerm=primary.querySelector('.ecg-panel h2 [data-term-help="ecg"]');
  if(ecgTerm)trace.querySelector('.cx-section-heading').append(ecgTerm);
  const metricsTerm=measurements.querySelector('h2 [data-term-help="measurements"]');
  if(metricsTerm){
    // metrics is declared below; defer the move until its new host exists.
    metricsTerm.dataset.cxRehome='measurements';
  }
  const control=section('cx-control','02  /  CONTROL THE CYCLE','시간과 심박수',
    '재생·일시정지·초기화는 기존 생리 시계를 제어합니다. 관찰 지점을 직접 이동할 수 있어요.');
  control.append(commands);
  const compare=section('cx-compare','03  /  CONNECT THE DOTS','전기와 수축을 비교하기',
    '세 보기는 하나의 심장주기 모델을 공유합니다. 보기 전환만으로 시간은 이동하지 않습니다.');
  const comparisonGrid=make('div','cx-compare-grid');
  comparisonGrid.append(workspace,inspector);
  compare.append(comparisonGrid);
  const metrics=section('cx-metrics','04  /  READ THE NUMBERS','심전도 측정값',
    '교육용 동율동 모델의 간격입니다. 환자 측정값이나 진단 결과가 아닙니다.');
  metrics.append(measurements);
  if(metricsTerm)metrics.querySelector('.cx-section-heading').append(metricsTerm);
  const more=section('cx-more','05  /  DEEPER STUDY','더 알아보기',
    '전도 경로와 심장 단계의 상세 근거, 위거스 학습 자료를 원본 그대로 확인할 수 있어요.');
  more.append(resources);
  const footer=make('footer','cx-educational-footer',
    '교육용 시뮬레이터 · 압력/심실 용적은 상대 지표이며, 임상 진단·치료 결정을 대신하지 않습니다.');
  dashboard.replaceChildren(intro,trace,control,compare,metrics,more,footer);
  main.classList.add('cx-main');

  // Learning content and original Guided 10 questions are unchanged; only a new reading shell.
  const learning=$('v113LearningScreen');
  const clinical=$('v113ClinicalScreen');
  function screenLead(screen,kicker,title,subtitle){
    if(!screen)return null;
    screen.classList.add('cx-designed-screen');
    const lead=make('div','cx-screen-lead');
    lead.append(make('span','cx-overline',kicker),
      make('h2','',title),make('p','',subtitle));
    screen.prepend(lead);
    return lead;
  }
  screenLead(learning,'LEARNING STUDIO  /  6 TOPICS',
    '개념을 읽고, 직접 관찰하고, 설명해 보세요.',
    '원본 6개 학습 주제와 심장주기 5단계·10문항을 그대로 사용합니다. 단원 탐색만으로 시뮬레이터 시간은 변경되지 않습니다.');
  const clinicalLead=screenLead(clinical,'CLINICAL REASONING  /  QA PREVIEW',
    '관찰에서 판단까지, 환자를 중심으로.',
    '개발 검증용 가상 사례입니다. 임상 전문가의 독립 검토와 공개 승인 전까지 일반 사용자에게는 비활성화되어 있습니다.');

  // Clinical's authoritative render() deliberately replaces its own children after
  // each decision. Preserve only the presentation heading across those renders.
  // This observer does not read answers, write session state, or run a clock.
  if(clinical&&clinicalLead){
    new MutationObserver(()=>{
      if(clinical.isConnected&&clinicalLead.parentElement!==clinical)
        clinical.prepend(clinicalLead);
    }).observe(clinical,{childList:true});
  }

  // Semantic original sliders; these labels do not change native value/step handlers.
  $('timeSlider')?.setAttribute('aria-label','심장주기 관찰 시점 0–100퍼센트');
  $('heartRateSlider')?.setAttribute('aria-label','심박수 분당 30–180회');

  // Optional mobile swipe between the existing Heart views. Never intercept the
  // Wiggers chart horizontal-scroll region, or invoke domain time/HR functions.
  let touchStart=null;
  for(const id of ['heartSVG','mechanicalSVG']){
    const surface=$(id);
    if(!surface)continue;
    surface.addEventListener('pointerdown',event=>{
      touchStart=event.pointerType==='touch'?
        {id:event.pointerId,x:event.clientX,y:event.clientY,from:root.CardiacDashboard.view}:null;
    },{passive:true});
    surface.addEventListener('pointercancel',()=>{touchStart=null;},{passive:true});
    surface.addEventListener('pointerup',event=>{
      const start=touchStart;touchStart=null;
      if(!start||start.id!==event.pointerId)return;
      const dx=event.clientX-start.x,dy=event.clientY-start.y;
      if(Math.abs(dx)<70||Math.abs(dx)<Math.abs(dy)*1.4)return;
      if(root.CardiacDashboard.view!==start.from)return;
      const order=['electrical','mechanical','wiggers'];
      const before=order.indexOf(start.from),to=before+(dx<0?1:-1);
      if(before<0||to<0||to>=order.length)return;
      const button=to===0?$('electricalModeBtn'):
        to===1?$('mechanicalModeBtn'):$('dashboardWiggersBtn');
      button?.click(); // Native handler owns visualization mode; no time mutation.
    },{passive:true});
  }

  // Nonfunctional decorative transition is CSS-only and short; no second RAF.
  root.CardiacExperienceV2=Object.freeze({
    get version(){return 'v2-review';},
    get source(){return 'original-v1.13-engine';},
    get view(){return root.CardiacDashboard.view;},
    get currentScreen(){return root.CardiacMainTabs.active;}
  });
})(window);
