# cc-sync 동기화 규칙

~/.claude의 CLAUDE.md·rules·skills·agents·commands·settings.json을 바꾸면 cc-sync에 push한다.

저장소(이 기기): ~/Library/Mobile Documents/com~apple~CloudDocs/0.work/cc-sync

## 절차
1. `git pull --ff-only` 먼저. 미커밋·충돌 있으면 stash 후 pull.
2. 변경 파일만 수동 복사. ⚠️ `sync.sh` 전체 실행은 rsync --delete 미러라 이 기기가 뒤처진 부분을 롤백시킬 수 있으니, 사전에 "repo에만 있고 홈엔 없는" 콘텐츠 손실 여부를 확인한 뒤에만 사용.
3. 복사 시 경로 정규화: `/Users/<현재유저>/` → `/Users/harugury/` (멀티머신 호환).
4. `git add <변경파일>` → commit(신원 Hagu <harugury@gmail.com>) → push.
