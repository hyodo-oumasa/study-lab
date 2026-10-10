from datetime import UTC, datetime

from commit_stats.aggregate import count_by_day, count_by_week, local_timezone

JST = local_timezone(9)


def utc(year: int, month: int, day: int, hour: int = 0, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=UTC)


def test_count_by_day_uses_local_date():
    # UTC の 15:30 は、日本時間では翌日の 0:30 になる
    dates = [utc(2026, 10, 5, 14, 59), utc(2026, 10, 5, 15, 30)]

    assert count_by_day(dates, JST) == {"2026-10-05": 1, "2026-10-06": 1}


def test_count_by_day_is_sorted_by_date():
    dates = [utc(2026, 10, 7, 3), utc(2026, 10, 5, 3), utc(2026, 10, 6, 3), utc(2026, 10, 5, 4)]

    result = count_by_day(dates, JST)

    assert list(result.items()) == [("2026-10-05", 2), ("2026-10-06", 1), ("2026-10-07", 1)]


def test_count_by_week_starts_on_monday():
    # 2026-10-05 は月曜、2026-10-11 は日曜、2026-10-12 は次の月曜
    dates = [utc(2026, 10, 5, 3), utc(2026, 10, 11, 3), utc(2026, 10, 12, 3)]

    assert count_by_week(dates, JST) == {"2026-10-05": 2, "2026-10-12": 1}


def test_count_by_week_uses_local_date():
    # UTC では日曜の 15:30 だが、日本時間では月曜の 0:30 なので、次の週に入る
    dates = [utc(2026, 10, 11, 15, 30)]

    assert count_by_week(dates, JST) == {"2026-10-12": 1}


def test_empty_input():
    assert count_by_day([], JST) == {}
    assert count_by_week([], JST) == {}
