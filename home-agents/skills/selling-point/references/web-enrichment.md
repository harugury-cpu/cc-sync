# 기본 웹 보강 규칙

웹 검색 도구가 있는 환경에서는 기본적으로 webEnrichment를 수행한다. 웹 검색 도구가 없으면 생략 사실을 명시하고 사용자 제공 자료 기준으로만 분석한다.

## 우선순위

1. 사용자 제공 제품/경쟁사 자료
2. `research/deep-research.md` 또는 `research/*.md` 자료
3. 웹 검색 보강 자료
4. 모델 추론

사용자 제공 자료와 웹 보강 자료는 반드시 구분한다.

## 기본 검색 목표

- 카테고리 공통 셀링포인트 확인
- 경쟁사 공통 메시지 확인
- 경쟁사 공통 이미지 표현 패턴 확인
- 소비자 리뷰/불만/구매 전 걱정 포인트 확인
- 사용자가 제공한 경쟁사 2~3개가 시장 전체 패턴과 크게 다른지 확인

## 검색 쿼리 구성

제품명과 카테고리를 기준으로 3~5개 검색어를 만든다.

예:

```text
{category} common selling points
{category} product page features
{category} customer complaints reviews
{category} amazon reviews waterproof touch screen
{category} competitor product page images
```

한국 제품/국내 상세페이지가 중요한 경우 한국어 검색어도 병행한다.

```text
{카테고리} 상세페이지 셀링포인트
{카테고리} 리뷰 불만
{카테고리} 경쟁 제품 기능
```

## 사용 가능한 자료

- 제조사 공식 상세페이지
- Amazon 등 커머스 공개 상품 설명
- 공개 리뷰 요약
- 신뢰 가능한 리뷰 기사
- 카테고리 비교 글

## 사용 금지 또는 주의

- 로그인/결제/비공개 자료 접근 시도 금지
- 자동 크롤링이나 차단 우회 금지
- 경쟁사 이미지를 복제하기 위한 분석 금지
- 검색 snippet만 보고 단정 금지
- 웹 보강 자료를 사용자 제공 자료와 같은 신뢰도로 취급 금지

## 출력 규칙

webEnrichment에는 다음을 포함한다.

```text
status: executed / skipped / research-file-only
searchQueries:
sources:
marketCommonClaims:
marketCommonVisualPatterns:
reviewPainPoints:
purchaseConcerns:
webConfidence:
limitation:
```

## 신뢰도 라벨

- high: 공식/커머스/리뷰 등 서로 다른 출처 3개 이상에서 같은 패턴 확인
- medium: 출처 2개 이상에서 유사 패턴 확인
- low: 검색 결과 부족, snippet 중심, 또는 출처 1개 이하

웹 보강이 low면 messageDifferentiation과 expressionDifferentiation 점수를 올리는 근거로 단독 사용하지 않는다.

