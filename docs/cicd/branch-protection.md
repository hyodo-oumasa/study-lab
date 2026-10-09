# ブランチ保護（ルールセット）で main を守る

このページでは、このサイト（study-lab）の `main` ブランチに、GitHub のブランチ保護を設定した手順と結果をまとめます。

ブランチ保護とは、特定のブランチに入る変更に対して、GitHub がルールを強制する仕組みです。設定する前は、「PR を出して、チェックの合格を確かめてからマージする」という手順を守るかどうかが、作業する人の注意力に任されていました。実際に、手順を通さずに `main` へ直接変更を送ることもできる状態でした。ブランチ保護を設定すると、手順を守らない変更を GitHub が自動で拒否するようになります。

## 用語の整理

| 用語 | 意味 |
|---|---|
| ブランチ | 変更の流れを分けて管理する仕組み。`main` は公開サイトの元になる本番のブランチ |
| push | 手元の変更を GitHub に送ること |
| 強制 push | `git push --force` のように、GitHub 上の履歴を書き換える push。ほかの人の変更を消してしまうおそれがある |
| PR（プルリクエスト） | 「この変更を取り込みたい」という提案。承認されるまで本番には反映されない |
| マージ | PR の変更を `main` に取り込むこと |
| ステータスチェック | PR に対して自動で実行される確認。このサイトでは、ビルドできるかを試す `docs-build` |
| ルールセット | ブランチ保護のルールをまとめて設定する、GitHub の新しい仕組み |

## 2 つの方式

GitHub には、ブランチを保護する仕組みが 2 つあります。

| 方式 | 特徴 |
|---|---|
| ブランチ保護ルール（従来の方式） | 古くからある設定。ブランチごとに個別に設定する |
| ルールセット（Rulesets） | 新しい方式。設定を JSON（設定を書くための書式）で書き出したり読み込んだりできる。削除せずに一時的に無効にすることもできる |

このサイトでは、ルールセットを使いました。新しく設定する場合は、GitHub もルールセットを勧めています。公開リポジトリなら、無料プランで使えます。

## 設定したルールと、その理由

対象は `main` ブランチだけです。

| # | ルール | 効果 | 設定 |
|---|---|---|---|
| ① | PR を必須にする | `main` への直接の push を拒否する。変更は必ず PR を通す | 有効 |
| ② | 承認（レビュー）の必要人数 | マージする前に、ほかの人の承認を何人分必要にするか | 0 人 |
| ③ | ステータスチェックを必須にする | `docs-build` に合格しないとマージできない | 有効 |
| ④ | マージ前に最新の `main` を取り込むことを必須にする | PR が古い `main` を元にしている場合、最新の `main` を取り込んでからでないとマージできない | 無効 |
| ⑤ | 強制 push を禁止する | 履歴を書き換える push を拒否する | 有効 |
| ⑥ | ブランチの削除を禁止する | `main` を誤って削除できないようにする | 有効 |
| ⑦ | 例外（バイパス）を認める人 | ルールを無視してよい人 | なし |

判断が分かれる 3 点について、理由をまとめます。

### ② 承認を 0 人にした理由

GitHub では、PR を作った本人は、その PR を承認できません。このサイトは 1 人で運用しているので、1 人以上にすると誰もマージできなくなります。そのため 0 人にして、内容の確認は人が目で行う運用にしました。

0 人は「確認しなくてよい」という意味ではありません。詳しくは、[PR の承認の仕組みと、AI が作る PR](./pr-approval-and-ai) で説明しています。

### ④ 最新の取り込みを必須にしなかった理由

有効にすると、ほかの PR をマージするたびに、残りの PR すべてで「最新の `main` を取り込む → チェックをやり直す」作業が必要になります。より安全ですが、1 人で運用するには手間が大きいため、無効にしました。

- 無効にした場合のリスク：別々の PR を続けてマージしたとき、それらの組み合わせで起きる問題を、事前には検出できません。
- 補う仕組み：マージしたあとのデプロイでもビルドが行われるので、問題があればそこで失敗して気づけます。失敗した場合、公開中のサイトはそのまま残ります。

### ⑦ 例外を認めなかった理由

リポジトリの管理者を例外に入れると、管理者のアカウントで作業している AI エージェントも、ルールを無視して `main` に直接 push できてしまいます。それではルールを作る意味がないので、例外は設けていません。緊急時は、ルールセットを一時的に無効にして対応します。

## 設定のしかた（JSON で管理する）

ルールセットは GitHub の画面からも設定できますが、このサイトでは JSON ファイルにルールを書き、GitHub CLI（コマンドで GitHub を操作するツール `gh`）で適用しました。設定の内容が文字として残るので、何を設定したのかが正確に分かり、ほかのリポジトリでも再現できます。

### JSON の全文

リポジトリの `.github/rulesets/main-branch-protection.json` に保存しています。

```json
{
  "name": "main-branch-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": [
        "~DEFAULT_BRANCH"
      ],
      "exclude": []
    }
  },
  "bypass_actors": [],
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false,
        "allowed_merge_methods": [
          "merge",
          "squash",
          "rebase"
        ],
        "require_extra_approval_for_unattributed_changes": true,
        "required_reviewers": []
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [
          {
            "context": "docs-build",
            "integration_id": 15368
          }
        ],
        "do_not_enforce_on_create": false
      }
    },
    {
      "type": "non_fast_forward"
    },
    {
      "type": "deletion"
    }
  ]
}
```

主な項目の意味です。

| 項目 | 意味 |
|---|---|
| `enforcement: "active"` | ルールを有効にする。`"disabled"` にすると、削除せずに無効にできる |
| `~DEFAULT_BRANCH` | リポジトリのデフォルトブランチ（ここでは `main`）を対象にする |
| `bypass_actors: []` | 例外を認める人はいない |
| `pull_request` | PR を必須にするルール。`required_approving_review_count` が承認の必要人数 |
| `required_status_checks` | 必須のステータスチェック。`strict_required_status_checks_policy` が上の表の ④ |
| `integration_id: 15368` | そのチェックを報告するアプリの ID。15368 は GitHub Actions。ほかのアプリが同じ名前のチェックを報告しても、合格として扱われない |
| `non_fast_forward` | 強制 push を禁止するルール |
| `deletion` | ブランチの削除を禁止するルール |

`integration_id` は、実際にチェックが動いたコミットの情報から調べられます。

```bash
gh api repos/OWNER/REPO/commits/COMMIT_SHA/check-runs --jq '.check_runs[] | "\(.name) \(.app.slug) \(.app.id)"'
```

### 適用するコマンド

```bash
gh api -X POST repos/OWNER/REPO/rulesets --input .github/rulesets/main-branch-protection.json
```

`OWNER/REPO` は、自分のリポジトリ名に置き換えてください。

### GitHub が自動で付ける設定

最初に書いた JSON には、次の 4 つの項目はありませんでした。適用したところ、GitHub が既定の値で自動的に追加しました。

| 項目 | 自動で付いた値 | 意味 |
|---|---|---|
| `allowed_merge_methods` | merge、squash、rebase | 使ってよいマージの方法 |
| `require_extra_approval_for_unattributed_changes` | true | 人に結び付いていない AI の PR に、承認を 1 人追加する（承認 0 人なら効果なし。[PR の承認の仕組みと、AI が作る PR](./pr-approval-and-ai) を参照） |
| `required_reviewers` | 空 | 特定のファイルにレビュアーを指定する設定 |
| `do_not_enforce_on_create` | false | ブランチを作った直後にチェックを免除するかどうか（免除しない） |

ファイルに書かれていない設定があると、あとで読んだときに実際の設定が分かりません。そこで、適用後の設定を GitHub から取得し、ファイルと一致させました。一致しているかどうかは、目で見比べずに、プログラムで比較して確かめました。

```bash
gh api repos/OWNER/REPO/rulesets/RULESET_ID --jq '{name, target, enforcement, conditions, bypass_actors, rules}'
```

## 設定後の確認

### main への直接の push が拒否される

確認用のコミットを作って `main` に push すると、次のように拒否されました。確認用のコミットは、そのあと手元から削除しています。

```text
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - Required status check "docs-build" is expected.
 ! [remote rejected] main -> main (push declined due to repository rule violations)
```

「変更は PR を通す必要がある」「`docs-build` のチェックが必要」という 2 つのルールに違反した、という意味です。

### チェックが終わるまで PR をマージできない

PR を作った直後、チェックがまだ動いている間は、PR の状態が `BLOCKED`（ブロック中）になり、マージできませんでした。チェックに合格すると、状態が `CLEAN`（マージ可能）に変わりました。

```bash
gh pr view PR_NUMBER --json mergeStateStatus
```

## 設定して変わったこと

| 場面 | 設定前 | 設定後 |
|---|---|---|
| 記事の追加・修正 | `main` に直接 push することもできた | 必ず作業用のブランチで PR を作る。誤字の修正のような小さな変更でも同じ |
| PR のマージ | チェックの合格を、目で確認してからマージしていた | チェックに合格するまで、マージできない |
| Dependabot の PR | 同上 | 同上 |
| マージ後のデプロイ | 自動 | 変わらない |

注意点が 1 つあります。ワークフローのジョブ名（`docs-build`）を変えると、ルールセットの `context` も合わせて変える必要があります。変えないと、必須のチェックがいつまでも報告されない状態になり、どの PR もマージできなくなります。

## 戻し方

ルールセットは、すぐに無効化・削除できます。

- 一時的に無効にする：JSON の `enforcement` を `"disabled"` にして、更新のコマンドで適用する

```bash
gh api -X PUT repos/OWNER/REPO/rulesets/RULESET_ID --input .github/rulesets/main-branch-protection.json
```

- 削除する

```bash
gh api -X DELETE repos/OWNER/REPO/rulesets/RULESET_ID
```

## まとめ

- ブランチ保護を設定すると、「PR を出す → チェックに合格する → マージする」という手順を、GitHub が強制してくれる。
- 新しく設定するなら、JSON で管理できるルールセットが便利。
- 1 人で運用するリポジトリでは、承認の必要人数を 0 人にする。確認は人が目で行う。
- 例外を認める人を設定すると、そのアカウントで動く AI エージェントもルールを無視できてしまう点に注意する。
- GitHub は既定の設定を自動で追加するので、適用後の設定を取得して、ファイルと一致させておく。
