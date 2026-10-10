"""コマンドとして実行する入口と、集計結果を JSON に書き出す部分。"""

import argparse
import io
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from commit_stats.aggregate import count_by_day, count_by_week, local_timezone
from commit_stats.fetch import GetJson, fetch_commit_dates, http_get_json


def build_report(
    repos: list[str],
    *,
    utc_offset_hours: float,
    token: str | None,
    get_json: GetJson,
    now: datetime,
) -> dict[str, Any]:
    """各リポジトリのコミットを取得して集計し、書き出す内容をまとめる。"""
    tz = local_timezone(utc_offset_hours)
    repositories = []
    for repo in repos:
        dates = fetch_commit_dates(repo, token=token, get_json=get_json)
        repositories.append(
            {
                "name": repo,
                "total": len(dates),
                "by_day": count_by_day(dates, tz),
                "by_week": count_by_week(dates, tz),
            }
        )
    return {
        "generated_at": now.astimezone(tz).isoformat(timespec="seconds"),
        "utc_offset_hours": utc_offset_hours,
        "repositories": repositories,
    }


def write_report(report: dict[str, Any], output: Path) -> None:
    """集計結果を JSON ファイルに書き出す。

    文字コードと改行コードを明示して、どの OS でも同じ内容のファイルになるようにする。
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    with output.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def use_utf8_output() -> None:
    """メッセージの出力に使う文字コードを UTF-8 に固定する。

    Windows では、出力先がファイルや別のプログラムの場合、文字コードの初期値が
    日本語を扱えないもの（cp1252 など）になっていることがあり、日本語の
    メッセージを出力するとエラーで止まる。
    """
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")


def main(
    argv: list[str] | None = None,
    *,
    get_json: GetJson = http_get_json,
    now: datetime | None = None,
) -> int:
    use_utf8_output()
    parser = argparse.ArgumentParser(
        prog="commit-stats",
        description="GitHub のコミット数を日ごと・週ごとに集計して JSON に書き出す。",
    )
    parser.add_argument(
        "--repo",
        action="append",
        required=True,
        metavar="OWNER/NAME",
        help="集計するリポジトリ。複数指定する場合は --repo を繰り返す。",
    )
    parser.add_argument("--output", type=Path, required=True, help="書き出す JSON ファイルのパス。")
    parser.add_argument(
        "--utc-offset",
        type=float,
        default=9,
        help="日付を区切るタイムゾーンの、UTC からの時差（時間）。既定値は日本時間の 9。",
    )
    args = parser.parse_args(argv)

    report = build_report(
        args.repo,
        utc_offset_hours=args.utc_offset,
        token=os.environ.get("GITHUB_TOKEN"),
        get_json=get_json,
        now=now or datetime.now(UTC),
    )
    write_report(report, args.output)
    print(f"{args.output} に {len(report['repositories'])} 件のリポジトリの集計を書き出しました。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
