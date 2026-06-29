---
name: automation-ops-triage
description: "Google Apps Script, Google Workspace/GWS, Sheets/Docs/Drive/Gmail 자동화, Apps Script HTML Service, 내부 HTML 서비스, Illustrator/Adobe 스크립트, Monday 연동, 업무 자동화 코드에서 구두 제보·이상징후·오류·데이터 누락/중복·날짜/권한/파일 처리 문제를 티켓화하고 우선순위·영향범위·다음 확인 액션으로 정리한다."
---

# Automation Ops Triage

업무 자동화의 문제를 바로 고치지 말고 먼저 운영 티켓으로 정리한다. PR·GitHub 이슈가 없는 환경에서 구두 전달, Telegram 메모, 사용자가 직접 발견한 이상징후를 구조화한다.

## 대상 범위

- Google Apps Script, Google Workspace/GWS 자동화
- Google Sheets, Docs, Drive, Gmail, Calendar 연동
- Apps Script HTML Service, 내부 HTML 서비스, 웹 폼/관리 화면
- Illustrator/Adobe 스크립트, ExtendScript, UXP, 디자인 파일 자동화
- Monday, Drive, 외부 API, 파일 처리, CSV/Excel/PDF 변환 자동화

## 원칙

- 사용자가 개발자가 아니라도 운영자가 판단할 수 있게 설명한다.
- 구두 전달, Telegram 메모, “뭔가 이상함” 수준의 입력도 티켓으로 만든다.
- 원인은 추정하지 말고 `확인 필요`로 둔다.
- 코드 수정이 필요하면 `automation-change-safety`로 넘긴다.
- 장애/재발 방지 기록이 필요하면 `automation-incident-log`로 넘긴다.
- 단순 업무기록 입력 요청은 기존 Monday 업무기록 규칙과 구분한다.

## 티켓화 템플릿

```markdown
## 업무 자동화 유지보수 티켓

- 제목:
- 출처: 구두 / Telegram / 내가 발견 / 사용자 제보 / 로그
- 자동화 유형: Apps Script / GWS / HTML Service / Illustrator script / Monday / 기타
- 관련 파일/시트/문서/보드/서비스:
- 증상:
- 기대 동작:
- 실제 동작:
- 발생 시점:
- 최근 변경:
- 영향 범위:
- 긴급도: 즉시 / 오늘 중 / 나중에 / 기록만
- 확인 필요:
- 다음 액션:
```

## 우선순위 기준

### 즉시 대응

- 운영 자동화가 멈췄다.
- 데이터, 파일, 디자인 산출물이 계속 잘못 생성된다.
- 중복 생성, 누락, 잘못된 대상 입력/저장이 발생한다.
- 수동 복구 비용이 커진다.
- 권한, API, 트리거, 파일 경로, 템플릿 손상 가능성이 있다.

### 오늘 중 확인

- 특정 케이스에서만 값이나 결과물이 이상하다.
- 수동 보정은 가능하지만 반복될 수 있다.
- 날짜, 시간대, 컬럼명, 파일명, 레이어명, 템플릿 구조 오류가 의심된다.

### 기록만

- 개선 아이디어다.
- 빈도 낮은 불편이다.
- 구조 정리 후보지만 당장 장애는 아니다.

## 출력 형식

```markdown
## 결론
- 지금은 [즉시 대응/오늘 중 확인/기록만]으로 보입니다.

## 정리된 티켓
...

## 확인 질문
- 꼭 필요한 질문만 1~3개.

## 다음 액션
1. ...
2. ...
```

