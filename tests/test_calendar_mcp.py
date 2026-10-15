import io
import json
from datetime import date

from calendar_mcp.calendar_source import Event, parse_output
from calendar_mcp.server import handle, serve


def fake_fetch(start: date, days: int) -> list[Event]:
    """カレンダーの代わりに、決まった予定を返す。テストのときだけ使う代役。"""
    return [
        Event("個人", "歯医者", "2026-10-15T10:00:00", "2026-10-15T11:00:00", False),
        Event("個人", "旅行", "2026-10-16T00:00:00", "2026-10-17T00:00:00", True),
    ]


def failing_fetch(start: date, days: int) -> list[Event]:
    raise RuntimeError("許可されていません")


def test_initialize_returns_server_info():
    response = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, fake_fetch)
    assert response["result"]["protocolVersion"] == "2025-06-18"
    assert response["result"]["serverInfo"]["name"] == "study-lab-calendar"
    assert "tools" in response["result"]["capabilities"]


def test_notification_gets_no_response():
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}, fake_fetch) is None


def test_tools_list_has_one_read_only_tool():
    response = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, fake_fetch)
    tools = response["result"]["tools"]
    assert [t["name"] for t in tools] == ["list_events"]
    assert tools[0]["annotations"]["readOnlyHint"] is True


def call(arguments: dict, fetch=fake_fetch) -> dict:
    message = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "list_events", "arguments": arguments},
    }
    return handle(message, fetch)["result"]


def test_tools_call_lists_events():
    result = call({"start_date": "2026-10-15", "days": 2})
    text = result["content"][0]["text"]
    assert "isError" not in result
    assert "歯医者" in text
    assert "2026-10-16 終日 旅行（個人）" in text


def test_tools_call_rejects_bad_date():
    result = call({"start_date": "10/15"})
    assert result["isError"] is True


def test_tools_call_rejects_too_many_days():
    result = call({"start_date": "2026-10-15", "days": 32})
    assert result["isError"] is True


def test_tools_call_reports_calendar_error():
    result = call({"start_date": "2026-10-15"}, fetch=failing_fetch)
    assert result["isError"] is True
    assert "許可されていません" in result["content"][0]["text"]


def test_unknown_method_is_an_error():
    response = handle({"jsonrpc": "2.0", "id": 4, "method": "resources/list"}, fake_fetch)
    assert response["error"]["code"] == -32601


def test_serve_answers_one_line_per_request():
    stdin = io.StringIO(
        '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n'
        '{"jsonrpc":"2.0","method":"notifications/initialized"}\n'
        '{"jsonrpc":"2.0","id":2,"method":"tools/list"}\n'
    )
    stdout = io.StringIO()
    serve(stdin, stdout, fake_fetch)
    lines = stdout.getvalue().splitlines()
    assert [json.loads(line)["id"] for line in lines] == [1, 2]


def test_parse_output_sorts_by_start():
    text = (
        "個人\tB\t2026-10-15T13:00:00\t2026-10-15T14:00:00\tfalse\n"
        "個人\tA\t2026-10-15T09:00:00\t2026-10-15T10:00:00\tfalse\n"
    )
    assert [e.title for e in parse_output(text)] == ["A", "B"]
