"""GitHub API からコミットの日時を取得する（通信する部分）。"""

import json
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import datetime
from typing import Any

API_ROOT = "https://api.github.com"
PER_PAGE = 100

# URL と HTTP ヘッダーを受け取り、JSON を読み込んだ結果を返す関数。
# テストでは、通信をしない偽の関数に差し替える。
GetJson = Callable[[str, dict[str, str]], Any]


def http_get_json(url: str, headers: dict[str, str]) -> Any:
    """GitHub API に GET リクエストを送り、応答の JSON を返す。"""
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_commit_dates(
    repo: str,
    *,
    since: datetime | None = None,
    token: str | None = None,
    get_json: GetJson = http_get_json,
) -> list[datetime]:
    """リポジトリ（"owner/name" 形式）のコミットの作成日時を、すべて取得する。

    GitHub API は 1 回の応答で最大 100 件までしか返さないため、
    ページを進めながら取得する。100 件より少ない応答が返ったら、
    それが最後のページなので、そこで終わる。
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "study-lab-commit-stats",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {"per_page": str(PER_PAGE)}
    if since is not None:
        params["since"] = since.isoformat()

    dates: list[datetime] = []
    page = 1
    while True:
        query = urllib.parse.urlencode({**params, "page": str(page)})
        commits = get_json(f"{API_ROOT}/repos/{repo}/commits?{query}", headers)
        dates.extend(datetime.fromisoformat(c["commit"]["author"]["date"]) for c in commits)
        if len(commits) < PER_PAGE:
            break
        page += 1
    return dates
