---
name: memory-infra
description: Claude와 Codex가 같은 4-layer 메모리 인프라를 우선 사용해야 할 때 적용한다. 사용자의 성향, 프로젝트, 회고, 업무 맥락, 과거 세션 기억이 필요한 모든 대화에서 LanceDB, LLM Wiki, Graphify, Obsidian Vault를 같은 기준으로 참조한다. "기억", "메모리", "전에 말한", "회고", "Obsidian", "wiki", "graphify", "dump", "wrap-up" 문맥에서 사용한다.
---

# Memory Infra

Claude와 Codex가 같은 장기 기억을 보도록 하는 공통 4-layer 메모리 인프라 지침이다. 목표는 특정 봇/클라이언트에 기억이 갈라지지 않게 하고, 사용자의 성향·프로젝트·회고·도구 제약을 일관되게 이어받는 것이다.

## 4-Layer 구조

### Layer 4 — LanceDB 벡터 DB

의미 검색이 필요할 때 우선 사용한다.

```text
/Users/user/.claude/lancedb
```

현재 기본 테이블:

```text
memories
```

임베딩 모델:

```text
nomic-embed-text:latest
```

Ollama API:

```text
http://127.0.0.1:11434/api/embeddings
```

사용 기준:

- 사용자가 "전에", "예전에", "지난번", "그때 말한", "맥락 기억해?"처럼 과거 대화를 암시할 때
- 현재 요청이 사용자의 성향/프로젝트/반복 패턴에 의존할 때
- Wiki 요약만으로 부족할 때

### Layer 2 — LLM Wiki

대화 초반 또는 사용자 맥락 파악이 필요할 때 먼저 훑는다.

```text
/Users/user/.claude/wiki
```

핵심 파일:

- `INDEX.md`
- `성향_말투.md`
- `관심사_고민.md`
- `작업_프로젝트.md`
- `도구_환경.md`
- `보안_제약.md`

사용 기준:

- 사용자의 말투/선호/제약을 빠르게 파악해야 할 때
- 작업 전 기본 맥락을 잡을 때
- LanceDB 검색 전 큰 그림이 필요할 때

### Layer 1 — Graphify

문서/코드/프로젝트를 그래프 구조로 인덱싱하거나 관계 중심으로 이해해야 할 때 사용한다.

공통 스킬 경로:

```text
/Users/user/.agents/skills/graphify
```

사용 기준:

- 사용자가 `/graphify`를 요청할 때
- 문서/프로젝트/코드의 관계망을 보고 싶어 할 때
- `graphify-out/`이 있는 프로젝트를 질문할 때

### Layer 3 — Obsidian 연동

최종 기록과 회고 정리는 Obsidian Vault에 남긴다.

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault
```

Daily 회고:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/회고일기/Daily
```

업무 PDF 기준:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/0.work
```

사용 기준:

- 회고, 업무 기록, 성과, 프로젝트 상태, 사람/팀 맥락을 장기 보존할 때
- `dump` 또는 `wrap-up` 스킬이 발동될 때

## 기본 우선순위

맥락이 필요한 요청에서는 다음 순서로 판단한다.

1. **Wiki**: 사용자의 장기 요약을 먼저 확인
2. **LanceDB**: 구체적인 과거 세션/대화 맥락이 필요하면 의미 검색
3. **Graphify**: 관계 구조나 문서/코드 그래프가 필요하면 사용
4. **Obsidian**: 최종 기록·회고·성과·업무 메모는 Vault에 정리

## 작업 착수 전 3종 게이트

사용자가 수정, 구현, 자동화, 스케줄, 메모리 인프라, Obsidian 연동 변경을 요청하면 먼저 공통 `task-gate` 스킬을 적용한다.

```text
/Users/user/.agents/skills/task-gate
```

실행 전 반드시 제시할 것:

- 완료조건
- 실패케이스
- 검증방법

사용자가 승인한 뒤 실행하고, 작업 후에는 실제 검증 명령과 결과를 보고한다.

## Claude/Codex 공통 운영 규칙

- 공통 스킬 원본은 `~/.agents/skills/`에 둔다.
- Claude는 `~/.claude/skills/`에서 symlink로 공통 스킬을 참조한다.
- Codex는 `~/.agents/skills/`를 우선 참조한다.
- Claude 전용 스킬과 Codex 전용 스킬은 무리하게 통합하지 않는다.
- 4-layer 기억 인프라와 직접 관련된 스킬만 공유한다.

## 관련 공통 스킬

```text
/Users/user/.agents/skills/dump
/Users/user/.agents/skills/wrap-up
/Users/user/.agents/skills/graphify
/Users/user/.agents/skills/memory-infra
```

## 회고 세션 규칙

스케줄로 시작된 회고 세션에서는 다음을 기본으로 한다.

- 사용자의 모든 발화는 `dump` 스킬 기준으로 기록 후보로 본다.
- 사용자가 "정리해줘", "마무리", "랩업", "wrap up"이라고 하면 `wrap-up` 스킬을 실행한다.
- 오늘 업데이트된 PDF는 `/Users/user/Library/Mobile Documents/com~apple~CloudDocs/0.work` 기준 `.pdf`만 본다.
- 회고 최종 기록은 Obsidian Daily에 남긴다.

## 안전 규칙

- iCloud 경로는 직접 파일 도구보다 bash/Python 기반 접근을 우선한다.
- 사용자가 말하지 않은 내용을 확정해서 기록하지 않는다.
- 메모리 검색 결과는 "기억 후보"로 보고, 불확실하면 사용자에게 확인한다.
- 다른 채팅/다른 사용자 기록과 섞지 않는다.
