# Python のテストと lint を CI で自動実行する

このページでは、PR（プルリクエスト：変更の提案）を出すたびに、Python のテストと lint を自動で実行する仕組みを作った手順をまとめます。あとから、型の検査も加えました。テストは、3 つの OS（Linux・Windows・macOS）と 2 つの Python バージョンの組み合わせで動かします。

テストの対象にしたプログラムの設計については、[通信するプログラムを、テストしやすく作る](./testable-python) で説明しています。

## 用語の整理

| 用語 | 意味 |
|---|---|
| テスト | プログラムが期待どおりに動くかを、別のプログラムで確かめること |
| lint（リント） | コードの書き方に誤りや、決まりから外れた書き方がないかを検査すること |
| pytest | Python のテストを実行するツール |
| ruff | Python の lint と、書式の確認・整形を行うツール |
| 型 | 値の種類。数字、文字列、日付、一覧など |
| 型の検査 | プログラムを動かさずに読んで、値の種類が合っているか（数字を渡すべきところに文字を渡していないか、など）を調べること |
| pyright | Python の型の検査を行うツール |
| ワークフロー | GitHub Actions で自動実行する手順をまとめたファイル |
| ジョブ | ワークフローの中の作業のまとまり。ジョブごとに別の仮想マシンで動く |
| マトリクス | OS やバージョンなどの組み合わせを指定して、同じジョブを複数の条件で動かす仕組み |
| 必須チェック | ブランチ保護で「合格しないとマージできない」と指定したチェック |

## 全体の構成

ワークフロー `.github/workflows/python-ci.yml` には、4 つのジョブがあります。

| ジョブ | 役割 | 動かす環境 |
|---|---|---|
| `python-lint` | ruff で書き方を検査し、書式が整っているかを確認する | Linux × Python 3.13 |
| `python-typecheck` | pyright で型の検査をする | Linux × Python 3.13 |
| `python-test` | pytest でテストを実行する | 3 つの OS × 2 つの Python バージョン（6 通り） |
| `python-ci` | 上の 3 つの結果をまとめて、合格か不合格かを判定する | Linux |

```text
python-lint ─────────────┐
python-typecheck ────────┼─→ python-ci（結果のまとめ）
python-test（6 通り）─────┘
```

ブランチ保護の必須チェックには、最後の `python-ci` だけを登録します。その理由は、あとの節で説明します。

## 開発用の部品はバージョンを固定する

pytest、ruff、pyright は、`requirements-dev.txt` にバージョンを固定して書いています。

```text
pytest==9.1.1
ruff==0.17.1
pyright==1.1.414
```

バージョンを固定しないと、新しい版が公開された日から、何も変更していないのに CI の結果が変わることがあります。特に lint は、新しい版で検査の内容が増えると、昨日まで合格していたコードが不合格になります。固定しておけば、手元と CI で同じ結果になり、更新は Dependabot の PR を通して、チェックを確認しながら行えます。

## ワークフローを読む

### 動くタイミングと権限

```yaml
name: Python CI

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: python-ci-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

- `on`：`main` に向けた PR が作られたとき、または更新されたときに動きます。
- `permissions`：検査するだけなので、リポジトリを読む権限だけを与えています。
- `concurrency`：同じ PR に続けて push された場合、古い実行を止めて、最新のものだけを実行します。

### python-lint：書き方の検査

```yaml
  python-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.13"
          cache: pip
          cache-dependency-path: requirements-dev.txt

      - name: Install dependencies
        run: python -m pip install -r requirements-dev.txt

      - name: Lint with ruff
        run: ruff check .

      - name: Check formatting with ruff
        run: ruff format --check .
```

- `ruff check .`：書き方の誤りを検査します。
- `ruff format --check .`：書式が整っているかを確認します。`--check` を付けると、ファイルを書き換えずに、整っていないファイルがあれば失敗します。
- lint の結果は OS によって変わらないので、Linux の 1 つの環境だけで動かしています。

### python-typecheck：型の検査

```yaml
  python-typecheck:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.13"
          cache: pip
          cache-dependency-path: requirements-dev.txt

      - name: Install dependencies
        run: python -m pip install -r requirements-dev.txt -e .

      - name: Type check with pyright
        run: pyright
```

- `-e .` で、このリポジトリの Python のパッケージも入れています。型の検査は、パッケージどうしの関係もたどるためです。
- 検査の対象と、前提にする Python のバージョンは、`pyproject.toml` に書いています。

```toml
[tool.pyright]
include = ["src", "tests"]
pythonVersion = "3.13"
```

このジョブは、あとから加えました。はじめは、lint（ruff）とテスト（pytest）があれば十分だと考えていました。しかし、この 2 つが調べるものと、型の検査が調べるものは、違います。

| 道具 | 調べるもの | 見逃すもの |
|---|---|---|
| ruff | 書き方。誤った書き方、使っていない読み込み、書式の乱れなど | 値の種類が合っているか |
| pytest | 動き。テストを書いた部分が、正しい答えを返すか | テストを書いていない部分の誤り |
| pyright | 型。値の種類が合っているか、存在しない関数や項目を使っていないか。テストを書いていない部分も含めて、すべてのコードを読む | 動きが正しいか（たとえば、並べる順番が逆でも、型は合っているので気づかない） |

3 つは、互いに代わりになるものではなく、穴を埋め合う関係です。

型の検査を加えると、さっそく、テストのコードの弱いところが 6 か所見つかりました。

サーバーの `handle` 関数は、応答を返すときと、何も返さない（`None`）ときがあります。テストでは、その戻り値から、何も返さなかった場合を考えずに、中身を取り出していました。今のテストでは、いつも応答が返るので合格していました。しかし、もし何も返らなかったら、テストはその場で、原因の分かりにくいエラーで止まります。

テストを動かしているだけでは気づけないところを、pyright が見つけました。型の検査を入れる目的どおりの働きです。

直し方：テストのコードに、「応答が返ってきたことを確かめてから、中身を渡す」小さな関数（`respond`）を足し、`handle` を直接使っていた 4 か所で、この関数を使うようにしました。

### python-test：テスト

```yaml
  python-test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.13", "3.14"]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Setup Python
        uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
          cache-dependency-path: requirements-dev.txt

      - name: Install dependencies
        run: python -m pip install -r requirements-dev.txt -e .

      - name: Test with pytest
        run: pytest
```

`python -m pip install` の `-e .` は、このリポジトリのプログラム自体を、テストから読み込めるようにインストールする指定です。

## マトリクスで複数の OS とバージョンを試す

`matrix` に一覧を書くと、その組み合わせの数だけジョブが作られます。

```yaml
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.13", "3.14"]
```

OS が 3 つ、Python のバージョンが 2 つなので、3 × 2 ＝ 6 通りのジョブが同時に動きます。それぞれのジョブの中では、`matrix.os` や `matrix.python-version` という書き方で、自分の組み合わせの値を参照できます。

バージョンは `"3.13"` のように引用符で囲みます。囲まないと数値として扱われ、たとえば `3.10` が `3.1` と解釈されてしまうためです。

### fail-fast: false

初期設定では、マトリクスの 1 つが失敗すると、残りのジョブは途中で中止されます。`fail-fast: false` にすると、1 つが失敗しても、ほかを最後まで実行します。「Windows だけ失敗する」のか「すべての OS で失敗する」のかを、1 回の実行で見分けられます。

### 実際の所要時間

| 環境 | 所要時間の例 |
|---|---|
| Linux | 11〜15 秒 |
| macOS | 14〜18 秒 |
| Windows | 27〜33 秒 |

公開リポジトリでは、GitHub が用意した標準の実行環境を無料で使えます。

## OS をあとから変える方法

プログラムによっては、Windows 限定など、特定の OS だけで動かしたい場合があります。その方法を、規模の小さい順に挙げます。

### 1. 一覧を書き換える

```yaml
        os: [windows-latest]
```

### 2. 特定の組み合わせだけ除く

```yaml
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.13", "3.14"]
        exclude:
          - os: macos-latest
            python-version: "3.14"
```

### 3. テスト単位で OS を限定する

プログラム全体は 3 つの OS で動くが、一部の機能だけが Windows 限定、という場合に使います。条件に合わない OS では、そのテストだけが自動で飛ばされます。

```python
import sys

import pytest


@pytest.mark.skipif(sys.platform != "win32", reason="Windows 専用の機能")
def test_windows_only_feature():
    ...
```

### 4. 再利用可能なワークフローにして、呼び出す側から指定する

複数のリポジトリで同じ CI を使う場合は、ほかのワークフローから呼び出せる形（再利用可能なワークフロー）にして、OS の一覧を呼び出す側から渡します。CI の中身を 1 か所で管理しながら、OS だけをリポジトリごとに変えられます。このサイトでは、まだこの形にはしていません。

## 結果をまとめるジョブを作る理由

```yaml
  python-ci:
    if: always()
    needs: [python-lint, python-typecheck, python-test]
    runs-on: ubuntu-latest
    steps:
      - name: Check results
        env:
          LINT_RESULT: ${{ needs.python-lint.result }}
          TYPECHECK_RESULT: ${{ needs.python-typecheck.result }}
          TEST_RESULT: ${{ needs.python-test.result }}
        run: |
          echo "python-lint: $LINT_RESULT"
          echo "python-typecheck: $TYPECHECK_RESULT"
          echo "python-test: $TEST_RESULT"
          if [ "$LINT_RESULT" != "success" ] || [ "$TYPECHECK_RESULT" != "success" ] || [ "$TEST_RESULT" != "success" ]; then
            echo "lint、型の検査、テストのどれかが成功していません。"
            exit 1
          fi
```

### 必須チェックの登録を 1 つにするため

ブランチ保護の必須チェックは、チェックの名前を 1 つずつ登録します。マトリクスのジョブは、`python-test (windows-latest, 3.13)` のように、組み合わせごとに別の名前になります。6 通りを 1 つずつ登録すると、OS やバージョンを変えるたびに、ブランチ保護の設定も直さなければなりません。直し忘れると、存在しない名前のチェックを待ち続けることになり、どの PR もマージできなくなります。

結果をまとめるジョブを 1 つ作り、それだけを登録しておけば、マトリクスの内容を変えても、ブランチ保護の設定はそのままで済みます。

### 落とし穴：スキップされた必須チェックは「合格」として扱われる

`needs` を指定したジョブは、前のジョブが失敗すると、通常は実行されずに「スキップ」になります。ところが GitHub では、**スキップされたジョブは、必須チェックとしては合格の扱い**になります。何も対策をしないと、テストが失敗しているのにマージできてしまいます。

そのため、次の 2 点を入れています。

- `if: always()`：前のジョブが失敗しても、このジョブを必ず実行する。
- 前のジョブの結果（`needs.<ジョブ名>.result`）を確認し、`success` でなければ `exit 1` で自分も失敗する。

マトリクスのジョブの結果は、1 つでも失敗があれば `failure` になります。

## 「変更されたときだけ動かす」設定をしなかった理由

ワークフローには、「Python のファイルが変更されたときだけ動かす」という設定（`paths` フィルタ）もあります。しかし、必須チェックに登録したワークフローがこの設定で動かなかった場合、チェックの結果が報告されないままになり、**PR がいつまでもマージできなくなります**。

そのため、記事だけを変更する PR でも、Python の CI は毎回動かしています。所要時間は 1 分以内です。

## 必須チェックに登録する順番

必須チェックへの登録は、次の順番で行いました。

1. CI のワークフローを追加する PR を出し、チェックが動くことを確認してマージする
2. そのあとで、ブランチ保護の必須チェックに `python-ci` を追加する

順番を逆にすると、`python-ci` というチェックがまだ存在しない状態で、それを必須にすることになります。CI を追加する PR を含め、どの PR もマージできなくなります。

## チェックが失敗を報告できるかを確かめる

すべて合格しているチェックを見ても、「失敗したときに正しく不合格になるか」は分かりません。必須チェックに登録する前に、次の方法で確かめました。

1. わざと失敗するテストを 1 つ入れた、確認専用の PR を作る
2. チェックの結果を確認する
3. PR をマージせずに閉じ、ブランチを削除する

```python
def test_intentional_failure():
    assert 1 + 1 == 3
```

結果は次のとおりでした。

| チェック | 結果 |
|---|---|
| `python-test`（6 通りすべて） | 不合格 |
| `python-lint` | 合格 |
| `python-ci` | 不合格 |

`python-ci` が、スキップではなく不合格になることを確認できました。そのうえで必須チェックに登録したところ、ほかのチェックに合格していても、`python-ci` が終わるまではマージできない状態になりました。

## まとめ

- 開発用の部品はバージョンを固定し、手元と CI で同じ結果になるようにする。
- lint（ruff）、型の検査（pyright）、テスト（pytest）は、調べるものが違う。テストがあっても、型の検査の代わりにはならない。
- マトリクスを使うと、複数の OS とバージョンの組み合わせを、1 つの設定で同時に試せる。
- 必須チェックには、結果をまとめるジョブを 1 つだけ登録する。マトリクスの内容を変えても、ブランチ保護の設定を直さずに済む。
- スキップされた必須チェックは合格として扱われる。まとめのジョブは `if: always()` で必ず実行し、前のジョブの結果を自分で確認する。
- 必須チェックのワークフローには、`paths` フィルタを付けない。
- 必須チェックは、CI が動くことを確かめてから登録する。失敗を正しく報告できることも、わざと失敗させて確かめる。
