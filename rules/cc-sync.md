# cc-sync 동기화 규칙

다음 파일/디렉토리를 변경한 후에는 **반드시** cc-sync에 push한다:

- `~/.claude/rules/`
- `~/.claude/CLAUDE.md`
- `~/.claude/settings.json`
- `~/.claude/agents/`
- `~/.claude/skills/`
- `~/.claude/commands/`

## push 절차

```bash
CCSYNC="경로/cc-sync-template"
# 변경된 파일을 cc-sync로 복사 후:
cd "$CCSYNC" && git add . && git commit -m "설정 동기화: [변경 내용]" && git push
```

push 전 `git pull`로 remote 변경사항 먼저 확인한다.
</thinking>
