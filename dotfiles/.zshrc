export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export PATH="$HOME/.local/bin:$PATH"

# pnpm
export PNPM_HOME="/Users/harugury/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

# cokacdir - cd to last directory on exit
cokacdir() { command cokacdir "$@" && cd "$(cat ~/.cokacdir/lastdir 2>/dev/null || pwd)"; }

# cokacctl - cd to last directory on exit
cokacctl() { command cokacctl "$@" && cd "$(cat ~/.cokacctl/lastdir 2>/dev/null || pwd)"; }

# Memory Bank + Self-Evolving aliases
alias mb='~/.claude/memory-bank/venv/bin/python ~/.claude/memory-bank/mb.py'
alias se='~/.claude/memory-bank/venv/bin/python ~/.claude/self-evolving/se.py'
alias mbsearch='~/.claude/memory-bank/venv/bin/python ~/.claude/memory-bank/mb.py search'

# Browser-Use
export PATH="/Users/harugury/.browser-use-env/bin:/Users/harugury/.local/bin:$PATH"

# bun completions
[ -s "/Users/harugury/.bun/_bun" ] && source "/Users/harugury/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
 
# tofu-at: install Agent Teams orchestration into the current project
alias set-agent-team='bash ~/tools/tofu-at/install.sh'
export OPENCRAB_TOKEN="echo export OPENCRAB_TOKEN=토큰 >> ~/.zshrc
source ~/.zshrc"
