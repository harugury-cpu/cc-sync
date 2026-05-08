# 폴더형 입력 규칙

## 권장 폴더 구조

```text
project/
  product.md
  our-product/
    product-front.jpg
    product-detail.jpg
    product-use.jpg
  competitors/
    competitor-a/
      description.txt
      thumbnail.jpg
      detail-1.jpg
      detail-2.jpg
      memo.txt
    competitor-b/
      description.txt
      thumbnail.jpg
      detail-1.jpg
      memo.txt
  research/
    deep-research.md
    market-notes.md
```

## product.md 권장 양식

```text
제품명:

제품 용도:

주요 기능:
- 
- 
-

강조하고 싶은 사용 상황:

내부적으로 꼭 밀고 싶은 기능:
```

## 경쟁사 폴더 규칙

각 경쟁사 폴더에는 다음 자료가 있을 수 있다.

- `description.txt`: 상품 bullet, 상세페이지 문구, 리뷰 요약, 사용자가 복사한 텍스트
- `thumbnail.*`: 대표 이미지 또는 썸네일
- `detail-*.*`: 상세페이지 이미지, 비교표, 사용 장면, 스펙 이미지
- `memo.txt`: 사용자가 직접 관찰한 내용
- URL은 텍스트 파일 안에 있어도 직접 접속하지 말고 출처 기록으로만 사용한다.

## 리서치 폴더 규칙

`research/` 폴더가 있으면 웹 보강보다 우선순위가 높은 보조 근거로 사용한다.

- `deep-research.md`: ChatGPT Deep Research 또는 사람이 작성한 시장/경쟁사 리서치 보고서
- `market-notes.md`: 카테고리 공통 셀링포인트, 리뷰 불만, 시장 메모
- 기타 `.md` 또는 `.txt`: 보조 조사 자료

리서치 자료는 사용자 제공 경쟁사 자료와 구분해 “research-provided” 근거로 표시한다.

## 자료가 부족한 경우

- 제품 기능만 있으면 우리 제품 셀링포인트 중심으로 분석한다.
- 경쟁사 텍스트만 있으면 메시지 차별성 위주로 분석한다.
- 경쟁사 이미지만 있으면 표현 차별성 위주로 분석한다.
- 경쟁사 자료가 부족하면 결과에 “제공된 자료 기준”이라고 명시한다.
- 웹 검색 도구가 없고 research 폴더도 없으면 webCoverage를 low로 표시한다.
