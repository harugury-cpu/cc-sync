# 골든 케이스 평가 모드

사용자가 "골든 케이스 평가", "정답 일치율"을 요청하거나, 입력 폴더에 `expected.md`(사람이 미리 정한 정답 셀링포인트)가 있으면 평가 모드를 활성화한다.

## 입력 구조

```text
case-01-product/
  case.md            # 사용자 작성 입력 자료
  product/           # 우리 제품 이미지
  competitors/       # 경쟁사 자료
  expected.md        # 사람이 정한 정답 (TOP 1, 2, 3 + 선정 이유)
```

`expected.md` 양식:

```markdown
## TOP 1
- 셀링포인트: 강력한 MagSafe 자력
- 선정 이유: 사용자 인터뷰에서 "자력이 약하다" 불만 1위
- 핵심 가시 요소: 자력 알림 링, 부착 순간, 흔들리지 않는 결과

## TOP 2
- 셀링포인트:
- 선정 이유:
- 핵심 가시 요소:

## TOP 3
- 셀링포인트:
- 선정 이유:
- 핵심 가시 요소:
```

## 평가 항목

### 1. TOP 일치율 (정량)

LLM이 뽑은 TOP 1, 2, 3과 사람이 정한 TOP 1, 2, 3을 비교한다.

- TOP 1 완전 일치: +40점
- TOP 1이 사람의 TOP 2 또는 TOP 3에 등장: +25점
- TOP 2 완전 일치: +30점, 부분 일치: +20점
- TOP 3 완전 일치: +20점, 부분 일치: +15점

최대 90점. 80점 이상 합격.

부분 일치 판정 기준: 사람이 정한 셀링포인트의 핵심 명사 또는 기능 키워드가 LLM 셀링포인트 타이틀 또는 strategy 안에 등장하는가.

### 2. scoreReasons 객관성 (정량)

LLM 출력의 scoreReasons 모든 reason 텍스트에서 객관 데이터 인용 단어를 카운트한다.

- 객관 단어 후보: "경쟁사 N개", "N점 조건", "uniqueFeatures", "competitorMessageMap", "missingMandatoryElements", "inputDataConfidence", "체크리스트", "analysis"
- 1개 이상 포함된 reason 비율을 측정한다.

판정:
- 50% 이상 합격
- 80% 이상 우수

### 3. 점수 분포 안정성 (정량, 선택 항목)

같은 입력으로 3회 분석을 실행한 후 6개 점수 항목별 표준편차를 계산한다.

- 표준편차 1.0 이하 합격
- 2.0 이상이면 직관 의존, 사고 순서 4단계 또는 selfReview 룰이 작동하지 않음. SKILL.md 사고 순서 섹션을 보강한다.

### 4. evidenceAudit 통과율 (정량)

각 TOP 카드의 evidenceAudit을 검사한다.

- scoringConditionMatched가 yes인 비율
- evidenceQuoted가 yes인 비율
- unsupportedClaims가 0개인 비율

판정:

- 80% 이상 합격
- 95% 이상 우수
- unsupportedClaims가 1개라도 있으면 해당 카드의 관련 점수 재검토

### 5. fitValidation 통과율 (정량)

각 TOP 카드에서 다음 5개 항목이 pass/weak/fail인지 집계한다.

- featureEvidence
- consumerProblemFit
- competitiveFit
- purchaseFit
- visualProofFit

판정:

- pass 4개 이상: strong
- pass 3개 + weak 2개 이하: acceptable
- fail 1개 이상: 재검토

TOP 1에 fail이 있으면 TOP 1 선정 자체를 재검토한다.

### 6. 이미지 5점 평가 (정성, 사용자 입력 필요)

사용자가 스킬이 만든 비주얼 브리프를 ChatGPT 웹 이미지 생성 등 별도 이미지 생성 환경에 복사해 생성한 후 다음 5개 항목을 1~5점 평가한다. 로컬 Codex CLI 데몬 환경에서는 AI 이미지 자동 생성을 수행하지 않으므로, 기본 평가는 비주얼 브리프와 구도 미리보기 기준으로 진행한다.

- 메시지 가독성: 이 이미지로 무얼 파는지 한눈에 읽히는가
- Must show 일치: visualBrief의 Must show 요소가 화면에 등장하는가
- Apple 톤 일치: baseline이 적용된 화이트백 또는 라이프스타일 톤이 살아 있는가
- 경쟁사 클리셰 회피: 어디서 본 듯한 평이한 컷이 아닌가
- 사용 가능성: 그대로 상세페이지에 사용 가능한가

합계 25점.

- 20점 이상: 사용 가능
- 15-19점: 가벼운 보정 후 사용
- 14점 이하: 비주얼 브리프 수정 필요

사용자가 점수만 알려주면 합산해 결과를 판정한다.

## 출력 보고서

평가 완료 후 다음 양식으로 보고한다.

```text
케이스: case-01-product
TOP 일치율: 75 / 90 (실패, 사용자의 TOP 2가 LLM TOP 3로 밀림)
scoreReasons 객관성: 16 / 18 (89%, 우수)
점수 분포 표준편차: 0.8 (합격)
evidenceAudit 통과율: 17 / 18 (94%, 합격)
fitValidation: TOP 1 strong, TOP 2 acceptable, TOP 3 재검토
이미지 5점 평가: (사용자 입력 대기)

가장 약한 부분:
- TOP 2/3 우선순위 역전 — messageDifferentiation 점수 산정에서 자력 강도가 충분히 반영되지 않음

다음 patch 후보:
- references/scoring.md 의 messageDifferentiation 5점 조건에 "정량 수치 차이 (자력, 무게, 두께 등)" 명시 추가
```

## 다중 케이스 일괄 평가

폴더에 case-01, case-02 ... 여러 케이스가 있고 사용자가 "전체 평가"를 요청하면 다음 순서로 진행한다.

1. 케이스 폴더 순회
2. 각 케이스 분석 → 평가 항목 1, 2, 3, 4, 5 측정
3. 케이스별 결과를 표 형태로 정리
4. 가장 약한 항목 (스킬 전체 평균이 낮은 항목)을 1개 짚고 patch 후보를 1줄 추천
