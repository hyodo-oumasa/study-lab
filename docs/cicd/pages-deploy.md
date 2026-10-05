# このサイトが公開されるまで

このページでは、このサイト（study-lab）が GitHub Pages に自動で公開される仕組みを解説します。実際に動いているワークフローファイルを、上から順に読んでいきます。

## 全体の流れ

Markdown でノートを書いて `main` ブランチに push すると、あとは自動でサイトに反映されます。

```text
① 手元で Markdown を書く
      ↓  git push（main ブランチ）
② GitHub が push を検知し、ワークフローを起動する
      ↓
③ build ジョブ：GitHub が用意した仮想マシン上で、サイトをビルドする
      ↓  ビルド結果（HTML など）を受け渡す
④ deploy ジョブ：ビルド結果を GitHub Pages に公開する
      ↓
⑤ https://hyodo-oumasa.github.io/study-lab/ に反映される
```

push してから公開されるまでの時間は、実測で 30 秒ほどでした（build 14 秒、deploy 9 秒、残りは待ち時間）。

## 登場するファイル

```text
study-lab/
├─ .github/
│  └─ workflows/
│     └─ deploy.yml        ← 自動化の手順書（ワークフロー）
├─ docs/
│  ├─ .vitepress/
│  │  └─ config.mts        ← サイト全体の設定
│  ├─ index.md             ← トップページ
│  └─ cicd/ など            ← 各テーマのノート
├─ package.json            ← 使う npm パッケージとコマンドの定義
└─ package-lock.json       ← 実際にインストールするバージョンの記録
```

GitHub Actions は、`.github/workflows/` フォルダに置かれた YAML ファイルを自動で読み込みます。この場所とファイル形式は決まりごとなので、フォルダ名を変えると動かなくなります。

## まず押さえたい用語

| 用語 | 意味 | このサイトでの例 |
|---|---|---|
| ワークフロー（workflow） | 自動化の手順全体をまとめたもの。YAML ファイル1つが1つのワークフロー | `deploy.yml` |
| トリガー（trigger） | ワークフローを起動するきっかけ | `main` への push、手動実行 |
| ジョブ（job） | ワークフローを構成する作業のまとまり。ジョブごとに別の仮想マシンで動く | `build` と `deploy` |
| ステップ（step） | ジョブの中で順番に実行される1つ1つの処理 | 「Node.js を用意する」「ビルドする」など |
| アクション（action） | 再利用できる部品化された処理。`uses:` で呼び出す | `actions/checkout` など |
| ランナー（runner） | ジョブを実行する仮想マシン | `ubuntu-latest`（GitHub が用意する Linux） |
| アーティファクト（artifact） | ジョブが作った成果物を保存・受け渡しする仕組み | ビルドされた HTML 一式 |

## ワークフローファイルを読む

ここからは `.github/workflows/deploy.yml` を、ブロックごとに分けて読んでいきます。

### 1. 名前とトリガー

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:
```

- `name`：GitHub の Actions タブに表示されるワークフローの名前です。
- `on`：ワークフローを起動するきっかけ（トリガー）を指定します。
  - `push` と `branches: [main]` の組み合わせで、「`main` ブランチに push されたときだけ」起動します。ほかのブランチへの push では動きません。
  - `workflow_dispatch` を書いておくと、GitHub の画面（Actions タブ）からボタンで手動実行できるようになります。設定を変えずにもう一度デプロイしたいときに便利です。

### 2. 権限

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

ワークフローが実行中に使える権限を指定します。必要なものだけを許可するのが安全です（最小権限の原則）。

| 権限 | 意味 | なぜ必要か |
|---|---|---|
| `contents: read` | リポジトリの中身を読む | ソースコードを取り出してビルドするため |
| `pages: write` | GitHub Pages に書き込む | ビルド結果を公開するため |
| `id-token: write` | 一時的な身分証明書（OIDC トークン）を発行する | デプロイを依頼しているのが、このリポジトリの正規のワークフローであることを GitHub Pages に証明するため |

::: tip なぜパスワードや鍵が要らないのか
`id-token: write` によって、ワークフローは実行のたびに短時間だけ有効な身分証明書を受け取れます。そのため、Pages へのデプロイにパスワードやアクセストークンを Secrets に登録する必要がありません。漏れて困る秘密情報を持たないこと自体が、安全性を高めています。
:::

### 3. 同時実行の制御

```yaml
concurrency:
  group: pages
  cancel-in-progress: false
```

短い間隔で何度も push すると、ワークフローが重なって起動することがあります。`concurrency` はその扱いを決める設定です。

- `group: pages`：同じグループ名を持つ実行は、同時に1つしか動かないようにします。
- `cancel-in-progress: false`：すでに実行中のものは途中で止めず、最後まで終わらせます。後から来た実行は、前の実行が終わるまで待機します。

デプロイが途中で中断されると、公開中のサイトが中途半端な状態になるおそれがあります。そのため、「止めずに待たせる」設定にしています。

### 4. build ジョブ：サイトを組み立てる

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Setup Node.js
        uses: actions/setup-node@v5
        with:
          node-version: 24
          cache: npm

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Install dependencies
        run: npm ci

      - name: Build with VitePress
        run: npm run docs:build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: docs/.vitepress/dist
```

`runs-on: ubuntu-latest` は、「GitHub が用意した最新の Ubuntu（Linux）の仮想マシンで動かす」という指定です。この仮想マシンはジョブのたびに新品の状態で用意され、終わると捨てられます。そのため、必要なものは毎回ステップの中で準備します。

ステップは上から順に実行されます。

| ステップ | やっていること | 手元で同じことをするなら |
|---|---|---|
| Checkout | リポジトリのファイルを仮想マシンにコピーする | `git clone` |
| Setup Node.js | Node.js 24 をインストールする。`cache: npm` で、ダウンロードしたパッケージを次回以降に再利用する | Node.js のインストール |
| Setup Pages | GitHub Pages の設定情報を読み込み、デプロイの準備をする | （該当なし） |
| Install dependencies | `package-lock.json` に記録されたとおりのバージョンでパッケージをインストールする | `npm ci` |
| Build with VitePress | Markdown から HTML を生成する | `npm run docs:build` |
| Upload artifact | 生成された `docs/.vitepress/dist` を、Pages 用の成果物として保存する | （該当なし） |

`uses:` はアクション（部品化された処理）を呼び出す書き方で、`run:` はシェルのコマンドを直接実行する書き方です。`@v5` の部分は、使うアクションのバージョンです。

::: tip npm install ではなく npm ci を使う理由
`npm install` は、状況によって `package-lock.json` を書き換えることがあります。`npm ci` は `package-lock.json` のとおりに厳密にインストールし、食い違いがあればエラーで止まります。CI では「いつ実行しても同じ結果になること」が大切なので、`npm ci` を使います。
:::

### 5. deploy ジョブ：公開する

```yaml
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- `needs: build`：build ジョブが成功してから実行する、という順序の指定です。何も書かないと、2つのジョブは同時に動き出してしまいます。build が失敗した場合、deploy は実行されないので、壊れたサイトが公開されることはありません。
- `environment`：デプロイ先の「環境」を指定します。`github-pages` という環境へのデプロイ履歴が、リポジトリの画面に記録されます。`url` に指定した公開 URL は、Actions の実行結果の画面にリンクとして表示されます。
- `actions/deploy-pages`：build ジョブがアップロードした成果物を受け取り、GitHub Pages に公開します。`id: deployment` で付けた名前を使って、上の `url` が公開 URL を参照しています。

::: info ジョブ間でファイルを受け渡す仕組み
ジョブごとに別の仮想マシンで動くため、build ジョブで作ったファイルは、そのままでは deploy ジョブから見えません。そこで、build ジョブの最後に成果物をアップロードし（アーティファクト）、deploy ジョブがそれを受け取って公開する、という受け渡しをしています。
:::

## GitHub 側で必要な設定

ワークフローファイルを置くだけでなく、リポジトリの設定で「Pages の公開元を GitHub Actions にする」必要があります。

**画面から設定する場合**

リポジトリの Settings → Pages → Build and deployment の Source で「GitHub Actions」を選びます。

**コマンドで設定する場合（GitHub CLI）**

```bash
gh api -X POST repos/hyodo-oumasa/study-lab/pages -f build_type=workflow
```

公開元には「ブランチから公開する」方式もあります。ただ、ブランチ方式では、ビルドしたファイルをリポジトリにコミットしておく必要があります。Actions 方式ならビルドは CI に任せられるので、リポジトリにはソースだけを置けば済みます。

## サイト側で必要な設定：base

GitHub Pages では、このサイトは `https://hyodo-oumasa.github.io/study-lab/` のように、リポジトリ名のサブパスの下で公開されます。そのため、VitePress の設定ファイル `docs/.vitepress/config.mts` で、サイトのルートを合わせています。

```ts
export default defineConfig({
  base: '/study-lab/',
  // ...
})
```

`base` を設定し忘れると、HTML は表示されても CSS や画像のパスがずれてしまい、デザインが崩れた状態で表示されます。サブパスで公開するときに最もつまずきやすいポイントです。

## 手元で同じ手順を確認する

CI で失敗してから原因を探すより、push する前に手元で同じ手順を試すほうが早く確実です。リポジトリのフォルダで、CI と同じ順にコマンドを実行します。

**macOS / Linux**

```bash
npm ci
npm run docs:build
npm run docs:preview
```

**Windows（PowerShell）**

```powershell
npm ci
npm run docs:build
npm run docs:preview
```

`docs:preview` は、ビルドされた HTML を本番と同じ形で表示します。表示された URL（通常は `http://localhost:4173/study-lab/`）をブラウザで開いて確認します。

## 実際の実行で出た警告

初めてデプロイしたとき、成功はしたものの、実行結果の画面に次の2種類の警告（ANNOTATIONS）が表示されました。

### 1. Node.js 20 の非推奨

一部のアクション（`configure-pages@v5`、`upload-pages-artifact@v4`、`deploy-pages@v4`）が、内部で Node.js 20 を前提に作られているという警告です。GitHub のランナーではすでに Node.js 20 が非推奨になっているため、GitHub が自動で Node.js 24 で動かしてくれています。

- 今は動いているので、すぐに困ることはありません。
- いずれ、アクションのバージョンを新しいものに上げる必要があります。

なお、ワークフローの中で指定した `node-version: 24` は、サイトのビルドに使う Node.js のバージョンです。アクション自体が内部で使う Node.js とは別物です。

### 2. ubuntu-latest の移行予告

`ubuntu-latest` が指す Ubuntu のバージョンが、2026年10月19日から順次 Ubuntu 26 に切り替わるという予告です。`latest` と書いておくと最新版に自動で追従できる反面、ある日突然、実行環境が変わることになります。

| 書き方 | 利点 | 注意点 |
|---|---|---|
| `ubuntu-latest` | 何もしなくても新しい環境に追従できる | 環境が変わったタイミングで、予期せず動かなくなる可能性がある |
| `ubuntu-24.04` のように固定する | いつ実行しても同じ環境で動く | 古いバージョンのサポートが終わる前に、自分で更新する必要がある |

このサイトのように依存関係が少ない場合は、`ubuntu-latest` のままでも影響はまず出ない見込みです。

## まとめ

- `.github/workflows/` に YAML ファイルを置くと、GitHub Actions がそれを読み込んで自動で実行する。
- このサイトでは、`main` への push をきっかけに、build ジョブ（組み立て）と deploy ジョブ（公開）が順に動く。
- 権限は必要最小限に絞り、Pages へのデプロイには一時的な身分証明書（OIDC）を使うので、秘密情報を登録しなくてよい。
- CI では `npm ci` を使い、いつ実行しても同じ結果になるようにする。
- サブパスで公開するときは、VitePress の `base` の設定を忘れない。

## 次に学ぶこと

- Python のテストと lint を自動で実行する CI を追加する
- Dependabot を設定して、アクションやパッケージの更新を自動で提案してもらう（上で見た警告への対処にもつながります）
