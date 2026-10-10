import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlparse

from commit_stats.cli import main


def fake_get_json(url: str, headers: dict[str, str]) -> list[dict]:
    """1 ページ目だけコミットを 3 件返す、偽の GitHub API。"""
    if parse_qs(urlparse(url).query)["page"] != ["1"]:
        return []
    return [
        {"commit": {"author": {"date": "2026-10-05T01:00:00Z"}}},
        {"commit": {"author": {"date": "2026-10-05T15:30:00Z"}}},
        {"commit": {"author": {"date": "2026-10-12T01:00:00Z"}}},
    ]


def run_main(tmp_path, *extra_args: str):
    output = tmp_path / "data" / "commit-stats.json"
    exit_code = main(
        ["--repo", "owner/name", "--output", str(output), *extra_args],
        get_json=fake_get_json,
        now=datetime(2026, 10, 12, 3, 0, tzinfo=UTC),
    )
    return exit_code, output


def test_writes_report_as_json(tmp_path):
    exit_code, output = run_main(tmp_path)

    assert exit_code == 0
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "generated_at": "2026-10-12T12:00:00+09:00",
        "utc_offset_hours": 9,
        "repositories": [
            {
                "name": "owner/name",
                "total": 3,
                "by_day": {"2026-10-05": 1, "2026-10-06": 1, "2026-10-12": 1},
                "by_week": {"2026-10-05": 2, "2026-10-12": 1},
            }
        ],
    }


def test_utc_offset_changes_the_date_boundary(tmp_path):
    _, output = run_main(tmp_path, "--utc-offset", "0")

    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["repositories"][0]["by_day"] == {"2026-10-05": 2, "2026-10-12": 1}


def test_output_file_is_the_same_on_every_os(tmp_path):
    _, output = run_main(tmp_path)

    raw = output.read_bytes()
    # Windows の改行コード（CR LF）が混ざらず、UTF-8 として読めること
    assert b"\r" not in raw
    assert raw.endswith(b"}\n")
    raw.decode("utf-8")


def test_help_works_when_default_encoding_cannot_show_japanese():
    # 日本語を扱えない文字コード（cp1252）が初期値になっている環境を再現する。
    # Windows の CI で、出力をファイルや別のプログラムに渡したときに起きる状況。
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}

    result = subprocess.run(
        [sys.executable, "-m", "commit_stats.cli", "--help"],
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert "集計するリポジトリ" in result.stdout.decode("utf-8")
