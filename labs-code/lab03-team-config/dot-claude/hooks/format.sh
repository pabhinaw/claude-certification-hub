#!/usr/bin/env bash
# PostToolUse hook: format the edited file. Exit 2 sends stderr back to Claude.
file=$(jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0
npx prettier --write "$file" >/dev/null 2>&1 || { echo "Prettier failed on $file" >&2; exit 2; }
exit 0
