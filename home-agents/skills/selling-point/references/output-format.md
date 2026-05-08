# 출력 포맷

기본 출력 순서를 지킨다.

1. 입력 자료 요약
2. 웹 보강 요약 (webEnrichment)
3. 분석 메모 (analysis)
4. 신뢰도 분해 (confidenceBreakdown)
5. 경쟁사 공통 표현 패턴
6. 우리 제품 차별화 기회
7. TOP 1, 2, 3 카드
8. 사진/일러스트 판단 보조 노트
9. 비주얼 브리프 (각 TOP 카드별, `visual-brief.md` 형식)
10. 구도 미리보기/이미지 생성 핸드오프
11. 평가 모드 보고서 (평가 모드일 때만)

## 1. 입력 자료 요약

```text
우리 제품:
- 제품명:
- 용도:
- 주요 기능:

경쟁사 자료:
- 경쟁사 A: 텍스트 N개, 이미지 N장, 메모 있음/없음
- 경쟁사 B:
- 경쟁사 C:
```

## 2. 웹 보강 요약 (webEnrichment)

웹 검색 도구가 있으면 기본 실행한다. 없으면 생략 사실을 쓴다.

```text
webEnrichment:
- status: executed / skipped / research-file-only
- searchQueries:
  - 
- sources:
  - title:
    url:
    usedFor: marketCommonClaims / marketCommonVisualPatterns / reviewPainPoints / purchaseConcerns
- marketCommonClaims:
  - 
- marketCommonVisualPatterns:
  - 
- reviewPainPoints:
  - 
- purchaseConcerns:
  - 
- webConfidence: high / medium / low
- limitation:
```

## 3. 분석 메모 (analysis)

`SKILL.md` 사고 순서 2단계의 결과를 기록한다.

```text
분석 메모

inputDataConfidence: high / medium / low

competitorMessageMap:
- 메시지: ..., 사용 경쟁사: [...], 우리 입장: 동일 / 약함 / 강함
- 

uniqueFeatures (우리만의 기능 또는 경쟁사가 거의 다루지 않는 기능):
- 

missingMandatoryElements (경쟁사 모두가 빠뜨렸으나 소비자 구매 판단에 필수인 정보):
- 

evidenceForScoring (점수 산정 근거 3문장):

```

## 4. 신뢰도 분해 (confidenceBreakdown)

```text
confidenceBreakdown:
- featureCoverage: high / medium / low
- competitorCoverage: high / medium / low
- visualCoverage: high / medium / low
- consumerCoverage: high / medium / low
- webCoverage: high / medium / low
- overallConfidence: high / medium / low
- confidenceReason:
```

## 5. 경쟁사 공통 표현 패턴

```text
경쟁사들이 공통으로 강조하는 기능:
- 

경쟁사들이 공통으로 사용하는 표현:
- 

경쟁사 표현의 약한 부분:
- 
```

## 6. 우리 제품 차별화 기회

```text
소비자 필수 전달 요소:
- 

우리 제품이 다르게 보여줄 수 있는 지점:
- 
```

## 7. TOP 카드 구조

각 TOP 카드에 다음 항목을 포함한다.

```text
TOP 1
셀링포인트:
역할:
근거 기능:
- 

추론한 소비자 문제:
- 

기능 묶기 근거:

경쟁사 공통 표현:
- 

소비자 필수 전달 요소:
- 

우리 제품 차별화 표현 전략:

우리 제품을 사야 하는 이유:

점수 (1-5점, scoring.md 통과 조건 매핑):
- 소비자 체감도:
- 메시지 차별성:
- 표현 차별성:
- 시각화 용이성:
- 증명력:
- 구매 영향도:
- 총점:

점수 근거 (체크리스트 조건 매핑 + analysis 데이터 인용 필수):
- 소비자 체감도:
- 메시지 차별성:
- 표현 차별성:
- 시각화 용이성:
- 증명력:
- 구매 영향도:

selfValidation:
- fitValidation:
  - featureEvidence: pass / weak / fail
  - consumerProblemFit: pass / weak / fail
  - competitiveFit: pass / weak / fail
  - purchaseFit: pass / weak / fail
  - visualProofFit: pass / weak / fail
  - fitReason:
- evidenceAudit:
  - scoringConditionMatched: yes / no
  - evidenceQuoted: yes / no
  - evidenceSources: product / competitor / visual / memo / research / web / inferred
  - unsupportedClaims:
    - 
  - auditAction: no-change / score-down / confidence-down / remove-candidate

selfReview: 수정 없음 / 또는 점수 조정 사실과 이유 1문장

추천 표현 형식:
- baseline: product_hero / lifestyle
- 주 표현:
- 보조 표현:
- 판단 이유:

추천 구도:
1.
2.
3.

피해야 할 표현:
- 

비주얼 브리프 (영문 8필드 + baseline prefix, visual-brief.md 형식 그대로):
```

## 8. 사진/일러스트 판단 보조 노트

사진이 적합한 경우:

- 실제 사용 장면 증명
- 결과물 비교
- 제품 질감/크기/핏
- 소비자가 "진짜 되나?"를 의심하는 기능

일러스트/도식이 적합한 경우:

- 내부 구조
- 치수/호환 범위
- 단계 설명
- 인증/스펙 정리
- 보이지 않는 원리

혼합이 적합한 경우:

- 실제 신뢰는 사진으로 주고, 정확한 정보는 도식으로 정리해야 할 때

예:

```text
대형폰 호환
- 주 표현: 실제 장착 사진 (product_hero)
- 보조 표현: 호환 범위/치수 도식
```

## 9. 비주얼 브리프 출력

`visual-brief.md`의 최종 출력 형식을 그대로 사용한다. 각 TOP 카드마다 1개의 비주얼 브리프를 출력한다. ChatGPT 웹 이미지 생성 등 외부 이미지 생성 환경에 복사해 사용할 수 있는 형태여야 한다.

## 10. 구도 미리보기/이미지 생성 핸드오프

로컬 Codex CLI 데몬 환경에서는 AI 이미지 자동 생성을 수행하지 않는다.

- TOP 카드별로 복사용 비주얼 브리프와 이미지 생성 프롬프트를 제공한다.
- 웹 UI가 SVG/HTML 구도 미리보기를 그릴 수 있도록 sceneType, medium, camera, composition, mustShow를 구조화한다.
- 사용자는 실제 이미지가 필요할 때 프롬프트를 ChatGPT 웹 이미지 생성 등 별도 이미지 생성 환경에 복사해 사용한다.
- 별도 과금이 발생할 수 있는 OpenAI API 키 기반 이미지 생성 스크립트는 기본 사용하지 않는다.
- 경쟁사 이미지의 레이아웃, 브랜드, 디자인을 복제하지 않는다.

## 11. 평가 모드 보고서

평가 모드(`expected.md` 존재 또는 사용자가 명시 요청)일 때 `evaluation.md`의 보고서 양식을 추가 출력한다.
