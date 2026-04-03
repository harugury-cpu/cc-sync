# GPTaku Plugins

AI Native가 되고 싶은 사람들을 위한 Claude Code 플러그인 모음집.

AI Native란 AI를 단순히 도구로 쓰는 게 아니라, 기획부터 실행까지 AI를 자연스럽게 녹여내는 사람을 말합니다. 본인이 하는 일에 AI를 적용해 실질적인 성과를 만들려면, 결국 자기 자신이 먼저 AI Native해져야 합니다.

하지만 그 과정은 쉽지 않습니다. 개발 경험이 없는 사람에게는 하나하나가 새로운 벽이고, AI와 협업하는 방법 자체를 배워가야 합니다. 이 플러그인들은 그 과정에서 겪는 구체적인 어려움을 하나씩 해소해주기 위해 만들어지고 있습니다.

## Quick Start

### 1. 마켓플레이스 등록 (처음 한 번만)

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

### 2. 원하는 플러그인 설치

```
/plugin install
```

설치 가능한 플러그인 목록이 나오면 원하는 걸 선택하세요.
특정 플러그인을 바로 설치하려면 이름을 붙이면 됩니다:

```
/plugin install show-me-the-prd
```

> **한 번에 하나씩만 설치됩니다.** 여러 개를 설치하려면 하나씩 반복해주세요.

### 3. 업데이트

플러그인이 업데이트되면 아래 명령어로 최신 버전을 받을 수 있습니다:

```
/plugin update
```

> 설치/업데이트 후에는 Claude Code를 **재시작**하세요.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [docs-guide](https://github.com/fivetaku/docs-guide) | 공식문서 기반 정확한 답변 - 68개+ 라이브러리 지원, llms.txt 패턴 활용 |
| [git-teacher](https://github.com/fivetaku/git-teacher) | 비개발자를 위한 Git/GitHub 온보딩 - 클라우드 비유로 5단계 완성 |
| [vibe-sunsang](https://github.com/fivetaku/vibe-sunsang) | 바이브코더를 위한 AI 멘토 에이전트 - 대화 분석, 멘토링, 성장 리포트 |
| [deep-research](https://github.com/fivetaku/deep-research-kit) | AI 딥리서치 - 멀티에이전트 소스 검증, 7단계 파이프라인, 구조화된 리포트 생성 |
| [pumasi](https://github.com/fivetaku/pumasi) | 품앗이 - Claude가 PM, Codex CLI가 병렬 외주 개발자로 대규모 코딩 병렬 처리 |
| [show-me-the-prd](https://github.com/fivetaku/show-me-the-prd) | 쇼미더피알디 - 인터뷰 기반 PRD 생성, 한 문장에서 4종 디자인 문서까지 |
| [kkirikkiri](https://github.com/fivetaku/kkirikkiri) | 끼리끼리 - 자연어 한마디로 AI 에이전트 팀 자동 구성, 멀티 모델 지원 |
| [skillers-suda](https://github.com/fivetaku/skillers-suda) | 스킬러들의 수다 - 4명의 전문가가 수다 떨면서 바이브코더의 아이디어를 동작하는 스킬로 변환 |
| [nopal](https://github.com/fivetaku/nopal) | 노팔 - Google Workspace 8개 서비스를 자연어로 오케스트레이션, gws CLI 기반 자동화 |

> 플러그인은 계속 추가됩니다. Watch 해두시면 새 플러그인 알림을 받을 수 있습니다.

## Requirements

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** 전용 플러그인입니다
- Codex, Antigravity 등 다른 AI 코딩 도구는 지원하지 않습니다
- **Windows**: WSL2 위에서 Claude Code를 실행해야 합니다 (`wsl --install`)
- **macOS / Linux**: 바로 사용 가능

## Contributing

새로운 플러그인 아이디어나 개선 제안은 [Issues](https://github.com/fivetaku/gptaku_plugins/issues)에 남겨주세요.

## License

MIT
