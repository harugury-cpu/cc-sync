# spigen-slides — skill status checklist

## 1. 캔버스 / 경계
- [x] 720×405pt 기준
- [x] off-canvas 금지
- [x] 내용 영역 overflow 금지
- [x] 안 들어가면 폰트 축소보다 레이아웃 재계산 우선

## 2. 타입 스케일
- [x] 7pt 미만 금지
- [x] 단순 floor가 아니라 type scale remap 적용
- [x] 작은/중간 텍스트 계층 같이 상승
- [x] 현재 덱도 7pt 미만 0개 확인

## 3. 카드 내부 간격
- [x] outer padding > inner gap
- [x] title/body gap > body/body gap
- [x] tight 상태면 text group 재배치
- [x] small card는 balanced
- [x] 큰 대표 카드/구조 카드는 top-weighted 가능

## 4. 불렛 규칙
- [x] small card = bullet 금지
- [x] compact card = bullet 금지
- [x] wide text block only = native paragraph bullets 허용 가능
- [x] bullet/text 수동 정렬 방식 지양

## 5. flow 규칙
- [x] flow는 one-row 우선
- [x] step label / title / service multiline 대응
- [x] 카드 높이 자동 재계산
- [x] 글자 커지면 카드/간격도 같이 재계산
- [x] overflow 나면 카드 높이로 먼저 해결

## 6. structure 규칙
- [x] structure = diagram only
- [x] 카드 리스트 fallback 지양
- [x] native BENT connector 기본값 금지
- [x] 필요 시 orthogonal/manual routing
- [x] 최근 기준은 connector 최소화도 허용
- [x] 배치/그룹으로 구조 읽히게 하기

## 7. mapping 규칙
- [x] divider/bar/기준선은 카드 내부만 허용
- [x] 카드 밖 gutter 요소 금지
- [x] lane 내부 정렬 우선
- [x] nested box 금지

## 8. 강조 규칙
- [x] 페이지당 핵심 강조 1개 원칙
- [x] 100% 오렌지 카드 남발 금지
- [x] 일반 강조는 border / tint / orange text
- [x] 강조 row/card는 BRING_TO_FRONT
- [x] 주황 border가 다른 row에 가려지지 않게 처리

## 9. 레이아웃 복잡도
- [x] 3-up + 1-wide 같은 비대칭 혼합 레이아웃 지양
- [x] 같은 의미는 같은 비율 반복
- [x] 다른 의미는 다른 형태 사용
- [x] 박스 안에 박스 하나 더 넣는 방식 금지

## 10. 커버 정책
- [x] 표지는 고정 자산
- [x] 내지만 재생성/교체 가능
- [x] cover는 함부로 갈아엎지 않음

## 11. 실제 덱 검수 방식
- [x] 필요 시 썸네일 직접 추출해서 시각 검수
- [x] 말로 추정하지 않고 실제 화면 기준으로 확인
- [x] 현재 가이드 덱 기준 반복 수정 반영 중

## 한 줄 요약

spigen-slides는 이제 단순한 컴포넌트 모음이 아니라,
overflow / spacing / typography / emphasis / layout choice를 자동 판단하는 방향으로 상당 부분 스킬화된 상태다.
