/*
 * v1.12 Patch 3: immutable qualitative questions transcribed from
 * V1.12_CLINICAL_CURRICULUM.md §3, 5 stages × basic/advanced.
 * All numerical LV values in questions are educational relative indexes.
 * This module contains no physiological equations, UI or timers.
 */
(function(root){
  'use strict';
  const raw=[
    ['atrial_systole',[
      ['P파가 직접 의미하는 것은?',
       ['심방 탈분극','승모판 폐쇄','실제 심방 박출량'],0,
       'P파는 전기적 사건인 심방 탈분극을 의미하며, 실제 심방 수축은 그 이후 나타납니다.',
       ['','승모판 폐쇄는 P파의 의미가 아니며 심실 수축 시작과 관련된 별도 기계적 사건입니다.','P파만으로 실제 심방 박출량을 측정할 수 없습니다.']],
      ['현 모델의 심방 수축 중 승모판 상태는?',
       ['닫힘','열림','반복 교대'],1,
       '이 모델의 심방 수축 단계에는 승모판이 열려 있어 추가 심실 충만이 일어납니다.',
       ['해당 모델에서 승모판은 열려 있으며, 폐쇄는 이후 등용적 수축 시작과 관련됩니다.','','이 단계의 판막 상태는 반복 교대로 표현되지 않습니다.']]
    ]],
    ['isovolumetric_contraction',[
      ['등용적 수축 중 일어나는 것은?',
       ['LV 압력 증가, 용적 일정','LV 압력 일정, 용적 감소','대동맥판 열림'],0,
       '두 판막이 닫혀 있으므로 좌심실 압력은 상승하지만 상대 용적은 일정합니다.',
       ['','등용적은 압력이 아니라 용적이 일정하다는 뜻입니다.','대동맥판이 열리는 것은 이어지는 박출 단계의 사건입니다.']],
      ['이 도식의 S1 대표 마커와 연결된 사건은?',
       ['승모판 폐쇄','대동맥판 폐쇄','승모판 개방'],0,
       '좌심계의 S1 대표 마커는 승모판 폐쇄입니다. 실제 S1에는 승모판·삼첨판 관련 사건이 포함됩니다.',
       ['','대동맥판 폐쇄는 S2 관련 좌심계 사건입니다.','승모판 개방은 심실 충만 시작과 연결됩니다.']]
    ]],
    ['ejection',[
      ['모델의 대동맥판이 열릴 때 상대 LV 용적의 방향은?',
       ['증가','감소','일정'],1,
       '대동맥판이 열려 혈액이 박출되는 단계에서 상대 LV 용적은 감소합니다. 실제 SV 또는 EF는 계산할 수 없습니다.',
       ['상대 LV 용적 증가가 아니라 박출에 따른 감소로 표현됩니다.','','용적이 일정한 구간은 등용적 단계입니다.']],
      ['T파가 끝나는 순간 대동맥판이 반드시 닫히는가?',
       ['그렇다','아니다','HR 80일 때만'],1,
       'ECG 재분극과 실제 판막 사건은 서로 다른 과정이며 동일한 순간이라고 단정할 수 없습니다.',
       ['T파 종료와 대동맥판 폐쇄 시각이 반드시 같지는 않습니다.','','특정 HR에서도 ECG 파형만으로 판막 폐쇄 시점을 확정할 수 없습니다.']]
    ]],
    ['isovolumetric_relaxation',[
      ['두 판막이 닫힌 이완 단계에서 모델 변화는?',
       ['압력 하강·용적 일정','압력 증가·용적 증가','대동맥판 개방'],0,
       '대동맥판 폐쇄 이후 승모판이 열리기 전까지 압력은 하강하고 상대 용적은 일정합니다.',
       ['','이 단계는 심실 압력이 상승하거나 용적이 증가하는 구간이 아닙니다.','대동맥판은 닫혀 있는 상태입니다.']],
      ['이 도식의 S2 대표 마커와 연결된 사건은?',
       ['승모판 폐쇄','대동맥판 폐쇄','심방 수축'],1,
       '이 좌심계 도식의 S2 대표 마커는 대동맥판 폐쇄입니다. 실제 S2에는 대동맥판·폐동맥판 폐쇄가 관련됩니다.',
       ['승모판 폐쇄는 S1에 대응하는 좌심계 사건입니다.','','심방 수축은 S2의 직접적인 판막 사건이 아닙니다.']]
    ]],
    ['filling',[
      ['승모판이 열린 후 좌심실 용적은 모델의 후반 충만 구간에서?',
       ['증가','감소','변하지 않음'],0,
       '모델 RR 후반 충만에서는 상대 LV 용적이 증가합니다. 단, RR 초반의 filling 구간은 0.88로 평탄합니다.',
       ['','모델 후반 충만에서는 상대 용적이 감소하지 않습니다.','모델 RR 초반과 달리 후반 충만에서는 상대 용적이 증가합니다.']],
      ['교육용 상대 LV 용적 0.88은 실제 무엇을 뜻하는가?',
       ['EF 88%','88 mL','단위 없는 교육용 지표'],2,
       '0.88은 단위 없는 상대 용적 지표일 뿐, 실제 mL·EF·박출량으로 환산할 수 없습니다.',
       ['상대 용적 0.88을 EF 88%로 해석할 수 없습니다.','상대 용적 0.88은 88 mL가 아닙니다.','']]
    ]]
  ];
  const levels=Object.freeze(['basic','advanced']);
  const mapping={};
  const letters=['A','B','C'];
  for(const [stage,questions] of raw){
    mapping[stage]=Object.freeze(questions.map(([prompt,options,correct,explanation,wrong],index)=>{
      if(options.length!==3||wrong.length!==3||correct<0||correct>2)
        throw new Error('Invalid question bank: '+stage);
      return Object.freeze({
        id:stage+'-'+levels[index],stage,level:levels[index],
        prompt,options:Object.freeze(options.map((text,i)=>letters[i]+'. '+text)),
        correctIndex:correct,explanation,
        wrong:Object.freeze(wrong.slice())
      });
    }));
  }
  root.CardiacGuidedQuestions=Object.freeze({
    levels,byStage:Object.freeze(mapping),
    get(stage,level){
      const index=levels.indexOf(level);
      return index>=0 ? mapping[stage]?.[index]||null : null;
    }
  });
})(window);
