#!/bin/bash

extract_commit_message() {
    local payload
    local command
    local message

    payload=$(cat)
    if [ -z "$payload" ]; then
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        command=$(printf '%s' "$payload" | jq -r '.tool_input.command // ""' 2>/dev/null)
    else
        command=$(printf '%s' "$payload" | /Users/harugury/.claude/memory-bank/venv/bin/python -c 'import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    raise SystemExit(0)
print(data.get("tool_input", {}).get("command", ""))' 2>/dev/null)
    fi

    case "$command" in
        git\ commit*|*/git\ commit*)
            ;;
        *)
            return 0
            ;;
    esac

    message=$(printf '%s\n' "$command" | /Users/harugury/.claude/memory-bank/venv/bin/python -c 'import re, shlex, subprocess, sys
command = sys.stdin.read().strip()
if not command:
    raise SystemExit(0)
try:
    args = shlex.split(command)
except ValueError:
    args = []
message = ""
for index, arg in enumerate(args):
    if arg == "-m" and index + 1 < len(args):
        message = args[index + 1]
        break
    match = re.match(r"^-m(.+)$", arg)
    if match:
        message = match.group(1)
        break
if not message:
    completed = subprocess.run(
        ["git", "log", "-1", "--format=%s"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        message = completed.stdout.strip()
print(message)' 2>/dev/null)

    printf '%s' "$message"
}

process_fix_commit() {
    local commit_message
    local extractor
    local result
    local status
    local rule_text

    commit_message=$1
    case "$commit_message" in
        fix:*|fix!:*)
            ;;
        *)
            return 0
            ;;
    esac

    extractor="$HOME/.claude/self-evolving/se_extractor.py"
    if [ ! -f "$extractor" ]; then
        return 0
    fi

    result=$(/Users/harugury/.claude/memory-bank/venv/bin/python - "$extractor" "$commit_message" <<'PY'
import importlib.util
import json
import pathlib
import sys

extractor_path = pathlib.Path(sys.argv[1]).expanduser()
commit_message = sys.argv[2]

spec = importlib.util.spec_from_file_location("se_extractor", extractor_path)
if spec is None or spec.loader is None:
    print(json.dumps({"ok": False}))
    raise SystemExit(0)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

rule = module.extract_rule_from_commit(commit_message)
if not rule:
    print(json.dumps({"ok": False}))
    raise SystemExit(0)

saved = bool(module.save_rule(rule))
print(json.dumps({"ok": saved, "rule_text": rule.get("rule_text", "")}, ensure_ascii=False))
PY
)

    if [ -z "$result" ]; then
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        status=$(printf '%s' "$result" | jq -r '.ok // false' 2>/dev/null)
        rule_text=$(printf '%s' "$result" | jq -r '.rule_text // ""' 2>/dev/null)
    else
        status=$(printf '%s' "$result" | /Users/harugury/.claude/memory-bank/venv/bin/python -c 'import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("False")
    raise SystemExit(0)
print(data.get("ok", False))' 2>/dev/null)
        rule_text=$(printf '%s' "$result" | /Users/harugury/.claude/memory-bank/venv/bin/python -c 'import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    raise SystemExit(0)
print(data.get("rule_text", ""))' 2>/dev/null)
    fi

    if [ "$status" = "true" ] || [ "$status" = "True" ]; then
        printf '✓ NEVER DO 규칙 자동 추가됨: %s\n' "$rule_text" >&2
    fi

    return 0
}

process_fix_commit "$(extract_commit_message)"
exit 0
