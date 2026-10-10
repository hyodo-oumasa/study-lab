# 通信するプログラムを、テストしやすく作る

このページでは、外部の API と通信する Python のプログラムを、テストしやすく、どの OS でも同じように動くように作る方法をまとめます。題材は、このサイト（study-lab）のために作った、GitHub のコミット数を集計するツールです。

このツールを検査する CI の仕組みについては、[Python のテストと lint を CI で自動実行する](./python-ci) で説明しています。

## 作ったツール

GitHub API（プログラムから GitHub の情報を取得する窓口）を使ってコミットの一覧を取得し、日ごと・週ごとの数を集計して、JSON ファイルに書き出します。Python の標準ライブラリだけで作っていて、外部の部品は使っていません。

```bash
commit-stats --repo hyodo-oumasa/study-lab --output data/commit-stats.json
```

書き出される JSON の例です。

```json
{
  "generated_at": "2026-10-10T09:44:25+09:00",
  "utc_offset_hours": 9,
  "repositories": [
    {
      "name": "hyodo-oumasa/study-lab",
      "total": 17,
      "by_day": {
        "2026-10-05": 2,
        "2026-10-06": 3,
        "2026-10-07": 7,
        "2026-10-08": 1,
        "2026-10-09": 4
      },
      "by_week": {
        "2026-10-05": 17
      }
    }
  ]
}
```

ファイルの構成は次のとおりです。

```text
src/commit_stats/
├─ fetch.py       ← GitHub API からコミットの日時を取得する（通信する部分）
├─ aggregate.py   ← 日ごと・週ごとに数える（計算する部分）
└─ cli.py         ← コマンドの入口と、JSON への書き出し
tests/
├─ test_fetch.py
├─ test_aggregate.py
└─ test_cli.py
```

## 「通信する部分」と「計算する部分」を分ける

このツールは、役割ごとに 3 つの部分に分けています。

| 部分 | 役割 | テストのしかた |
|---|---|---|
| 通信する部分 | GitHub API からコミットの一覧を受け取る | 本物の通信はせず、偽の応答を使ってテストする |
| 計算する部分 | 受け取った日時から、日ごと・週ごとの数を数える | 入力と期待する出力を用意して、そのままテストする |
| 書き出す部分 | 集計結果を JSON ファイルに保存する | 一時フォルダに書き出して、中身を確認する |

通信と計算が 1 つの関数に混ざっていると、計算が正しいかを確かめるだけでも、毎回 GitHub と通信する必要があります。分けておくと、次の利点があります。

- **テストが通信なしで動く。** CI が、通信エラーや GitHub API の利用回数の制限に左右されなくなります。
- **テストが速い。** このツールのテスト 15 件は、0.1 秒ほどで終わります。
- **結果が毎回同じになる。** 本物のリポジトリはコミットが増えていくので、本物を相手にすると、期待する結果を固定できません。

計算する部分は、日時の一覧を受け取って結果を返すだけの関数です。

```python
def count_by_day(dates: list[datetime], tz: timezone) -> dict[str, int]:
    """日ごとのコミット数を、日付（YYYY-MM-DD）の昇順で返す。"""
    counts = Counter(d.astimezone(tz).date().isoformat() for d in dates)
    return dict(sorted(counts.items()))
```

テストでは、境界になる入力を渡して確かめます。次の例は、「UTC（協定世界時）の 15:30 は、日本時間では翌日の 0:30 になる」ことを確かめています。

```python
def test_count_by_day_uses_local_date():
    dates = [utc(2026, 10, 5, 14, 59), utc(2026, 10, 5, 15, 30)]

    assert count_by_day(dates, JST) == {"2026-10-05": 1, "2026-10-06": 1}
```

## 通信を偽物に差し替える

通信する部分をテストするために、実際に通信する関数を、引数で差し替えられるようにしています。

```python
def fetch_commit_dates(
    repo: str,
    *,
    since: datetime | None = None,
    token: str | None = None,
    get_json: GetJson = http_get_json,
) -> list[datetime]:
```

`get_json` は、「URL とヘッダーを受け取り、応答の JSON を返す関数」です。何も指定しなければ、本物の通信をする `http_get_json` が使われます。テストでは、通信をしない偽の関数を渡します。

```python
class FakeApi:
    """通信をせずに、あらかじめ用意したページを順に返す偽の GitHub API。"""

    def __init__(self, pages: list[list[dict]]):
        self.pages = pages
        self.calls: list[tuple[str, dict[str, str]]] = []

    def __call__(self, url: str, headers: dict[str, str]) -> list[dict]:
        self.calls.append((url, headers))
        page = int(parse_qs(urlparse(url).query)["page"][0])
        return self.pages[page - 1] if page <= len(self.pages) else []
```

偽の関数は、呼び出された URL とヘッダーを記録しています。これにより、「正しい URL を呼んでいるか」「何回通信したか」「認証の情報を正しく送っているか」も確かめられます。

```python
def test_stops_at_a_page_with_fewer_items_than_the_limit():
    api = FakeApi([[commit("2026-10-05T01:00:00Z")] * 100, [commit("2026-10-06T01:00:00Z")]])

    dates = fetch_commit_dates("owner/name", get_json=api)

    assert len(dates) == 101
    assert len(api.calls) == 2
```

GitHub API は、1 回の応答で最大 100 件までしか返しません。このテストは、「101 件ある場合に、2 ページ目まで取得して、そこで終わる」ことを確かめています。

### 本物の API でも一度は確かめる

偽の API でのテストは、「自分が想定した応答」に対して正しく動くことしか確かめられません。想定そのものが間違っていないかは、本物を相手に一度実行して確かめます。このツールでは、本物の GitHub API で集計した合計が、`git` で数えたコミット数と一致することを確認しました。

## OS の違いで起きる問題と対処

3 つの OS で動かすために、次の 3 点に対処しました。

### 1. 文字コード：日本語を出力するとエラーになる場合がある

このツールは、使い方の説明（`--help`）や完了のメッセージを日本語で出力します。Windows では、出力先がファイルや別のプログラムの場合、文字コードの初期値が日本語を扱えないもの（cp1252 など）になっていることがあります。その状態で日本語を出力すると、`UnicodeEncodeError` というエラーで止まります。

対処として、出力に使う文字コードを UTF-8 に固定しています。

```python
def use_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")
```

ファイルを読み書きするときも、文字コードを省略せずに `encoding="utf-8"` と明示します。省略すると、OS ごとの初期値が使われ、OS によって結果が変わります。

### 2. 改行コード：OS によって違う

改行を表す文字は、Windows では CR LF（2 文字）、macOS と Linux では LF（1 文字）です。Python でファイルを書き出すとき、何も指定しないと、Windows では改行が自動的に CR LF に変換されます。同じデータから作ったファイルが、OS によって違う内容になってしまいます。

対処として、書き出すときに `newline="\n"` を指定し、どの OS でも LF にしています。

```python
with output.open("w", encoding="utf-8", newline="\n") as f:
    f.write(text)
```

### 3. タイムゾーンのデータ：Windows には入っていない

コミットの日時は UTC で返ってくるので、日本時間に直してから日付を数えます。Python には、`"Asia/Tokyo"` のような名前でタイムゾーンを指定する方法があります。ただし、この方法は OS に入っているタイムゾーンのデータベースを使います。Windows にはこのデータベースが入っていないため、追加の部品（`tzdata`）をインストールしないと動きません。

このツールでは、UTC からの時差（日本時間なら 9）を数値で指定する方法にしました。日本時間には夏時間がないので、これで足ります。外部の部品を増やさずに、どの OS でも同じように動きます。

```python
def local_timezone(utc_offset_hours: float) -> timezone:
    return timezone(timedelta(hours=utc_offset_hours))
```

夏時間がある地域のタイムゾーンを扱う場合は、時差が季節で変わるので、名前で指定する方法と `tzdata` が必要になります。

## テストが問題を検出できるかを確かめる

対処を入れたら、それを確かめるテストも書きます。たとえば、文字コードの対処には、次のテストを書きました。日本語を扱えない文字コードが初期値になっている環境を再現して、`--help` を実行しています。

```python
def test_help_works_when_default_encoding_cannot_show_japanese():
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}

    result = subprocess.run(
        [sys.executable, "-m", "commit_stats.cli", "--help"],
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert "集計するリポジトリ" in result.stdout.decode("utf-8")
```

環境を再現する形にしたので、このテストは Windows だけでなく、どの OS でも同じ問題を検出できます。

合格しているテストを見ても、「問題があるときに、本当に不合格になるのか」は分かりません。そこで、対処を入れない状態で同じ条件を再現し、実際にエラーになることを確かめました。

```bash
PYTHONIOENCODING=cp1252 python -c "print('集計するリポジトリ')"
```

```text
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-8: character maps to <undefined>
```

問題が起きることを確かめてから、対処を入れてテストが合格することを確認する。この順番で進めると、テストが意味のあるものになっているかが分かります。

## 手元での実行のしかた

手元では、仮想環境（プロジェクト専用の Python 環境）を作って実行します。仮想環境の名前は `venv` にしています。

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt -e .
ruff check .
ruff format --check .
pytest
```

**Windows（PowerShell）**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt -e .
ruff check .
ruff format --check .
pytest
```

CI と同じコマンドを手元で実行しておくと、PR を出す前に問題に気づけます。

### macOS で通信エラーになる場合

python.org からインストールした Python を macOS で使っていると、ツールを実行したときに、次のエラーになることがあります。

```text
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

通信相手を検証するための証明書の一覧が、Python に入っていないことが原因です。プログラムの誤りではありません。python.org が案内している対処は、Python と一緒にインストールされる `Install Certificates.command`（「アプリケーション」フォルダの Python のフォルダにあります）を一度実行することです。

一時的に確かめるだけなら、macOS に標準で入っている証明書を指定して実行する方法もあります。

```bash
SSL_CERT_FILE=/etc/ssl/cert.pem commit-stats --repo hyodo-oumasa/study-lab --output data/commit-stats.json
```

なお、CI のテストは通信をしないので、この問題の影響を受けません。

## AI と進める中で起きたことと、その対処

このツールとテストは、Claude Code と一緒に作りました。その中で起きたことと、その対処をまとめます。

| 起きたこと | 対処 |
|---|---|
| AI が書いたテスト用の偽の API に誤りがあり、テストが終わらなくなった。偽の API が「URL に `page=1` という文字の並びがあれば 1 ページ目」と判定していたため、必ず含まれる `per_page=100` にも反応し、どのページでもデータを返していた。プログラム本体ではなく、テストの側の誤りだった | AI が書いたテストも誤ることがある。テストが止まったり失敗したりしたら、本体とテストの両方を疑う。あわせて、本体側も「100 件より少ない応答が来たら終わる」ようにして、同じことが起きにくくした |
| 手元で実行したとき、通信エラーが出た。AI は、プログラムの誤りか、環境の問題かを切り分けてから報告した。原因は、手元の Python に証明書の設定がないことだった | エラーが出たら、すぐに直そうとさせず、原因がプログラムにあるのか、環境にあるのかを切り分けさせる |
| AI は「Windows で最初は失敗する可能性がある」と予告していたが、実際には失敗しなかった。実装中に問題の箇所を見つけて、先に対処とテストを入れていたため | 予告と結果が違ったときは、その理由を説明させる |

1 つ目の出来事は、文字の並びで判定するのではなく、URL を正しく分解して値を読み取るべきだった、という一般的な教訓でもあります。

## まとめ

- 通信する部分と計算する部分を分けると、通信なしで、速く、毎回同じ結果になるテストが書ける。
- 通信する関数を引数で差し替えられるようにしておくと、偽の API を使ってテストできる。
- 偽の API でのテストに加えて、本物の API でも一度は実行して、想定が正しいかを確かめる。
- OS の違いに備えて、文字コードと改行コードは明示する。タイムゾーンは、OS に入っているデータに頼らない方法を検討する。
- テストは、問題があるときに不合格になることを確かめてから信用する。
- AI が書いたテストも誤ることがある。止まったら、本体とテストの両方を疑う。
