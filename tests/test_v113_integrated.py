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
    ck(page.evaluate("CardiacClinicalCasesV113.validateCase(CardiacClinicalCasesV113.first).length===0"),"clinical schema invalid")
    ck(page.evaluate("CardiacClinicalV113.caseReviewStatus==='draft-human-review-pending'"),"unreviewed status wrong")
    ck(page.locator('#v113TabLearning').is_enabled(),"Learning should be usable")
    ck(page.locator('#v113TabClinical').is_disabled(),"unreviewed Clinical exposed publicly")
    ck(page.evaluate("heartState.physiologicalTime===0&&heartState.visualizationTime===0"),"Ready changed")
    page.locator('#v113TabLearning').click()
    ck(page.locator('#v113LearningScreen').is_visible(),"Learning missing")
    ck(page.locator('.v113-unit-button').count()==6,"six course units missing")
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
    page.close()

    # A preview-only fully functional Clinical session, isolated from simulator.
    page=browser.new_page(viewport={"width":1366,"height":900})
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((ROOT/"index.html").as_uri()+"?v113Preview=1")
    ck(page.locator('#v113TabClinical').is_enabled(),"Clinical preview gate missing")
    ck(page.evaluate("CardiacClinicalCasesV113.validateCase({...CardiacClinicalCasesV113.first,labs:[{...CardiacClinicalCasesV113.first.labs[0],status:'pending',value:0}]}).length>0"),
       "invalid lab zero/pending accepted")
    clk=page.evaluate("({a:heartState.physiologicalTime,b:heartState.visualizationTime,hr:heartRate})")
    page.locator('#v113TabClinical').click()
    page.get_by_role("button",name="가상 사례 시작").click()
    ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.index===0"),"case did not start")
    ck(page.get_by_text("결과 대기 중",exact=True).count()>=1,"pending lab not shown")
    ck(page.get_by_text("결과 확인 전",exact=False).count()>=1,"future lab not hidden")
    for idx in range(4):
        ck(page.evaluate("CardiacClinicalV113.sessionSnapshot.index")==idx,"wrong clinical phase")
        page.locator('.v113-choices input[type=radio]').nth(0 if idx==0 else 1 if idx in (1,3) else 2).check()
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

    for width in (320,360,390,768,900,1024,1366):
        page.set_viewport_size({"width":width,"height":900})
        page.locator('#v113TabLearning').click()
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           f"Learning overflow at {width}px")
        ck(page.locator('.v113-unit-button').count()==6,"unit links disappear on mobile")
        page.screenshot(path=str(SHOTS/f"learning-{width}.png"),full_page=True)
        page.locator('#v113TabClinical').click()
        ck(page.evaluate("document.documentElement.scrollWidth<=innerWidth+2"),
           f"Clinical overflow at {width}px")
        page.screenshot(path=str(SHOTS/f"clinical-{width}.png"),full_page=True)
    ck(not errors,"JavaScript runtime errors: "+str(errors))
    browser.close()
print(f"v1.13 integrated P2–P6: {checks} assertions passed")
