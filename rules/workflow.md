# 코딩 필수 워크플로우

코드를 작성하거나 수정할 때 **반드시** 아래 순서를 따른다.

1. **플랜 수립** — 작업 시작 전 반드시 계획을 먼저 작성한다.
   ```
   목표:
   수정할 파일:
   검증 방법:
   ```
2. **Read** — 대상 파일을 읽는다. 기존 구조·패턴·의존성을 확인한다.
3. **Edit** — 변경 범위를 최소화하여 수정한다.
4. **코드 작성** — 계획한 내용을 구현한다.
5. **/codex 검증** — 코드 작성 완료 후 `/codex`로 반드시 검증한다.

이 순서를 절대 건너뛰지 않는다.

---

# Superpowers + OMC 조율 워크플로우

작업 규모에 따라 아래 순서를 따른다.

### 소규모 (버그 수정, 간단한 수정)
```
Superpowers: systematic-debugging  →  직접 수정  →  verification-before-completion
```

### 중규모 (새 기능 추가)
```
Superpowers: brainstorming          →  요구사항 명확화
Superpowers: writing-plans          →  계획 수립
OMC: executor 에이전트              →  구현
Superpowers: verification-before-completion  →  완료 확인
```

### 대규모 (멀티파일, 아키텍처 변경)
```
Superpowers: brainstorming          →  아이디어 탐색
OMC: /oh-my-claudecode:ralplan      →  깊은 계획 수립
OMC: /oh-my-claudecode:ultrawork    →  병렬 구현
Superpowers: requesting-code-review →  리뷰
```

### 핵심 원칙
- **Superpowers 먼저** — 무엇을 할지 결정 (규율)
- **OMC는 실행 단계에서** — 복잡한 작업만 에이전트 위임
- **단순 작업에 OMC 남용 금지** — 에이전트 오버헤드가 더 클 수 있음
- **완료 주장 전 항상** `verification-before-completion` 실행
