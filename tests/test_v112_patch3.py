"""v1.12 Patch 3 — real-browser clinical learning and quiz regression.

No simulator state is owned by the guide's 10 qualitative questions.
Existing 12 suites must remain separately green.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SHOT=ROOT/'preview-v112p3'
SHOT.mkdir(exist_ok=True)
n=0
def ck(test,name):
 global n
 n+=1
 assert test,name

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',
   args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1366,'height':768})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'index.html').as_uri(),wait_until='load')
 page.wait_for_function('["v1.12 Patch 3","v1.12 Patch 4","v1.12 Patch 5","v1.12 Patch 6","v1.12 Patch 7","v1.12 Patch 8","v1.12 Patch 9","v1.12 Patch 10","v1.12 Patch 11","v1.12 Patch 12","v1.12 Patch 13"].includes(window.CardiacGuidedLearning?.version)')
 ck('v1.12 Patch ' in page.locator('h1').inner_text(),'version')
 ck(page.evaluate('CardiacDashboard.density')=='compact','compact default')
 ck(page.locator('#guidedV112Panel').is_hidden(),'new content incorrectly visible by default')
 ck(page.locator('.dashboard-clinical').is_visible(),'original short source hidden')
 ck(page.locator('#ecgCanvas').is_visible(),'original ECG missing')
 ck(page.evaluate("""() => {
   const nav=document.querySelector('.v113-main-nav');
   const style=nav&&getComputedStyle(nav);
   const navigationFootprint=nav ? nav.getBoundingClientRect().height+
     parseFloat(style.marginTop)+parseFloat(style.marginBottom) : 0;
   return document.documentElement.scrollHeight-navigationFootprint;
 }""")<=1150,
    'default desktop page grew beyond 16px height budget')
 ck(page.locator('#guidedV112Level').count()==1,'duplicate level control')
 ck(page.locator('#guidedV112Quiz').count()==1,'quiz missing')
 ck(page.locator('#guidedV112Advanced').count()==1,'deep learning missing')
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='basic','default difficulty not basic')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==0,'answered count not empty')
 ck(page.locator('#wiggersDeepDive').count()==1,'original six-part details lost')
 page.screenshot(path=str(SHOT/'01-default-compact-1366.png'),
    full_page=True,animations='disabled')

 # Immutable question bank is tied exactly to the signed-off curriculum;
 # no numerical patient prediction, score, medical qualification.
 stages=['atrial_systole','isovolumetric_contraction','ejection',
        'isovolumetric_relaxation','filling']
 keys=['basic','advanced']
 expected_answers=[[0,1],[0,0],[1,1],[0,1],[0,2]]
 bank=page.evaluate("""() => Object.fromEntries(
   CardiacGuidedContent.stages.map(s=>[
     s.id,CardiacGuidedQuestions.byStage[s.id].map(q=>({
       id:q.id,stage:q.stage,level:q.level,options:q.options,
       correct:q.correctIndex,explanation:q.explanation,wrong:q.wrong
     }))
   ])
 )""")
 ck(set(bank)==set(stages),'incorrect stage mapping')
 for i,stage in enumerate(stages):
    ck(len(bank[stage])==2,f'expected basic and advanced items at {stage}')
    for j,entry in enumerate(bank[stage]):
       ck(entry['stage']==stage and entry['level']==keys[j],
          f'question stage or tier corrupted at {stage}')
       ck(entry['correct']==expected_answers[i][j],
          f'wrong documented correct answer at {stage}:{j}')
       ck(len(entry['options'])==3 and len(entry['wrong'])==3,
          f'three validated alternatives required at {stage}:{j}')
       ck(len(entry['explanation'])>25,
          f'source-oriented reasoning missing at {stage}:{j}')
       ck(all(x.startswith(letter+'. ') for x,letter in zip(
          entry['options'],'ABC')),f'option labels changed at {stage}:{j}')
 ck(page.evaluate("CardiacGuidedQuestions.get('filling','advanced').correctIndex") ==2,
    'relative LV value must not be EF or mL')
 ck(page.evaluate("CardiacGuidedQuestions.get('ejection','advanced').correctIndex") ==1,
    'T wave vs aortic closure distinction incorrect')

 page.evaluate("""() => {
   window.__quizTimelineInputs=0;
   document.getElementById('timeSlider').addEventListener('input',
     ()=>window.__quizTimelineInputs++);
 }""")
 def state():
    return page.evaluate("""() => ({
     a:heartState.physiologicalTime,b:heartState.visualizationTime,
     cycle:heartState.cycleStartTime,sweep:heartState.sweepPosition,
     hr:heartRate,playing:heartState.playing,
     view:CardiacDashboard.view,mechanical:CardiacMechanical.mode,
     selected:CardiacGuidedLearning.selectedStageId,
     density:CardiacDashboard.density,
     timeline:window.__quizTimelineInputs
    })""")
 start=state()
 page.locator('#guidedV112Toggle').click()
 page.locator("#guidedV112Tools").evaluate("(e)=>e.open=true")
 ck(page.locator('#guidedV112Panel').is_visible(),'guide fails to open')
 ck(page.locator('.dashboard-clinical').is_hidden(),'original summary did not get replaced')
 ck(page.locator('#guidedV112Level').input_value()=='basic','level not initially basic')
 ck(page.locator('#guidedV112Advanced').is_hidden(),'advanced full text visible in basic mode')
 ck(page.locator('#guidedV112Quiz').evaluate('(el)=>!el.open'),
    'quiz expanded without user request')
 ck(page.locator('#guidedV112BasicQuestion').is_hidden(),
    'quiz content should remain hidden until native disclosure')
 ck(not state()['playing'] and state()['a']>0,'course start did not observe stage 1')
 start=state()
 page.screenshot(path=str(SHOT/'02-basic-guide-1366.png'),
    full_page=True,animations='disabled')

 page.locator('#guidedV112Quiz summary').click()
 ck(page.locator('#guidedV112BasicQuestion').is_visible(),
    'basic question not visible after disclosure opened')
 ck(page.locator('#guidedV112AdvancedQuestion').is_hidden(),
    'advanced item leaked into basic tier')
 ck(page.locator('#guidedV112SubmitBasic').is_disabled(),
    'answer-check available before a choice')
 ck(page.locator('#guidedV112FeedbackBasic').is_hidden(),
    'answer feedback / correct choice leaked pre-submission')

 # Exercise a WRONG basic answer first; reveal its source-supported
 # explanation only AFTER native submission. Retry wipes one item.
 first=bank[stages[0]][0]
 wrong=(first['correct']+1)%3
 page.locator('#guidedV112BasicQuestion input[type=radio]').nth(wrong).check()
 ck(page.locator('#guidedV112FeedbackBasic').is_hidden(),
    'revealed explanation before submission')
 ck(not page.locator('#guidedV112SubmitBasic').is_disabled(),
    'cannot submit a chosen answer')
 ck(state()==start,'choosing a radio answer changed simulation')
 page.locator('#guidedV112SubmitBasic').click()
 ck(page.locator('#guidedV112FeedbackBasic').get_attribute('data-result')=='incorrect',
    'wrong answer marked correct')
 text=page.locator('#guidedV112FeedbackBasic').inner_text()
 ck(first['options'][first['correct']] in text,
    'wrong answer did not identify correct answer after submission')
 ck(first['wrong'][wrong] in text and first['explanation'] in text,
    'wrong answer has no curriculum-grounded reason')
 ck(page.locator('#guidedV112BasicQuestion input[type=radio]').first.is_disabled(),
    'submitted answer should lock until retry')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==1,'answer not stored')
 ck(state()==start,'submitting question moved A/B or playback')
 page.locator('#guidedV112RetryBasic').click()
 ck(page.locator('#guidedV112FeedbackBasic').is_hidden(),'retry did not hide answer')
 ck(not page.locator('#guidedV112BasicQuestion input[type=radio]:checked').count(),
    'retry did not clear radio answer')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==0,
    'retry did not clear only chosen answer')
 ck(state()==start,'retry unexpectedly moved model')

 # Advanced mode reveals original PHASES and RATE source text exactly.
 page.locator('#guidedV112Level').select_option('advanced')
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='advanced',
    'advanced tier not selected')
 ck(page.locator('#guidedV112Advanced').is_visible(),
    'advanced detail disclosure unavailable')
 ck(page.locator('#guidedV112AdvancedQuestion').is_visible(),
    'advanced concept item not accessible')
 ck(page.locator('#guidedV112Advanced').evaluate('(el)=>!el.open'),
    'advanced full text forcibly expanded')
 page.locator('#guidedV112Advanced summary').click()
 ck(page.locator('#guidedV112FullCaution').is_visible(),
    'advanced limitations are not visible')
 for stage in stages:
    page.locator('#guidedV112Select').select_option(stage)
    for field,source_field in [('Electrical','electrical'),
       ('Hemodynamics','hemodynamics'),('Volume','volume'),
       ('Nursing','nursing'),('Caution','caution'),('Comparison','comparison')]:
       text=page.locator('#guidedV112Full'+field).inner_text()
       original=page.evaluate("(args)=>CardiacLearning.getStageNarrative(args[0])[args[1]]",
          [stage,source_field])
       ck(text==original,f'original clinical source mutated: {stage}:{field}')
    ck(page.locator('#guidedV112FullCaution').inner_text()!='',
       'stage scientific caveat missing')
    ck(page.locator('#guidedV112AdvancedQuestion').is_visible(),
       'advanced second item not present')
 ck('EF' in page.locator('#guidedV112Limits').text_content(),
    'normalized model caution removed')
 ck(state()['timeline']>=len(stages)-1,'guided stage navigation failed to seek')
 page.screenshot(path=str(SHOT/'03-advanced-open-desktop.png'),
    full_page=True,animations='disabled')

 # Every stage: submit basic and advanced with DOCUMENTED correct responses.
 # Switching stages and difficulty must preserve in-session answers.
 for i,stage in enumerate(stages):
    page.locator('#guidedV112Select').select_option(stage)
    for level in keys:
       suffix='Basic' if level=='basic' else 'Advanced'
       card=page.locator('#guidedV112'+suffix+'Question')
       options=card.locator('input[type=radio]')
       question=bank[stage][keys.index(level)]
       ck(page.locator('#guidedV112Prompt'+suffix).inner_text()!='',
          'question missing for '+stage+level)
       ck(options.count()==3,'must have 3 radio options')
       correct=question['correct']
       ck(page.locator('#guidedV112Feedback'+suffix).is_hidden(),
          'unanswered item leaked feedback: '+stage+level)
       options.nth(correct).check()
       ck(page.locator('#guidedV112Feedback'+suffix).is_hidden(),
          'correctness revealed upon selection')
       submissionBefore=state()
       page.locator('#guidedV112Submit'+suffix).click()
       ck(page.locator('#guidedV112Feedback'+suffix).get_attribute('data-result')=='correct',
          'documented correct choice rejected: '+stage+level)
       ck(question['explanation'] in page.locator('#guidedV112Feedback'+suffix).inner_text(),
          'correctness feedback lacked source reason')
       ck(card.locator('input:checked').count()==1,
          'submitted choice lost after grading')
       ck(state()['timeline']==submissionBefore['timeline'],
          'answer submission triggered original Timeline input')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==10,
    'all 10 stages / tiers not retained')
 ck(not state()['playing'] and state()['a']>0,
    'guided observation was lost during questions')
 ck(state()['hr']==start['hr'] and state()['view']==start['view'],
    'quiz changed HR or view')

 # Switch between tiers and phases; status persists and quiz is NOT a
 # clinical certification score. Reset of the cardiac model is separate.
 page.locator('#guidedV112Level').select_option('basic')
 ck(page.locator('#guidedV112Advanced').is_hidden(),
    'full explanatory detail leaked in basic tier')
 ck(page.locator('#guidedV112AdvancedQuestion').is_hidden(),
    'advanced question leaked to basic tier')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==10,
    'tier switch destroyed answered state')
 page.locator('#guidedV112Select').select_option('atrial_systole')
 ck(page.locator('#guidedV112FeedbackBasic').get_attribute('data-result')=='correct',
    'earlier submitted response lost on revisit')
 page.locator('#guidedV112Level').select_option('advanced')
 ck(page.locator('#guidedV112FeedbackAdvanced').get_attribute('data-result')=='correct',
    'advanced earlier answer lost')
 page.locator('#guidedV112RetryAdvanced').click()
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==9,
    'retry must reset one question only')
 ck(page.locator('#guidedV112FeedbackBasic').get_attribute('data-result')=='correct',
    'retry advanced should not reset basic')
 page.locator('#resetBtn').click()
 ck(page.evaluate('CardiacDashboard.isReady'),'original Reset broken')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==9,
    'simulation Reset silently erased learning progress')
 ck(page.locator('#guidedV112Level').input_value()=='advanced',
    'simulation Reset changed selected difficulty')
 page.locator('#guidedV112Toggle').click()
 ck(page.locator('.dashboard-clinical').is_visible(),
    'close guide did not restore original clinical summary')
 page.locator('#guidedV112Toggle').click()
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==9,
    'closing/opening teaching lost in-memory answers')
 ck(page.locator('#wiggersDeepDive').count()==1,
    'original six-part education lost')

 # All active player controls work; quiz form never pauses a running sim.
 page.locator('#pauseBtn').click()
 page.locator('#playBtn').click()
 page.wait_for_timeout(120)
 ck(page.evaluate('heartState.playing'),'Play unavailable')
 page.locator('#guidedV112Level').select_option('basic')
 page.locator('#guidedV112Quiz summary').click() if not page.locator('#guidedV112Quiz').evaluate('(el)=>el.open') else None
 ck(page.evaluate('heartState.playing'),'level selection paused playback')
 page.locator('#guidedV112Select').select_option('isovolumetric_contraction')
 ck(not page.evaluate('heartState.playing'),'guided step must pause playback')
 beforeRepeat=page.evaluate('window.__quizTimelineInputs')
 page.locator('#guidedV112Seek').click()
 ck(not page.evaluate('heartState.playing'),
    'existing explicit Timeline seek failed to pause')
 ck(page.evaluate('window.__quizTimelineInputs')==beforeRepeat+1,
    'manual repeat should dispatch exactly one additional Timeline event')
 page.locator('#guidedV112ViewWiggers').click()
 ck(page.evaluate('CardiacDashboard.view')=='wiggers','Wiggers button broken')
 ck(page.locator('#wiggersChart').is_visible(),'Wiggers chart broken')
 ck(page.locator('#wiggersMarkers [data-event]').count()==4,
    'Wiggers clinical valve event overlay lost')
 page.locator('#electricalModeBtn').click()
 ck(page.locator('#ecgCanvas').is_visible(),'ECG unexpectedly hidden')

 # The advanced disclosure is deliberately hidden in basic mode.
 # Select advanced explicitly before testing its visual responsiveness.
 page.locator('#guidedV112Level').select_option('advanced')
 # No page-level horizontal overflow in original layouts + opened study.
 for width in (1440,1366,1024,768,390,360):
    page.set_viewport_size({'width':width,'height':800})
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       f'horizontal overflow on {width}px')
    ck(page.locator('#guidedV112Level').is_visible(),
       f'difficulty not visible at {width}px')
    ck(page.locator('#guidedV112Quiz').is_visible(),
       f'quiz not visible at {width}px')
    ck(page.locator('#guidedV112Advanced').is_visible(),
       f'deep detail not accessible at {width}px')
    if width==390:
       page.screenshot(path=str(SHOT/'04-mobile-quiz-390.png'),
                       full_page=True,animations='disabled')
    page.locator('#guidedV112Toggle').click()
    ck(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),
       f'closed layout overflow at {width}px')
    page.locator('#guidedV112Toggle').click()

 # Learning answers are explicitly session-only: no localStorage/sessionStorage.
 ck(page.evaluate("""() => {
   return Object.keys(localStorage).filter(k=>k.includes('guided')).length===0 &&
          Object.keys(sessionStorage).filter(k=>k.includes('guided')).length===0;
 }"""),'guided questions unexpectedly persisted')
 page.reload(wait_until='load')
 page.wait_for_function('!!window.CardiacGuidedLearning')
 ck(page.evaluate('CardiacGuidedLearning.submittedAnswerCount')==0,
    'quiz answers unexpectedly persisted across a reload')
 ck(page.evaluate('CardiacGuidedLearning.detailLevel')=='basic',
    'new session must start with basic')
 ck(page.locator('#guidedV112Panel').is_hidden(),
    'new session must start closed')
 ck(not errors,'JavaScript errors: '+str(errors))
 print(f'PASS {n} v1.12 Patch3 checks: 10 source-aligned questions, '
       'advanced clinical text, no implicit A/B/HR/timeline effects.')
 browser.close()
