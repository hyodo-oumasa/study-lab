# study-lab

学習した内容をまとめ、GitHub Pages で公開するサイトのリポジトリ。
サイトは VitePress で作り、`docs/` 以下の Markdown がページになる。

## コマンド

- サイトのビルド：`npm run docs:build`
- ビルド結果の確認：`npm run docs:preview -- --port 4173`
  - ビルドし直したら、確認用のサーバーを起動し直す（古いファイル一覧のままになるため）
- Python のテスト：`pytest`
- Python の lint：`ruff check .`
- Python の型の検査：`pyright`（仮想環境の外から動かすときは `venv/bin/pyright --pythonpath venv/bin/python`）
- Python の仮想環境は `venv/`

## 変更の進め方

- `main` へ直接 push しない。ブランチを作り、プルリクエストを出す
- 必須のチェック（`docs-build`、`python-ci`）に合格してから、マージする
- 公開の前に、確認用のサーバーで表示を確かめる

## ページを書くときの決まり

- 専門用語は、最初に出てくるところで説明する
- 事実は、公式ドキュメントで確かめてから書く。確かめていない内容は、その旨を書く
- 資格試験の問題文や、その再現は載せない。確認問題は自作する
- 新しいページを公開したら、次の 3 か所を更新する
  - テーマのトップページ（`docs/<テーマ>/index.md`）の一覧
  - サイドバー（`docs/.vitepress/config.mts`）
  - トップページ（`docs/index.md`）の「新着記事」
