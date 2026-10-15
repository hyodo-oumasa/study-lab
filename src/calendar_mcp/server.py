"""MCP の決まりに従って、標準入力と標準出力でやり取りする部分。

1 行に 1 つの JSON-RPC のメッセージを読み、応答を 1 行で返す。
標準出力には MCP のメッセージ以外を書かない。記録は標準エラー出力に書く。
"""

import json
import sys
from collections.abc import Callable
from datetime import date
from typing import Any, TextIO

from calendar_mcp.calendar_source import Event, fetch_events

PROTOCOL_VERSION = "2025-06-18"
MAX_DAYS = 31

FetchEvents = Callable[[date, int], list[Event]]

LIST_EVENTS_TOOL = {
    "name": "list_events",
    "title": "予定の一覧",
    "description": (
        "macOS のカレンダーから、指定した日から指定した日数分の予定を読み、一覧で返す。"
        "予定の作成や変更はしない。"
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "start_date": {
                "type": "string",
                "description": "読み始める日。YYYY-MM-DD の形",
            },
            "days": {
                "type": "integer",
                "description": f"読む日数。1 から {MAX_DAYS} まで。省略すると 1",
                "minimum": 1,
                "maximum": MAX_DAYS,
            },
        },
        "required": ["start_date"],
        "additionalProperties": False,
    },
    "annotations": {"readOnlyHint": True},
}


def format_events(events: list[Event]) -> str:
    """予定の一覧を、Claude が読みやすい文章にする。"""
    if not events:
        return "予定はありません。"
    lines = []
    for e in events:
        when = "終日" if e.all_day else f"{e.start} 〜 {e.end}"
        lines.append(f"- {e.start[:10]} {when} {e.title}（{e.calendar}）")
    return "\n".join(lines)


def text_result(text: str, *, is_error: bool = False) -> dict[str, Any]:
    """tools/call の結果を、文章 1 つの形で作る。"""
    result: dict[str, Any] = {"content": [{"type": "text", "text": text}]}
    if is_error:
        result["isError"] = True
    return result


def call_list_events(arguments: dict[str, Any], fetch: FetchEvents) -> dict[str, Any]:
    """list_events ツールを実行して、tools/call の結果を作る。"""
    try:
        start = date.fromisoformat(arguments["start_date"])
        days = int(arguments.get("days", 1))
        if not 1 <= days <= MAX_DAYS:
            raise ValueError(f"days は 1 から {MAX_DAYS} までにしてください")
    except (KeyError, ValueError) as err:
        return text_result(f"入力が正しくありません：{err}", is_error=True)
    try:
        events = fetch(start, days)
    except RuntimeError as err:
        return text_result(f"カレンダーを読めませんでした：{err}", is_error=True)
    return text_result(format_events(events))


def error_response(msg_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def handle(message: dict[str, Any], fetch: FetchEvents) -> dict[str, Any] | None:
    """受け取ったメッセージ 1 つに対する応答を返す。通知には応答しない（None）。"""
    method = message.get("method")
    msg_id = message.get("id")
    if msg_id is None:
        return None

    if method == "initialize":
        result: dict[str, Any] = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "study-lab-calendar", "version": "0.1.0"},
            "instructions": "macOS のカレンダーの予定を読むためのサーバー。読み取りだけを行う。",
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [LIST_EVENTS_TOOL]}
    elif method == "tools/call":
        params = message.get("params") or {}
        if params.get("name") != "list_events":
            return error_response(msg_id, -32602, f"知らないツールです：{params.get('name')}")
        result = call_list_events(params.get("arguments") or {}, fetch)
    else:
        return error_response(msg_id, -32601, f"対応していないメソッドです：{method}")
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def serve(stdin: TextIO, stdout: TextIO, fetch: FetchEvents) -> None:
    """標準入力が閉じられるまで、1 行ずつ読んで応答する。"""
    for line in stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            print(f"JSON として読めない行を飛ばしました：{line[:80]!r}", file=sys.stderr)
            continue
        response = handle(message, fetch)
        if response is not None:
            stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            stdout.flush()


def main() -> None:
    serve(sys.stdin, sys.stdout, fetch_events)


if __name__ == "__main__":
    main()
