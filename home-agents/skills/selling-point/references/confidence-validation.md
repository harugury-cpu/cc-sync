# 신뢰도 및 적합도 검증

셀링포인트 제안의 신뢰성은 점수와 별도로 검증한다. 점수가 높아도 근거가 약하면 confidence를 낮춘다.

## confidenceBreakdown

각 항목을 high/medium/low로 평가한다.

### featureCoverage

- high: 제품명, 용도, 기능 목록, 핵심 스펙/수치가 충분함
- medium: 기능 목록은 있으나 용도나 수치가 부족함
- low: 기능이 추상적이거나 제품 용도를 알기 어려움

### competitorCoverage

- high: 경쟁사 3개 이상, 각 제품의 텍스트/이미지/메모 중 2종 이상 존재
- medium: 경쟁사 2개 이상 또는 텍스트/이미지 중 1종만 존재
- low: 경쟁사 1개 이하 또는 자료가 거의 없음

### visualCoverage

- high: 경쟁사 썸네일 + 상세 이미지/비교표/사용 장면이 충분함
- medium: 썸네일 또는 일부 상세 이미지만 있음
- low: 이미지 없음 또는 이미지 내용 식별 어려움

### consumerCoverage

- high: 리뷰/불만/사용자 메모/Deep Research에서 소비자 문제 근거가 있음
- medium: 사용 상황은 있으나 리뷰/불만 근거는 부족함
- low: 소비자 문제를 기능에서만 추론해야 함

### webCoverage

- high: 웹 보강 또는 Deep Research에서 출처 3개 이상 확인
- medium: 출처 2개 이하 또는 일부 카테고리 정보만 확인
- low: 웹 보강 미실행 또는 검색 결과 부족

### overallConfidence

- high: featureCoverage high + competitorCoverage medium 이상 + visualCoverage medium 이상 + consumerCoverage 또는 webCoverage medium 이상
- medium: featureCoverage medium 이상 + competitorCoverage 또는 webCoverage medium 이상
- low: featureCoverage low 또는 competitorCoverage/webCoverage 모두 low

overallConfidence가 low면 결과를 “확정 추천”이 아니라 “가설 추천”으로 표기한다.

## fitValidation

각 TOP 카드마다 pass/weak/fail로 검증한다.

### featureEvidence

- pass: 셀링포인트를 뒷받침하는 제품 기능이 명시되어 있음
- weak: 기능은 있으나 구체 수치/구조 설명이 부족함
- fail: 입력에 없는 기능을 셀링포인트로 사용함

### consumerProblemFit

- pass: 셀링포인트가 소비자 걱정/불편과 직접 연결됨
- weak: 소비자 문제는 추론 가능하나 근거가 약함
- fail: 소비자 문제가 불명확함

### competitiveFit

- pass: 사용자 제공 자료 또는 웹 보강에서 경쟁사 대비 차이/빈틈이 확인됨
- weak: 차이는 추론 가능하나 자료 근거가 부족함
- fail: 경쟁사와 동일하거나 차별 근거 없음

### purchaseFit

- pass: 구매 이유 또는 구매 불안 해소와 직접 연결됨
- weak: 보조 구매 이유에 가까움
- fail: 구매 결정과 연결 약함

### visualProofFit

- pass: 사진/일러스트/비교컷으로 증명 가능
- weak: 보조 설명이 필요함
- fail: 이미지로 증명하기 어려움

TOP 1에 fail이 하나라도 있으면 TOP 1 선정 자체를 재검토한다.

## evidenceAudit

각 TOP 카드와 각 scoreReason을 검사한다.

### 필수 항목

- scoringConditionMatched: scoring.md의 어떤 조건에 해당하는지 명시했는가
- evidenceQuoted: product/competitor/research/web/visual/memo 중 실제 근거를 인용했는가
- evidenceSources: 근거 출처 타입을 나열했는가
- unsupportedClaims: 입력에 없는 주장, 수치, 경쟁사 사실, 리뷰 불만을 만들지 않았는가
- auditAction: 문제가 있으면 score-down, confidence-down, remove-candidate 중 하나를 선택했는가

## unsupportedClaims 예시

- 입력에 없는 수치 사용
- 경쟁사 자료에 없는 “타사는 하지 않는다” 단정
- 리뷰가 없는데 “고객들이 불만을 가진다” 단정
- 이미지에 보이지 않는 상세 구조 단정
- Apple/Spigen/경쟁사 로고나 디자인 복제 지시

unsupportedClaims가 발견되면 해당 문장을 삭제하거나 “추론”으로 낮춰 표기하고, 관련 점수 또는 confidence를 하향한다.

