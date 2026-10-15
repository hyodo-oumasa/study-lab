# MCP サーバーを自作する

[07. MCP とコネクター](./07-mcp-and-connectors) で、Claude に外部のサービスをつなぐ仕組みを見ました。コネクターの一覧には、多くのサービスが並んでいます。ところが、Mac に最初から入っている「カレンダー」のアプリにつなぐものは、見つかりませんでした。このページでは、ほしいものが一覧にないときの方法として、カレンダーの予定を読む MCP サーバーを、Python で自分で作り、Claude Code につなぎます。

## この記事で分かること

- 自分で MCP サーバーを作るときに、何を作ればよいか
- MCP サーバーが、Claude Code とどうやり取りしているか
- 作ったサーバーを、Claude Code につなぐ手順
- ターミナル版の Claude Code の入れ方
- 個人の情報を扱うサーバーを作るときに、気をつけること

## 用語の整理

| 用語 | 意味 |
|---|---|
| MCP サーバー（MCP server） | MCP の決まりに従って、Claude にツールを提供するプログラム（07 を参照） |
| stdio（標準入出力） | プログラムが、文字を受け取る口（標準入力）と、文字を出す口（標準出力）。自分の PC で動かす MCP サーバーは、この 2 つを使って Claude Code とやり取りする |
| JSON-RPC | 「何をしてほしいか」と「その結果」を、JSON という形式でやり取りする決まり。MCP は、これを使っている |
| AppleScript | macOS に最初から入っている、アプリを操作するための言語。`osascript` というコマンドで実行する |
| PATH | ターミナルが、入力されたコマンドを探しに行く場所の一覧 |

## 何を作るか

### 作るものの姿

作るのは、次の 1 つの道具（ツール）を持つ、小さなサーバーです。

| 項目 | 内容 |
|---|---|
| 道具の名前 | `list_events`（予定の一覧） |
| 受け取るもの | 読み始める日（例：`2026-10-01`）と、読む日数（1〜31 日） |
| 返すもの | その期間の予定の一覧（日付、時刻、件名、カレンダーの名前） |
| できないこと | 予定の作成、変更、削除 |

つなぐと、次のように変わります。

| | つなぐ前 | つないだ後 |
|---|---|---|
| 「10 月の予定を整理して」と頼む | 利用者が、カレンダーのアプリから予定を書き写して、会話に貼り付ける | Claude が、サーバーの道具を使って、予定を直接読む |

### 全体の流れ

```text
Claude Code ─(MCP のやり取り)─ 作ったサーバー ─(AppleScript)─ カレンダーのアプリ
```

- Claude が「予定の一覧」の道具を使うと、Claude Code が、サーバーに頼む。
- サーバーは、AppleScript で、カレンダーのアプリに問い合わせる。
- 結果を、Claude Code に返す。

すべて、この Mac の中で動きます。予定の中身が、サーバーを作った人や、ほかのサービスに送られることはありません。ただし、Claude が読んだ結果は、会話の一部として Anthropic に送られます（下の「個人の情報を扱うときに、気をつけること」を参照）。

### 決めたこと

| 決めたこと | 理由 |
|---|---|
| 道具は、読み取りだけの 1 つにする | 予定を作ったり消したりする道具があると、Claude が誤って使うおそれがある。最初は、できることを最小にする |
| 一度に読むのは、最大 31 日にする | 範囲が広いほど、時間がかかり、Claude に渡る情報も増える |
| Python に最初から入っている機能だけで書く | 追加の部品をインストールせずに済む。MCP のやり取りの中身も、目で見て分かる |

MCP サーバーを作るための部品（SDK）も公開されています。部品を使うと、やり取りの部分を自分で書かずに済みます。ここでは、仕組みを理解するために、やり取りの部分も自分で書きました。

## MCP サーバーの中身

### Claude Code とのやり取りの決まり

自分の PC で動かす MCP サーバーは、Claude Code が、プログラムとして起動します。やり取りは、標準入力と標準出力で行います。MCP の仕様には、次のように書かれています。

- メッセージは、1 行に 1 つずつ。メッセージの中に、改行を入れてはいけない。
- サーバーは、標準出力に、MCP のメッセージ以外を書いてはいけない。
- 記録（ログ）は、標準エラー出力に書いてよい。

2 つ目が、作るときに特に大切です。動作を確かめるつもりで `print()` を 1 行入れると、それが標準出力に出て、Claude Code が、壊れたメッセージとして受け取ってしまいます。

### 応答するメッセージ

このサーバーが応答するのは、07 で `curl` を使って見たのと同じ、次のメッセージです。

| メッセージ | 意味 | サーバーが返すもの |
|---|---|---|
| `initialize` | 接続の挨拶 | 対応している仕様の版、サーバーの名前、できること |
| `notifications/initialized` | 挨拶が済んだという知らせ | 何も返さない（知らせには応答しない決まり） |
| `tools/list` | 道具の一覧を教えて | `list_events` の名前、説明、入力の形 |
| `tools/call` | 道具を使って | 予定の一覧の文章 |

受け取ったメッセージを、種類ごとに振り分ける部分は、次のとおりです。

```python
def handle(message, fetch):
    method = message.get("method")
    msg_id = message.get("id")
    if msg_id is None:          # id がないものは「知らせ」なので、応答しない
        return None

    if method == "initialize":
        result = {
            "protocolVersion": "2025-06-18",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "study-lab-calendar", "version": "0.1.0"},
            "instructions": "macOS のカレンダーの予定を読むためのサーバー。読み取りだけを行う。",
        }
    elif method == "tools/list":
        result = {"tools": [LIST_EVENTS_TOOL]}
    elif method == "tools/call":
        result = call_list_events(message["params"]["arguments"], fetch)
    else:
        return error_response(msg_id, -32601, f"対応していないメソッドです：{method}")
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}
```

（実際のコードから、説明に必要な部分を抜き出しています。）

### 道具の説明

`tools/list` で返す道具の定義には、名前、説明、入力の形を書きます。Claude は、この説明を読んで、いつ、どんな入力で、この道具を使うかを決めます。[06. Skills](./06-skills) で、スキルの説明が大事だと書いたのと同じです。

```python
LIST_EVENTS_TOOL = {
    "name": "list_events",
    "description": "macOS のカレンダーから、指定した日から指定した日数分の予定を読み、一覧で返す。"
                   "予定の作成や変更はしない。",
    "inputSchema": {
        "type": "object",
        "properties": {
            "start_date": {"type": "string", "description": "読み始める日。YYYY-MM-DD の形"},
            "days": {"type": "integer", "description": "読む日数。1 から 31 まで。省略すると 1",
                     "minimum": 1, "maximum": 31},
        },
        "required": ["start_date"],
    },
    "annotations": {"readOnlyHint": True},
}
```

`annotations` の `readOnlyHint` は、「この道具は読むだけ」という目印です。

### カレンダーを読む部分

カレンダーのアプリへの問い合わせは、AppleScript で書き、Python から `osascript` コマンドで実行します。AppleScript の中で、それぞれのカレンダーについて、指定した期間に重なる予定を探し、1 件ずつ 1 行に書き出します。

```applescript
tell application "Calendar"
    repeat with cal in calendars
        set evs to (every event of cal whose start date < endDate and end date > startDate)
        -- 予定ごとに、カレンダーの名前、件名、開始、終了、終日かどうかを 1 行に書き出す
    end repeat
end tell
```

Python の側では、この出力を 1 行ずつ読み、開始の早い順に並べます。

## テストする

カレンダーを読む部分と、やり取りの部分を、別の関数に分けました。こうすると、本物のカレンダーを使わずに、やり取りの部分をテストできます。テストでは、カレンダーの代わりに、決まった予定を返す代役を使います。

```python
def fake_fetch(start, days):
    """カレンダーの代わりに、決まった予定を返す。テストのときだけ使う代役。"""
    return [
        Event("個人", "歯医者", "2026-10-15T10:00:00", "2026-10-15T11:00:00", False),
        Event("個人", "旅行", "2026-10-16T00:00:00", "2026-10-17T00:00:00", True),
    ]
```

テストは 10 件です。挨拶に正しく答えるか、知らせには応答しないか、道具の一覧に読み取り専用の道具が 1 つだけあるか、日付の誤りや 31 日を超える指定をはじくか、などを確かめています。テストは、このサイトの Python の CI（[Python のコードに CI を付ける](../cicd/python-ci)）で、変更のたびに実行されます。

## Claude Code につなぐ

### ターミナル版を入れる

サーバーをつなぐには、ターミナル版の Claude Code の `claude mcp add` コマンドを使います。[02. Claude Code を使う場所](./02-where-to-use) で見たとおり、デスクトップアプリを入れただけでは、ターミナルで `claude` コマンドは使えません。そこで、ターミナル版を入れました。

ターミナル版を入れた理由は、正しい場所に設定を書けることに加えて、**つながらないときに原因を調べるコマンドが使える**ことです。自分で作ったサーバーは、完成品と違い、つながらないことがあります。

| コマンド | 分かること |
|---|---|
| `claude mcp list` | それぞれのサーバーが、つながっているか |
| `claude mcp get <名前>` | つながらないときの、エラーの中身 |

入れ方は、公式ドキュメントにある、macOS 用の 1 行のコマンドです。Mac の「ターミナル」のアプリで実行します。

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

この Mac では、最後に、次の注意が表示されました。

```text
⚠ Setup notes:
  ● Native installation exists but ~/.local/bin is not in your PATH. Run:

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

ターミナル版は `~/.local/bin` に入りますが、その場所が PATH に入っていない、という意味です。表示されたコマンドを実行すると、シェルの設定ファイル（`~/.zshrc`）に 1 行が加わり、`claude` コマンドが使えるようになりました。

```bash
claude --version
```

```text
2.1.300 (Claude Code)
```

デスクトップアプリの Claude Code は、2.1.295 でした。02 で見た「使う場所ごとに本体が別々で、バージョンが違うことがある」が、実際に起きています。

初めて `claude` を起動すると、サインインの方法の選択（Claude のアカウントの契約を選ぶ）、注意書き、ターミナルの推奨設定の確認などの画面が、順に出ました。選択肢は、矢印のキーで選び、`return` キーで決めます。

### サーバーを追加する

サーバーは、**ローカル**の範囲に追加しました。

```bash
claude mcp add --scope local --transport stdio study-lab-calendar -- "$HOME/python-projects/study-lab/venv/bin/python" -m calendar_mcp.server
```

| 部分 | 意味 |
|---|---|
| `--scope local` | ローカルの範囲。自分だけ、このプロジェクトだけで使える。設定は `~/.claude.json` に書かれ、リポジトリには入らない |
| `--transport stdio` | 自分の PC で動かすサーバー |
| `study-lab-calendar` | 付けた名前 |
| `--` から後ろ | サーバーを起動するコマンド |

ローカルにした理由は、このサーバーが、個人のカレンダーを読むものだからです。07 のように、リポジトリの `.mcp.json`（プロジェクトの範囲）に書くと、リポジトリを複製した人の環境でも、このサーバーが動くようになります。サーバーのプログラムはリポジトリで公開していますが、つなぐかどうかは、それぞれの人が決められるようにしました。

追加したあと、つながるかを確かめました。

```bash
claude mcp list
```

```text
（一部の行を省略）
claude-code-docs: https://code.claude.com/docs/mcp (HTTP) - ✔ Connected
study-lab-calendar: /Users/<ユーザー名>/python-projects/study-lab/venv/bin/python -m calendar_mcp.server - ✔ Connected
```

`✔ Connected` は、Claude Code がサーバーを起動し、挨拶と道具の一覧のやり取りまで成功した、という意味です。

## 実際にやってみる

作ったサーバーで、実際に予定を読めるかを確かめました。

### 1. 作ったサーバーで、カレンダーを読んだ

まず、Claude Code を通さずに、カレンダーを読む部分だけを動かして、10 月の 1 か月分の予定を読みました。

| 項目 | 結果 |
|---|---|
| かかった時間 | 約 12 秒 |
| 読めた予定 | カレンダーのアプリに表示されている件数と、一致した |

### 2. Claude に、道具を使わせた

次に、ターミナル版で新しく会話を始め、次のように頼みました。

```text
study-lab-calendar を使って、2026 年 10 月 1 日から 31 日分の予定を一覧にして
```

答えが出るまでに、確認の画面が 2 回出ました（操作した人の記憶による）。

| 画面 | 内容 |
|---|---|
| Claude Code の確認 | Claude が `list_events` の道具を使ってよいか。承認した |
| macOS の確認 | ターミナルのアプリが、カレンダーを使ってよいか。許可した |

1 つ目は、MCP サーバーの道具を使うときの、Claude Code の権限の確認です（[03. 権限モードと、確認を減らす方法](./03-permission-modes) を参照）。2 つ目は、macOS が、アプリごとに求める許可です。

Claude は、`list_events` の道具を使い、10 月の予定を一覧にして答えました。直前にカレンダーのアプリで 1 件の予定を加えておいたところ、その予定も、答えに含まれていました。サーバーが、使われるたびに、カレンダーを読みに行っていることが分かります。

Claude の答えは、たとえば次のような形になります（予定は、作りものに置き換えています）。

```text
- 2026-10-04 終日 運動会（家族）
- 2026-10-16 2026-10-16T10:00:00 〜 2026-10-16T11:00:00 歯医者（個人）
- 2026-10-25 終日 旅行（家族）
```

### 3. 想定していなかったこと

**カレンダーのアプリが起動していないと、読めなかった**

最初に読もうとしたとき、次のエラーになりました。

```text
Calendarでエラーが起きました: アプリケーションは実行されていません。 (-600)
```

カレンダーのアプリが、起動していなかったためです。通常、AppleScript でアプリに問い合わせると、そのアプリが自動で起動します。今回は、起動しませんでした。Claude がコマンドを実行する環境に、ほかのアプリを起動できない制限がかかっていたためと考えられますが、確かめてはいません。カレンダーのアプリを開いておくと、読めるようになりました。

**macOS の許可の画面が、何度か出た**

カレンダーを読むと、macOS が、カレンダーの操作やカレンダーへのアクセスを許可するかを尋ねる画面を出しました。許可は、プログラムを動かしたアプリごとに求められます。手順 1 で、デスクトップアプリの Claude から動かしたときにも、手順 2 で、ターミナル版から動かしたときにも、それぞれ許可を求められました。手順 1 では、原因を調べるために実行したコマンドが、サーバーには必要のない許可（アプリの一覧などを扱う仕組みへの操作の許可）を、余分に求めていた可能性があります。

許可したものは、あとから「システム設定」→「プライバシーとセキュリティ」の「オートメーション」と「カレンダー」で、確かめたり、取り消したりできます。

**ターミナル版では、プロジェクトの MCP サーバーを使ってよいかを尋ねる画面が出た**

ターミナル版を、このリポジトリで初めて起動したとき、次の画面が出ました。

```text
New MCP server found in this project: claude-code-docs

MCP servers may execute code or access system resources. All tool calls require approval.

  Use this MCP server
  Use this and all future MCP servers in this project
❯ Continue without using this MCP server
```

07 でつないだ、リポジトリの `.mcp.json` のサーバーについての確認です。07 では、デスクトップアプリで、この画面が出ないままつながりました。ターミナル版では、公式ドキュメントのとおり、初めて起動したときに尋ねられました。

選択肢のうち、2 つ目（今後このプロジェクトに加わるサーバーも、すべて使う）は選ばず、1 つ目（このサーバーだけを使う）を選びました。2 つ目を選ぶと、あとで `.mcp.json` に別のサーバーが書き足されたときに、確認なしで使われるようになるためです。

## 個人の情報を扱うときに、気をつけること

このサーバーは、個人の予定を読みます。作る前に、予定の中身がどこに渡るかを整理しました。

| 渡る先 | 何が渡るか |
|---|---|
| このサイトのページ | 作りものの予定の例だけ |
| GitHub のリポジトリ | サーバーのプログラムだけ。予定の中身は入らない |
| Claude との会話 | Claude が読んだ予定の中身。会話の一部として、Anthropic に送られる |
| この Mac の中 | 会話の記録（`~/.claude/projects/` の下）。暗号化されずに保存される |

Claude との会話が学習に使われるかどうかは、claude.ai の設定（Settings → Privacy の「Help improve our AI models」）で決まります。個人向けのプランでは、この設定がオンだと、Claude Code の会話も学習に使われ、5 年間保存されます。オフにすると、学習には使われず、保存は 30 日になります。個人の情報を扱うサーバーをつなぐ前に、この設定を確かめておきます。この作業では、設定がオンになっていたので、オフにしてから、カレンダーを読みました。

ほかに、次の点に気をつけました。

- 道具は、読み取りだけにする。
- 一度に読む範囲に、上限を設ける。
- サーバーの設定は、ローカルの範囲にして、ほかの人の環境では動かないようにする。
- 組織のアカウントの予定が同期されているカレンダーは、読まないようにする。このサーバーは、すべてのカレンダーを読む作りなので、そうした予定が同期されている環境では、読むカレンダーを絞る作りに変える必要がある。

## まとめ

- ほしいコネクターがないときは、MCP サーバーを自分で作れる。自分の PC で動かすサーバーは、標準入力と標準出力で、Claude Code と 1 行ずつメッセージをやり取りする。
- サーバーが応答するのは、挨拶（`initialize`）、道具の一覧（`tools/list`）、道具を使う（`tools/call`）の 3 つが中心。標準出力には、MCP のメッセージ以外を書かない。
- 道具の説明は、Claude が道具を使うかどうかの判断の材料になる。何をする道具か、何をしない道具かを書く。
- 作ったサーバーは、ターミナル版の `claude mcp add` で追加し、`claude mcp list` で確かめる。個人の情報を扱うサーバーは、ローカルの範囲に追加する。
- 個人の情報を扱う前に、その情報がどこに渡るかと、学習に使われる設定を確かめる。

## 確認の記録

- [Transports（Model Context Protocol の仕様）](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- [Lifecycle（Model Context Protocol の仕様）](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
- [Connect Claude Code to tools via MCP（Claude Code Docs）](https://code.claude.com/docs/en/mcp)
- [Advanced setup（Claude Code Docs）](https://code.claude.com/docs/en/setup)
- [Troubleshoot installation and login（Claude Code Docs）](https://code.claude.com/docs/en/troubleshoot-install)
- [Data usage（Claude Code Docs）](https://code.claude.com/docs/en/data-usage)

| 項目 | 内容 |
|---|---|
| 最終確認日 | 2026 年 10 月 15 日 |
| Claude Code のバージョン | デスクトップアプリ 2.1.295、ターミナル版 2.1.300（macOS） |
| 検証の状況 | サーバーのプログラム、テスト、カレンダーの読み取り、ターミナル版の導入、`claude mcp add` と `claude mcp list`、ターミナル版の会話で Claude が道具を使うことは、この Mac で実際に確かめた |
| 確かめていない内容 | デスクトップアプリの会話から、このサーバーを使うこと。繰り返しの予定が、長い期間でも正しく読めること。MCP サーバーを作るための部品（SDK）を使う方法 |
