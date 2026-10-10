"""コミットの日時を、日ごと・週ごとに数える（計算する部分）。"""

from collections import Counter
from datetime import datetime, timedelta, timezone


def local_timezone(utc_offset_hours: float) -> timezone:
    """UTC からの時差（時間）で表したタイムゾーンを返す。日本時間は 9。

    タイムゾーン名（"Asia/Tokyo" など）を使う方法もあるが、Windows には
    タイムゾーンのデータベースが入っておらず、追加の部品が必要になる。
    どの OS でも同じように動くよう、時差の数値で指定する。
    """
    return timezone(timedelta(hours=utc_offset_hours))


def count_by_day(dates: list[datetime], tz: timezone) -> dict[str, int]:
    """日ごとのコミット数を、日付（YYYY-MM-DD）の昇順で返す。"""
    counts = Counter(d.astimezone(tz).date().isoformat() for d in dates)
    return dict(sorted(counts.items()))


def count_by_week(dates: list[datetime], tz: timezone) -> dict[str, int]:
    """週ごとのコミット数を返す。週は月曜始まりで、キーはその週の月曜の日付。"""
    counts: Counter[str] = Counter()
    for d in dates:
        day = d.astimezone(tz).date()
        monday = day - timedelta(days=day.weekday())
        counts[monday.isoformat()] += 1
    return dict(sorted(counts.items()))
