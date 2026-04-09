---
name: gchat-security-check
description: Use when modifying any code in the gchat-bot project to verify no security issues were introduced
---

# gchat-bot 보안 체크

## 개요

코드 수정 후 보안 이슈를 점검하는 체크리스트. gchat-bot 프로젝트 전용.

## 체크리스트

수정된 파일에 대해 아래 항목을 **반드시** 확인한다.

### 1. 하드코딩 금지 확인
- [ ] 소스코드에 보안 코드명(제품명)이 직접 삽입되지 않았는가?
- [ ] 보안 관련 패턴은 `security_config.json`에만 존재하는가?
- [ ] `security_config.json`이 `.gitignore`에 등록되어 있는가?

### 2. 로그 출력 확인
- [ ] `logger.info` / `logger.debug`에 추출된 글자값(자재번호, 기기명, 원산지 등)이 찍히지 않는가?
- [ ] 민감 데이터가 Cloud Logging에 남지 않는가?
- [ ] `logger.warning` / `logger.error`는 에러 메시지만 포함하는가?

### 3. AI 프롬프트 확인
- [ ] Vertex AI / Gemini 프롬프트에 보안 코드명 예시가 없는가?
- [ ] 프롬프트는 위치/레이블 기반 설명만 사용하는가?

### 4. 인증 정보 확인
- [ ] `service_account.json`이 소스코드에 하드코딩되지 않았는가?
- [ ] API 키, 토큰 등이 코드에 직접 박히지 않았는가?
- [ ] 인증 정보는 환경변수로만 참조하는가?

### 5. 데이터 흐름 확인
- [ ] 새로 추가된 외부 API 호출이 있다면, 전송 데이터에 민감 정보가 포함되지 않는가?
- [ ] 이미지/텍스트를 외부로 보내는 경우 Vertex AI 경로를 통하는가?

## 판정

- 모든 항목 통과 → 수정 완료
- 하나라도 문제 → 즉시 수정 후 재확인
