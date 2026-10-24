#!/bin/sh
# Claude Code の PostToolUse フックから呼ばれる。
# 時刻、使う場所、セッション、道具の名前、触れたファイルの場所（またはコマンドの文字）を、1 件 1 行で記録する。
# ファイルの中身や、コマンドの結果は記録しない。
jq -r --arg entry "${CLAUDE_CODE_ENTRYPOINT:-unknown}" '
  def oneline: tostring | gsub("\n"; " ⏎ ");
  [ (now | localtime | strftime("%Y-%m-%d %H:%M:%S")),
    $entry,
    ((.session_id // "") | .[0:8]),
    .tool_name,
    ( if .tool_name == "Bash" then (.tool_input.command // "")
      elif (.tool_name == "Grep" or .tool_name == "Glob")
        then ((.tool_input.path // ".") + "  " + (.tool_input.pattern // ""))
      else (.tool_input.file_path // "") end | oneline ),
    ( if .tool_input.description then "（" + (.tool_input.description | oneline) + "）" else empty end )
  ] | join("  ")
' >> "$HOME/.claude/tool-use.log"
