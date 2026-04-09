# Superpowers + OMC 조율 워크플로우

### 소규모 (버그 수정, 간단한 수정)
```
Superpowers: systematic-debugging  →  직접 수정  →  verification-before-completion
```

### 중규모 (새 기능 추가)
```
Superpowers: brainstorming  →  writing-plans  →  OMC: executor  →  verification-before-completion
```

### 대규모 (멀티파일, 아키텍처 변경)
```
Superpowers: brainstorming  →  OMC: ralplan  →  OMC: ultrawork  →  requesting-code-review
```

- Superpowers 먼저 — 무엇을 할지 결정
- OMC는 실행 단계에서 — 복잡한 작업만 에이전트 위임
- 단순 작업에 OMC 남용 금지
- 완료 주장 전 항상 `verification-before-completion` 실행
