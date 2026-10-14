"""v1.13 integration regression: original Guided, course units, isolated case session."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/"preview-v113-integrated"
SHOTS.mkdir(exist_ok=True)
checks=0
def ck(cond,message):
    global checks
    assert cond,message
    checks+=1

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":1366,"height":900})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri())
    ck(page.evaluate("!!CardiacCourseV113&&!!CardiacClinicalV113"),"integration scripts missing")
    ck(page.evaluate("!!CardiacTermsV113"),"Korean student concept help missing")
    ck(page.get_by_role("button",name="전기 전도",exact=True).count()==1,"Korean conduction label missing")
    ck(page.get_by_role("button",name="심장 수축·판막",exact=True).count()==1,"Korean contraction label missing")
    ck(page.locator('#playBtn').inner_text().find("재생")>=0,"Play not localized")
    original_clocks=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    help_button=page.get_by_role("button",name="심전도 설명")
    help_button.click()
    ck(page.locator('#v113TermDialog').is_visible(),"ECG explanation dialog missing")
    ck(page.locator('#v113TermDialog h3').count()==4,"Student explanation needs 4 sections")
    ck(page.locator('#v113TermTitle').inner_text().startswith("심전도"),"wrong concept displayed")
    page.keyboard.press("Escape")
    ck(page.locator('#v113TermDialog').is_hidden(),"Escape did not close concept dialog")
    ck(help_button.evaluate("e=>document.activeElement===e"),"concept dialog did not restore focus")
    ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")==original_clocks,
       "concept pop-up unexpectedly seeks original A/B")
    page.locator('[data-term-help="wiggers"]').first.click()
    ck("위거스" in page.locator('#v113TermTitle').inner_text(),"Wiggers concept missing")
    ck("왜 중요한가요?" in page.locator('#v113TermBody').inner_text(),"importance section missing")
    page.get_by_role("button",name="용어 설명 닫기").click()
    ck(page.locator('#v113TermDialog').is_hidden(),"concept dialog close failed")

    ck(page.evaluate("CardiacClinicalCasesV113.validateCase(CardiacClinicalCasesV113.first).length===0"),"clinical schema invalid")
    ck(page.evaluate("CardiacClinicalV113.caseReviewStatus==='draft-human-review-pending'"),"unreviewed status wrong")
    ck(page.locator('#v113TabLearning').is_enabled(),"Learning should be usable")
    ck(page.locator('#v113TabClinical').is_disabled(),"unreviewed Clinical exposed publicly")
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),"Ready changed")
    page.locator('#v113TabLearning').click()
    ck(page.locator('#v113LearningScreen').is_visible(),"Learning missing")
    ck(page.locator('.v113-unit-button').count()==6,"six course units missing")
    ck(page.locator('.v113-course-layout>.v113-unit-picker').count()==1,
       "A1 desktop course outline missing")
    ck(page.locator('.v113-unit-picker').evaluate("e=>e.open"),
       "A1 desktop outline should be expanded")
    ck(page.locator('.v113-guide-host').evaluate("e=>e.parentElement.classList.contains('v113-course-content')"),
       "original Guide must share the chapter reading column")
    ck(page.evaluate("CardiacCourseV113.activeUnitId==='unit-cardiac-cycle'"),"default unit wrong")
    ck(not page.evaluate("CardiacGuidedLearning.open"),"navigation auto-started guide")
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),"Learning auto-seeked Ready")
    ck(page.locator('#guidedV112Toggle').is_visible(),"original Guided toggle not in Learning")
    ck(page.locator('#guidedV112Panel').count()==1,"original Guide cloned")
    for i in range(1,6):
        page.locator('.v113-unit-button').nth(i).click()
        ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),
           f"course unit {i} seeked")
        ck(page.evaluate("CardiacGuidedLearning.selectedStageId")=='atrial_systole',
           "course browsing changed Guide stage")
    page.locator('.v113-course-modes button').nth(1).click()
    ck(page.evaluate("CardiacCourseV113.mode==='free'"),"free exploration mode missing")
    page.locator('.v113-course-actions button').filter(has_text="이 단원 학습 완료 표시").first.click()
    ck(len(page.evaluate("CardiacCourseV113.completedUnitIds"))==1,"manual progress missing")
    page.locator('.v113-unit-button').first.click()
    ck(page.locator('#guidedV112Panel').is_hidden(),"Guide started from unit switch")
    page.locator('#guidedV112Toggle').click()
    ck(page.evaluate("CardiacGuidedLearning.open"),"explicit Guided entry failed")
    ck(page.locator('.v113-unit-title').evaluate("e=>e.tagName==='H3'"),
       "unit heading hierarchy should be h3")
    ck(page.locator('.v113-reading-block h4').count()>=1,
       "nested course sections should be h4")
    beforeCTA=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    page.get_by_role("button",name="5단계 심장주기 학습 시작 · 내용으로 이동").click()
    ck(page.evaluate("CardiacGuidedLearning.open"),"reopening CTA closed original Guided")
    ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")==beforeCTA,
       "already-open course CTA unexpectedly seeks")
    ck(page.evaluate("document.activeElement?.id==='guidedV112Title'"),
       "explicit course CTA should focus the study title")
    ck(page.evaluate("heartState.physiologicalTime>0"),"existing first Ready native seek broken")
    page.locator('#guidedV112Quiz summary').click()
    page.locator('#guidedV112BasicQuestion input[type=radio]').first.check()
    before=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    page.locator('#guidedV112SubmitBasic').click()
    ck(page.evaluate("CardiacGuidedLearning.submittedAnswerCount===1"),"original quiz submission lost")
    ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")==before,
       "question submission mutated clocks")
    page.locator('#v113TabSimulator').click()
    ck(page.locator('.dashboard-clinical').is_visible(),"Simulator Live Inspector hidden after Guide move")
    ck(page.evaluate("CardiacGuidedLearning.open"),"Guide state lost on return")
    ck(page.locator('#guidedV112Panel').is_hidden(),"invisible Guide overlaid live Inspector")
    ck(page.evaluate("CardiacCourseV113.completedUnitIds.length===1"),"course completion lost")
    page.locator('#resetBtn').click()
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),"original Reset failed")
    ck(page.evaluate("CardiacGuidedLearning.submittedAnswerCount===1"),"Reset cleared original quiz")
    ck(page.evaluate("CardiacCourseV113.completedUnitIds.length===1"),"Reset cleared course")
    page.locator('#v113TabLearning').click()
    ck(page.evaluate("CardiacGuidedLearning.open"),"Guide did not reopen in Learning")
    ck(page.locator('#guidedV112Panel').is_visible(),"original Guide rehost failure")
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),
       "return to Guided re-seeked after Reset")
    ck(page.evaluate("document.querySelectorAll('#guidedV112Panel').length===1"),"Guide duplicated")
    # A1 responsive chapter index is compact until the student opens it.
    page.set_viewport_size({"width":390,"height":850})
    page.wait_for_function("!document.querySelector('.v113-unit-picker').open")
    ck(page.locator('.v113-unit-title').is_visible(),
       "A1 mobile selected reading hidden behind index")
    page.locator('.v113-unit-picker>summary').click()
    ck(page.locator('.v113-unit-picker').evaluate("e=>e.open"),
       "mobile chapter index did not expand on request")
    previous=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")
    page.locator('.v113-unit-button').nth(2).click()
    ck(not page.locator('.v113-unit-picker').evaluate("e=>e.open"),
       "mobile selected chapter should return to compact index")
    ck(page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime})")==previous,
       "mobile chapter navigation touched A/B")
    ck(page.evaluate("CardiacGuidedLearning.submittedAnswerCount===1"),
       "reflow and mobile chapter change cleared original quiz")
    page.close()

    # A preview-only fully functional Clinical session, isolated from simulator.
    page=browser.new_page(viewport={"width":1366,"height":900})
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri()+"?v113Preview=1")
    ck(page.locator('#v113TabClinical').is_enabled(),"Clinical preview gate missing")
    ck(page.evaluate("CardiacClinicalCasesV113.validateCase({...CardiacClinicalCasesV113.first,labs:[{...CardiacClinicalCasesV113.first.labs[0],status:'pending',value:0}]}).length>0"),
       "invalid lab zero/pending accepted")
    ck(page.evaluate("CardiacClinicalCasesV113.validateCase({...CardiacClinicalCasesV113.first,labs:[{...CardiacClinicalCasesV113.first.labs[0],availableFromPhase:0},CardiacClinicalCasesV113.first.labs[1]]}).length>0"),
       "future lab result visible before availableAt was accepted")
    ck(page.evaluate("CardiacClinicalCasesV113.validateCase({...CardiacClinicalCasesV113.first,status:'clinical-reviewed'}).length>0"),
       "unapproved case accepted as clinically reviewed")
    clk=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,hr:heartRate})")
    page.locator('#v113TabClinical').click()
    page.get_by_role("button",name="가상 사례 시작").click()
    ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.index===0"),"case did not start")
    ck(page.locator('.v113-case-stage-layout>.v113-case-observations').count()==1,
       "E1 patient snapshot is not beside the current decision")
    ck(page.locator('.v113-case-stage-layout>.v113-case-card').count()==1,
       "E1 current decision is not in the study layout")
    ck(page.locator('.v113-case-observations .v113-vital').count()==2,
       "E1 snapshot must prioritize HR and BP")
    ck(page.locator('.v113-case-evidence').count()==1,
       "ECG/Lab disclosure is missing")
    ck(page.locator('.v113-case-complaint').is_visible(),
       "patient symptoms must remain visible before choosing an answer")
    ck(page.get_by_role("button",name="선택한 답안 제출").is_disabled(),
       "unanswered clinical quiz must not allow submit")
    page.get_by_role("button",name="같은 사례 다시 풀기").click()
    ck(page.locator('.v113-choices').count()==0,
       "destructive confirmation should temporarily isolate the quiz")
    ck(page.evaluate("document.activeElement?.closest('.v113-confirm')!==null"),
       "confirmation lost focus")
    page.get_by_role("button",name="취소").click()
    ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.index===0"),
       "cancelling confirmation changed session")
    ck(page.get_by_role("button",name="선택한 답안 제출").is_disabled(),
       "cancel left submit enabled with no answer")
    ck(page.get_by_text("결과 대기 중",exact=True).count()>=1,"pending lab not shown")
    ck(page.get_by_text("결과 확인 전",exact=False).count()>=1,"future lab not hidden")
    for idx in range(4):
        ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.index")==idx,"wrong clinical phase")
        if idx==3:
            ck(page.locator('.v113-case-observations').get_by_text("46 /min").count()==1,
               "E1 reassessment HR not visible in essential snapshot")
            ck(page.locator('.v113-case-observations').get_by_text("90/58 mmHg").count()==1,
               "E1 follow-up BP not visible in essential snapshot")
        page.locator('.v113-choices input[type=radio]').nth(0 if idx==0 else 1 if idx in (1,3) else 2).check()
        ck(page.get_by_role("button",name="선택한 답안 제출").is_enabled(),
           "submit failed to become enabled after choosing an answer")
        page.get_by_role("button",name="선택한 답안 제출").click()
        ck(page.locator('#v113ClinicalFeedback').is_visible(),"feedback unavailable")
        if idx==1:
            beforeSession=page.evaluate("CardiacClinicalV113.sessionSnapshot")
            page.get_by_role("button",name="관련 학습",exact=False).first.click()
            ck(page.evaluate("CardiacMainTabs.active==='learning'"),"wrong concept not linked to learning")
            ck(page.evaluate("CardiacCourseV113.returnContext?.source==='clinical'"),"return link missing")
            ck(page.evaluate("CardiacClinicalV113.sessionSnapshot")==beforeSession,"clinical session lost crossing to Learning")
            page.get_by_role("button",name="임상 문제로 돌아가기").click()
            ck(page.evaluate("CardiacMainTabs.active==='clinical'"),"return to clinical failed")
            ck(page.evaluate("CardiacClinicalV113.sessionSnapshot")==beforeSession,"clinical result changed after return")
        page.get_by_role("button",name=("결과·복습 보기" if idx==3 else "다음 단계")).click()
        ck(page.evaluate("document.activeElement?.classList.contains('v113-question-prompt') || !!document.activeElement?.closest('.v113-review-card')"),
           "next question/result should receive focus after view recreation")
    ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.status==='completed'"),"case did not complete")
    ck(page.locator('.v113-review-card').count()==4,"not all questions in review")
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),
       "clinical session touched A/B")
    ck(page.evaluate("heartRate===80"),"clinical patient HR mutated original simulator")
    page.locator('#v113TabSimulator').click()
    page.locator('#resetBtn').click()
    page.locator('#v113TabClinical').click()
    ck(page.locator('.v113-review-card').count()==4,"Simulator Reset cleared clinical")
    page.get_by_role("button",name="같은 사례 다시 풀기").click()
    ck(page.get_by_text("기록 초기화",exact=False).count()>=1,"explicit restart confirmation missing")
    page.get_by_role("button",name="취소").click()
    ck(page.locator('.v113-review-card').count()==4,"canceled restart lost answers")
    page.get_by_role("button",name="같은 사례 다시 풀기").click()
    page.get_by_role("button",name="확인 · 기록 초기화").click()
    ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.index===0"),"restart did not reset index")
    ck(page.evaluate("Object.keys(CardiacClinicalV113.sessionSnapshot.answers).length===0"),"restart retained answers")
    page.get_by_role("button",name="사례 종료 · 목록으로").click()
    page.get_by_role("button",name="확인 · 기록 초기화").click()
    ck(page.evaluate("CardiacClinicalV113.sessionSnapshot===null"),"explicit exit retained case")
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),
       "exit mutated A/B")

    page.get_by_role("button",name="가상 사례 시작").click()
    for width in (320,360,390,768,900,1024,1366):
        page.set_viewport_size({"width":width,"height":900})
        page.locator('#v113TabLearning').click()
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           f"Learning overflow at {width}px")
        ck(page.locator('.v113-unit-button').count()==6,"unit links disappear on mobile")
        ck(page.locator('.v113-unit-title').is_visible(),
           f"{width} active course reading missing")
        if width<=900:
            ck(not page.locator('.v113-unit-picker').evaluate("e=>e.open"),
               f"{width} mobile chapter index should initially be compact")
        page.screenshot(path=str(SHOTS/f"learning-{width}.png"),full_page=True)
        page.locator('#v113TabClinical').click()
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           f"Clinical overflow at {width}px")
        ck(page.locator('.v113-case-complaint').is_visible(),
           f"{width} critical patient information hidden")
        ck(page.locator('.v113-question-prompt').is_visible(),
           f"{width} current decision missing")
        if width<1000:
            ck(not page.locator('.v113-case-evidence').evaluate("e=>e.open"),
               f"{width} evidence should begin compact on mobile")
        page.screenshot(path=str(SHOTS/f"clinical-{width}.png"),full_page=True)
    ck(not errors,"JavaScript runtime errors: "+str(errors))
    browser.close()
print(f"v1.13 integrated P2–P6: {checks} assertions passed")
