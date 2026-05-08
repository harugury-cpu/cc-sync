---
name: selling-point
description: 제품 기능과 경쟁사 자료를 기반으로 상세페이지용 셀링포인트 TOP 3, 점수 근거, 경쟁사 대비 차별화 표현 전략, 사진/일러스트/혼합 구도, 이미지 생성용 비주얼 브리프와 프롬프트를 설계한다. 사용자가 제품 기능, 상세페이지 이미지 전략, 경쟁사 분석, 셀링포인트 추출, 이미지 구도 추천, 상세페이지 컷 기획, 제품 이미지 프롬프트 생성, 구도 미리보기, 골든 케이스 평가 등을 요청할 때 사용한다.
---

# Selling Point

제품 기능과 경쟁사 자료 폴더를 분석해, 상세페이지에서 어떤 기능을 어떤 이미지 방식으로 보여줘야 하는지 결정한다. 결과는 TOP 3 셀링포인트와 외부 이미지 생성 환경에 복사해 사용할 수 있는 비주얼 브리프/프롬프트로 출력한다.

## 회사 컨텍스트

당사는 Apple 디바이스(iPhone, iPad, MacBook 등)용 케이스와 액세서리를 제조한다. 비주얼 브리프는 Apple 제품 페이지 톤을 따른다. 케이스에 장착된 Apple 디바이스가 결과 이미지에 자연스럽게 등장하는 것은 권장한다.

## 기본 원칙

- 소비자가 구매 판단에 필요한 필수 정보는 경쟁사와 겹쳐도 제거하지 않는다.
- 차별화는 메시지 제거가 아니라 구도, 증명 방식, 비교 방식, 정보 구조 개선으로 달성한다.
- 경쟁사 이미지는 분석용으로만 사용하고 복제하지 않는다.
- 셀링포인트에서 바로 프롬프트로 가지 말고, 반드시 분석 메모와 비주얼 브리프를 거친다.
- 사진/일러스트 중 하나만 고르지 말고, 필요하면 주 표현과 보조 표현으로 나눈다.
- 점수는 직관이 아니라 `references/scoring.md` 통과 조건에 매핑해서 산정한다.
- scoreReasons에는 일반론 금지. 분석 메모의 데이터를 인용한다.

## 사고 순서 (반드시 이 순서)

1. 입력 자료에서 patterns(공통 표현)과 gaps(차별화 기회)를 추출한다.
2. 웹 검색 도구가 있는 환경에서는 기본 webEnrichment를 수행한다. 없으면 생략 사실을 명시한다. Deep Research 파일이 있으면 웹 보강보다 우선 참고한다.
3. 분석 메모(analysis)를 작성한다 — competitorMessageMap, uniqueFeatures, missingMandatoryElements, inputDataConfidence, evidenceForScoring.
4. confidenceBreakdown을 작성한다 — featureCoverage, competitorCoverage, visualCoverage, consumerCoverage, webCoverage, overallConfidence.
5. 분석 메모를 인용해 sellingPoints의 점수와 scoreReasons를 1차 산정한다. 각 점수는 `references/scoring.md`의 정량 통과 조건에 매핑한다.
6. fitValidation과 evidenceAudit을 실행한다. 입력 근거가 약하거나 환각 가능성이 있으면 점수와 순위를 보수적으로 조정한다.
7. selfReview에서 점수 인플레이션·근거 부족을 점검한다. 위험을 발견하면 코멘트만 남기지 말고 점수와 scoreReasons를 실제로 수정한 뒤 최종 출력한다.

## 입력 방식

폴더형 입력을 우선한다. 사용자가 자료 폴더를 제공하면 먼저 `references/input-folder.md`를 읽고 자료 구조를 확인한다.

권장 구조:

```text
project/
  product.md
  our-product/
    *.jpg | *.png | *.webp
  competitors/
    competitor-a/
      description.txt
      thumbnail.*
      detail-*.*
      memo.txt
    competitor-b/
    competitor-c/
  expected.md          # (선택) 평가 모드 활성화용 정답 셀링포인트
```

채팅형 입력도 받을 수 있다. 이 경우 제품 기능 텍스트와 업로드된 이미지를 역할별로 분류한 뒤 같은 분석 절차를 적용한다.

## 작업 절차

1. **입력 자료 확인**
   - 제품명, 제품 용도, 기능 목록을 찾는다.
   - 우리 제품 이미지가 있으면 제품 형태/구조/사용 맥락을 파악한다.
   - 경쟁사별 텍스트, 썸네일, 상세 이미지, 메모를 분리한다.
   - `expected.md`가 있으면 평가 모드를 활성화한다.
   - `research/deep-research.md` 또는 `research/*.md`가 있으면 리서치 보강 자료로 분리한다.

2. **기본 웹 보강 (webEnrichment)**
   - 웹 검색 도구가 있는 환경에서는 `references/web-enrichment.md`에 따라 기본 웹 보강을 수행한다.
   - 제품 카테고리 공통 셀링포인트, 경쟁사 공통 표현, 소비자 리뷰/불만 키워드, 구매 전 걱정 포인트를 보강한다.
   - 웹 검색 도구가 없으면 webEnrichment를 생략하고 “웹 보강 미실행 — 사용자 제공 자료 기준”이라고 명시한다.
   - Deep Research 파일이 있으면 검색 결과보다 우선도가 높은 보조 근거로 사용한다.

3. **분석 메모 작성 (analysis)**
   - competitorMessageMap: 경쟁사 메시지를 매핑하고 우리 입장(동일/약함/강함)을 기록한다.
   - uniqueFeatures: 우리만의 기능 또는 경쟁사가 거의 다루지 않는 기능을 추출한다.
   - missingMandatoryElements: 경쟁사 모두가 빠뜨렸으나 소비자 구매 판단에 필수인 정보를 식별한다.
   - inputDataConfidence: `references/scoring.md`의 판정 게이트로 high/medium/low를 결정한다.
   - evidenceForScoring: 위 데이터를 기반으로 점수 산정 근거 3문장을 적는다.

4. **신뢰도 분해 (confidenceBreakdown)**
   - `references/confidence-validation.md`에 따라 featureCoverage, competitorCoverage, visualCoverage, consumerCoverage, webCoverage, overallConfidence를 산정한다.
   - overallConfidence가 low면 TOP 결과를 확정형이 아니라 “가설”로 표기한다.

5. **우리 제품 기능 분석**
   - 기능을 사용성, 결과 품질, 구조/안정성, 호환성, 신뢰 근거, 구매 불안 해소 등으로 분류한다.
   - 각 기능 뒤의 숨은 소비자 문제를 추론한다.
   - 비슷한 기능을 소비자 가치 기준으로 묶는다.

6. **셀링포인트 후보 생성**
   - 기능 묶음별로 소비자 관점 셀링포인트를 만든다.
   - 각 후보에 소비자 필수 전달 요소를 붙인다.
   - 경쟁사와 다르게 보여줄 표현 전략을 만든다.

7. **점수화 + 검증 + selfReview**
   - `references/scoring.md`의 1~5점 정량 통과 조건에 매핑해 6개 항목을 점수화한다.
   - 각 점수의 reason에는 체크리스트 조건 + 분석 메모 데이터를 인용한다.
   - `references/confidence-validation.md`에 따라 fitValidation과 evidenceAudit을 실행한다.
   - unsupportedClaims가 있으면 해당 셀링포인트의 관련 점수와 confidence를 하향한다.
   - selfReview를 실행한다 — inputDataConfidence가 medium/low면 messageDifferentiation과 expressionDifferentiation을 1점씩 하향. 평균 4.5 이상이면 가장 약한 항목을 1점 하향.
   - 위험을 발견하면 점수와 scoreReasons를 실제로 수정한다. selfReview 필드에 "수정 없음" 또는 "X점 → Y점으로 하향한 이유"를 기록한다.
   - 총점과 전략적 우선순위를 함께 고려해 TOP 1, 2, 3을 선정한다.

8. **이미지 표현 전략 + baseline 선택**
   - 각 TOP 카드별로 사진/일러스트/혼합 판단을 한다.
   - `references/baseline.md`에서 product_hero 또는 lifestyle 중 하나를 선택한다.
   - 주 표현과 보조 표현의 역할을 분리한다.
   - 추천 구도 2~3개와 피해야 할 표현을 제안한다.

9. **비주얼 브리프 작성 (8필드 영문)**
   - 각 TOP 카드마다 `references/visual-brief.md`의 8필드를 영문 1줄씩 작성한다.
   - baseline 텍스트를 prefix로 두고, ChatGPT 웹 이미지 생성 등 외부 이미지 생성 환경에 붙여넣기 쉬운 자연어 brief 형태로 출력한다.
   - 같은 셀링포인트에 baseline 2종을 동시에 출력하지 않는다.

10. **구도 미리보기/이미지 생성 핸드오프**
   - 로컬 Codex CLI 데몬 환경에서는 AI 이미지 자동 생성을 수행하지 않는다.
   - 별도 과금이 발생할 수 있는 OpenAI API 키 기반 이미지 생성 스크립트도 기본 사용하지 않는다.
   - 결과물은 비주얼 브리프, 복사용 프롬프트, 웹 UI에서 그릴 수 있는 SVG/HTML 구도 미리보기용 구조 정보까지 제공한다.
   - 사용자가 실제 이미지를 원하면 프롬프트를 ChatGPT 웹 이미지 생성 등 별도 환경에 복사해 사용한다.
   - 경쟁사 이미지의 레이아웃, 브랜드, 디자인을 복제하지 않는다.

11. **(평가 모드) 정답 일치율 측정**
   - `expected.md`가 있거나 사용자가 평가를 요청하면 `references/evaluation.md`의 보고서 양식으로 결과를 추가 출력한다.

## 출력 형식

`references/output-format.md`를 따른다. 출력은 다음 순서를 지킨다.

1. 입력 자료 요약
2. 웹 보강 요약 (webEnrichment)
3. 분석 메모 (analysis)
4. 신뢰도 분해 (confidenceBreakdown)
5. 경쟁사 공통 표현 패턴
6. 우리 제품 차별화 기회
7. TOP 1, 2, 3 카드 (점수, scoreReasons, fitValidation, evidenceAudit, selfReview, baseline 선택, 추천 구도, 피해야 할 표현 포함)
8. 사진/일러스트 판단 보조 노트
9. 비주얼 브리프 (각 TOP 카드별, baseline + 8필드 영문)
10. 구도 미리보기/이미지 생성 핸드오프
11. (평가 모드) 평가 보고서

## 결과 작성 규칙

- "경쟁사 분석 기준: 제공된 자료 기준"을 분석 메모에 명시한다.
- 추론과 실제 입력 근거를 구분한다.
- 경쟁사 자료가 부족하면 inputDataConfidence를 medium 또는 low로 떨어뜨리고 그 사실을 selfReview에 명시한다.
- 점수만 주지 말고 점수별 근거를 함께 쓴다. 일반론("구매로 직접 연결되는 핵심 기능이다") 금지.
- "무조건 다르게"가 아니라 "필수 정보 유지 + 표현 방식 차별화" 관점으로 제안한다.
- 크기/호환성은 사진과 도식 중 목적에 맞게 나눈다.
  - 체감 크기: 사진
  - 정확한 치수/호환 범위: 일러스트/도식
  - 실제 신뢰와 정보 전달이 모두 필요하면 혼합

## references 인덱스

| 파일 | 내용 |
|---|---|
| `references/input-folder.md` | 폴더형 입력 구조와 파일 규칙 |
| `references/scoring.md` | 점수 1~5점 정량 통과 조건 + inputDataConfidence 게이트 + selfReview 룰 |
| `references/baseline.md` | Apple 톤 product_hero / lifestyle baseline 2종 |
| `references/visual-brief.md` | 비주얼 브리프 8필드 작성 규칙 + scoreReasons 객관성 룰 |
| `references/output-format.md` | 출력 순서 9단계 + TOP 카드 양식 |
| `references/evaluation.md` | 골든 케이스 평가 모드 (TOP 일치율, 객관성, 안정성, 이미지 5점 평가) |
| `references/web-enrichment.md` | 기본 웹 보강 검색 절차, 출처 라벨, Deep Research 파일 처리 |
| `references/confidence-validation.md` | confidenceBreakdown, fitValidation, evidenceAudit, unsupportedClaims 검증 |
