# Hooks

- `post_bash_git_commit.sh`: `PostToolUse:Bash`에서 `git commit` 명령을 감지하고, `fix:` 또는 `fix!:` 커밋 메시지면 `~/.claude/self-evolving/se_extractor.py`를 호출해 NEVER DO 규칙을 자동 생성합니다.
