---
name: automation-incident-log
description: "Apps Script, GWS, HTML Service, Illustrator/Adobe 스크립트, Monday/Drive/Sheets/API 자동화 장애, 오류, 수동 복구, 데이터/파일/디자인 산출물 누락·중복·덮어쓰기, 구두 제보 해결, 수정 이력, 재발 방지 교훈을 Obsidian brain 또는 업무 노트에 기록해야 할 때 사용한다."
---

# Automation Incident Log

업무 자동화의 문제와 수정 이력을 Obsidian에 남긴다. 기억에 의존하지 않고 다음 유지보수 때 바로 이어갈 수 있게 한다.

## 기록 기준

다음 중 하나면 기록한다.

- 자동화가 멈췄다.
- 데이터, 파일, 디자인 산출물이 잘못 생성/누락/중복/덮어쓰기 됐다.
- 구두로 전달된 문제가 실제 수정으로 이어졌다.
- 수동 복구를 했다.
- 재발 방지 규칙이 생겼다.
- 코드, 시트, 컬럼, 문서, 폴더, 템플릿, 레이어, 트리거 구조를 바꿨다.

## 기본 기록 위치

- 반복 패턴: `brain/Patterns.md`
- 주의점/재발 방지: `brain/Gotchas.md`
- 다음 세션에 이어갈 맥락: `brain/Memories.md`
- 프로젝트별 운영 기록: 기존 `work/Project/` 또는 관련 업무 노트

새 노트보다 기존 노트 append를 우선한다.

## 기록 템플릿

```markdown
## YYYY-MM-DD — 업무 자동화 이슈

- 자동화:
- 유형: Apps Script / GWS / HTML Service / Illustrator script / Monday / 기타
- 증상:
- 원인:
- 영향:
- 조치:
- 검증:
- 재발 방지:
- 관련 파일/시트/문서/보드/서비스:
- 다음에 볼 것:
```

## 주의

- secret 원문, API 토큰, credential 값은 기록하지 않는다.
- 확인되지 않은 원인은 확정하지 않는다.
- 개인/팀 맥락과 실행 정책을 섞어 쓰지 않는다.
- 장애 기록은 비난이 아니라 재발 방지 중심으로 쓴다.

## 출력 형식

```markdown
## 기록 요약
- ...

## 업데이트한 노트
- ...

## 다음에 이어갈 맥락
- ...
```

