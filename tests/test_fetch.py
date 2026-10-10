from datetime import UTC, datetime
from urllib.parse import parse_qs, urlparse

from commit_stats.fetch import fetch_commit_dates


def commit(date: str) -> dict:
    """GitHub API が返すコミット 1 件分のうち、このツールが使う部分だけを作る。"""
    return {"commit": {"author": {"date": date}}}


class FakeApi:
    """通信をせずに、あらかじめ用意したページを順に返す偽の GitHub API。"""

    def __init__(self, pages: list[list[dict]]):
        self.pages = pages
        self.calls: list[tuple[str, dict[str, str]]] = []

    def __call__(self, url: str, headers: dict[str, str]) -> list[dict]:
        self.calls.append((url, headers))
        page = int(parse_qs(urlparse(url).query)["page"][0])
        return self.pages[page - 1] if page <= len(self.pages) else []


def test_parses_commit_dates():
    api = FakeApi([[commit("2026-10-05T01:00:00Z"), commit("2026-10-06T03:00:00+09:00")]])

    dates = fetch_commit_dates("owner/name", get_json=api)

    assert dates == [
        datetime(2026, 10, 5, 1, tzinfo=UTC),
        datetime(2026, 10, 5, 18, tzinfo=UTC),
    ]


def test_stops_at_a_page_with_fewer_items_than_the_limit():
    api = FakeApi([[commit("2026-10-05T01:00:00Z")] * 100, [commit("2026-10-06T01:00:00Z")]])

    dates = fetch_commit_dates("owner/name", get_json=api)

    assert len(dates) == 101
    assert len(api.calls) == 2


def test_stops_at_an_empty_page_when_the_last_page_is_full():
    # コミットがちょうど 100 件の場合、2 ページ目は空で返ってくる
    api = FakeApi([[commit("2026-10-05T01:00:00Z")] * 100])

    dates = fetch_commit_dates("owner/name", get_json=api)

    assert len(dates) == 100
    assert len(api.calls) == 2


def test_requests_the_repository_commits_endpoint():
    api = FakeApi([])

    fetch_commit_dates("owner/name", get_json=api)

    url = urlparse(api.calls[0][0])
    assert url.netloc == "api.github.com"
    assert url.path == "/repos/owner/name/commits"
    assert parse_qs(url.query) == {"per_page": ["100"], "page": ["1"]}


def test_sends_since_when_given():
    api = FakeApi([])

    fetch_commit_dates("owner/name", since=datetime(2026, 10, 1, tzinfo=UTC), get_json=api)

    query = parse_qs(urlparse(api.calls[0][0]).query)
    assert query["since"] == ["2026-10-01T00:00:00+00:00"]


def test_sends_token_only_when_given():
    without_token = FakeApi([])
    with_token = FakeApi([])

    fetch_commit_dates("owner/name", get_json=without_token)
    fetch_commit_dates("owner/name", token="dummy-token", get_json=with_token)

    assert "Authorization" not in without_token.calls[0][1]
    assert with_token.calls[0][1]["Authorization"] == "Bearer dummy-token"
