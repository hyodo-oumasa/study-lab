"""macOS のカレンダーのアプリから、予定を読む部分。

AppleScript（macOS に最初から入っている、アプリを操作するための言語）を
osascript コマンドで実行して、カレンダーのアプリに問い合わせる。
"""

import subprocess
from dataclasses import dataclass
from datetime import date

TIMEOUT_SECONDS = 60

# 指定した期間に重なる予定を、カレンダーごとに 1 行ずつ書き出す。
# 1 行の形：カレンダーの名前、件名、開始、終了、終日かどうか（タブ区切り）
APPLESCRIPT = """
on run argv
    set startDate to current date
    set day of startDate to 1
    set year of startDate to (item 1 of argv) as integer
    set month of startDate to (item 2 of argv) as integer
    set day of startDate to (item 3 of argv) as integer
    set time of startDate to 0
    set endDate to startDate + ((item 4 of argv) as integer) * days
    set output to {}
    tell application "Calendar"
        repeat with cal in calendars
            set calName to name of cal
            set evs to (every event of cal whose start date < endDate and end date > startDate)
            repeat with ev in evs
                set end of output to calName & tab & (summary of ev) & tab & ¬
                    ((start date of ev) as «class isot» as string) & tab & ¬
                    ((end date of ev) as «class isot» as string) & tab & ¬
                    ((allday event of ev) as string)
            end repeat
        end repeat
    end tell
    set AppleScript's text item delimiters to linefeed
    return output as string
end run
"""


@dataclass(frozen=True)
class Event:
    calendar: str
    title: str
    start: str
    end: str
    all_day: bool


def parse_output(text: str) -> list[Event]:
    """AppleScript の出力を、予定の一覧にする。開始の早い順に並べる。"""
    events = []
    for line in text.splitlines():
        if not line.strip():
            continue
        calendar, title, start, end, all_day = line.split("\t")
        events.append(Event(calendar, title, start, end, all_day == "true"))
    return sorted(events, key=lambda e: e.start)


def fetch_events(start: date, days: int) -> list[Event]:
    """start から days 日分の予定を、カレンダーのアプリから読む。"""
    args = [str(start.year), str(start.month), str(start.day), str(days)]
    try:
        completed = subprocess.run(
            ["osascript", "-", *args],
            input=APPLESCRIPT,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as err:
        raise RuntimeError(str(err)) from err
    if completed.returncode != 0:
        message = completed.stderr.strip() or f"osascript の終了コード {completed.returncode}"
        raise RuntimeError(message)
    return parse_output(completed.stdout)
