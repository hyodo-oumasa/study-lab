# Claude 認定資格

Anthropic が実施している Claude の認定資格に向けた学習ノートです。初級（Foundations）の 3 つの資格を受けるために、公式の試験ガイドをもとに、出題分野ごとにまとめていきます。

::: warning 掲載ルール
このテーマのページには、試験問題やその再現、試験ガイドの例題は載せません。公式ドキュメントで確認した内容と、実際に試した結果をもとにした説明だけを載せます。確認問題は、すべて自作です。
:::

## Claude の認定資格とは

Claude の認定資格は、Claude を使った仕事の力を確かめる、Anthropic の公式の資格です。2026 年 7 月に、4 つの資格がそろいました。

| 資格 | 試験コード | 対象 | 主な範囲 |
|---|---|---|---|
| Claude Certified Associate – Foundations | CCAO-F | お客さまと接する人、導入を進める人。技術者でなくてもよい | 日常の業務での Claude の使い方、プロンプト、出力の確かめ方、モデルや製品の選び方、責任ある AI |
| Claude Certified Developer – Foundations | CCDV-F | 開発者 | Claude API、エージェントの開発、MCP サーバーの開発、評価とデバッグ、セキュリティ |
| Claude Certified Architect – Foundations | CCAR-F | ソリューションアーキテクト（システムの設計を担う人） | Claude Code の設定、Claude Agent SDK、Claude API、MCP、複数のエージェントの協調 |
| Claude Certified Architect – Professional | CCAR-P | 経験のあるアーキテクト | 大規模な導入の設計、システム間の連携、ガバナンス、リスク管理 |

このテーマでは、上の 3 つ（Foundations）を扱います。

### 4 つに共通すること

| 項目 | 内容 |
|---|---|
| 試験時間 | 120 分。受付などを含めると、全体で約 135 分 |
| 問題の形式 | 選択式。答えを 1 つ選ぶ問題と、複数選ぶ問題がある |
| 合格点 | 100〜1,000 点の換算点で、720 点以上 |
| 受験の方法 | オンライン受験（試験官が画面越しに見張る）、または Pearson の試験会場 |
| 言語 | 英語と日本語 |
| 有効期限 | 合格から 12 か月。更新は、無料の確認テストで行う |
| 受験できる人 | Claude Partner Network（Anthropic のパートナー企業の集まり）に加盟している組織で働く人。会社のメールアドレスで登録する |

### 12 月 7 日の内容の変更

2026 年 12 月 7 日から、Associate、Developer、Architect – Professional の 3 つは、試験の内容が新しくなります。新しい試験ガイドは、11 月 17 日に公開されます。Architect – Foundations は、この変更の対象外です。

このテーマでは、変更の対象外の Architect – Foundations から勉強を始め、11 月 17 日に新しい試験ガイドを見てから、Developer と Associate の進め方を決めます。

## 学習の進め方

1 つの出題分野を、次の 3 つの段階で学びます。

| 段階 | すること |
|---|---|
| ① 解説を読む | このテーマの解説のページで、出題分野の内容を日本語で学ぶ。公式ドキュメントで確かめた内容と、このサイトのリポジトリで試した結果をまとめる |
| ② 動画で確かめる | 英語の動画の講座で、同じ出題分野を見る |
| ③ 演習問題を解く | 確認問題と、模擬試験を解く。間違えた出題分野は、① に戻って見直す |

英語の動画や演習問題を読みやすくするために、各ページには、出題分野でよく使われる用語の英語と日本語を並べた表を付けます。

## Architect – Foundations

### 試験の概要

公式の試験ガイド（Version 1.0、2026 年 7 月）による内容です。

| 項目 | 内容 |
|---|---|
| 問題数 | 60 問 |
| 出題の形 | 実際の仕事を想定した 6 つの場面から、4 つが出題される。場面ごとに、いくつかの問題に答える |
| 想定している受験者 | Claude API、Agent SDK、Claude Code、MCP で、6 か月以上ものを作ってきたソリューションアーキテクト |
| 成績表 | 合否と換算点に加えて、出題分野ごとの正答率 |

### 出題分野

| 出題分野 | 英語での名前 | 比重 | 問題数の目安 | 課題の数 | 主な内容 |
|---|---|---|---|---|---|
| 1. エージェントの設計と協調 | Agentic Architecture & Orchestration | 27% | 約 16 問 | 7 | エージェントの作業の繰り返し、複数のエージェントの協調、サブエージェントへの情報の渡し方、Agent SDK のフック、セッションの再開と分岐 |
| 2. 道具の設計と MCP の組み込み | Tool Design & MCP Integration | 18% | 約 11 問 | 5 | 道具の説明の書き方、エラーの返し方、道具の振り分け、Claude Code への MCP の組み込み、組み込みの道具の使い分け |
| 3. Claude Code の設定と使い方 | Claude Code Configuration & Workflows | 20% | 約 12 問 | 6 | CLAUDE.md の階層、スラッシュコマンドとスキル、ファイルの場所ごとのルール、Plan モードの使いどころ、CI への組み込み |
| 4. プロンプトと構造化した出力 | Prompt Engineering & Structured Output | 20% | 約 12 問 | 6 | 判断の基準を明示したプロンプト、例を添えるプロンプト、JSON スキーマで出力の形を決める方法、検証とやり直し、まとめて処理する API、複数回の見直し |
| 5. コンテキストの管理と信頼性 | Context Management & Reliability | 15% | 約 9 問 | 6 | 長い会話で大事な情報を残す、人に引き継ぐ判断、エラーの伝え方、大きなコードの探索、人による確認、情報の出どころの管理 |

- 問題数の目安は、60 問に比重を掛けて、このサイトで計算したものです。試験ガイドによると、比重は「おおよその割合」なので、実際の問題数は前後します。
- 課題の数は、試験ガイドが出題分野ごとに挙げている、具体的な課題（Task Statement）の数です。

出題分野の日本語の名前は、このサイトでの訳です。

### 出題される場面

試験は、6 つの場面のうち 4 つが出題されます。試験ガイドは、場面ごとに、主に関わる出題分野を挙げています。

| 場面 | 主に関わる出題分野 |
|---|---|
| 問い合わせに答えるエージェント（Agent SDK と MCP の道具を使う） | 1、2、5 |
| Claude Code でのコードの作成 | 3、5 |
| 複数のエージェントによる調査 | 1、2、5 |
| 開発者の作業を助ける道具 | 2、3、1 |
| Claude Code を CI に組み込む | 3、4 |
| 文書からのデータの取り出し | 4、5 |

出題分野 5 は 4 つの場面に、1、2、3 は 3 つの場面に、4 は 2 つの場面に関わります。比重が 15% の出題分野 5 も、多くの場面で問われます。

試験ガイドは、試験に出ない内容も挙げています。たとえば、モデルの学習（ファインチューニング）、API の認証や料金の計算、画像の読み取り、ストリーミング、クラウドごとの設定などです。

### ページの構成

前の出題分野で身に付けたことが、次の出題分野の土台になる順番で学びます。

| 順番 | ページ | 出題分野 | この順番にした理由 | 状態 |
|---|---|---|---|---|
| 1 | [Claude Code の設定と使い方](./architect-3-claude-code) | 3 | 「Claude Code」のテーマの 01〜11 が、そのまま土台になる | <span class="nowrap">公開済み</span> |
| 2 | 道具の設計と MCP | 2 | 「Claude Code」のテーマの 08 で、MCP サーバーを作った。道具の作り方は、エージェントの前提になる | <span class="nowrap">準備中</span> |
| 3 | エージェントの設計と協調 | 1 | 比重がいちばん大きい。2 で学んだ道具を使って、エージェントを作る | <span class="nowrap">準備中</span> |
| 4 | プロンプトと構造化した出力 | 4 | 出力の形を決める方法の 1 つは、道具の呼び出しの形を使う。1 と 2 の知識を使う | <span class="nowrap">準備中</span> |
| 5 | コンテキストの管理と信頼性 | 5 | 1、2、4 をまたぐ内容が多い。全体の見直しを兼ねて、最後に学ぶ | <span class="nowrap">準備中</span> |

「Claude Code」のテーマのページと内容が重なるところは、そちらへのリンクで説明します。

## Developer – Foundations と Associate – Foundations

2026 年 11 月 17 日に公開される新しい試験ガイドを見てから、出題分野とページの構成を決めます。Architect – Foundations と重なる出題分野は、Architect のページへのリンクで済ませ、重ならない部分だけを新しく書く予定です。

## 教材

| 教材 | 使い方 |
|---|---|
| 公式の試験ガイド | 出題範囲の基準。Architect – Foundations の試験ガイドは、Anthropic Partner Academy の資格のページから入手できる |
| 公式ドキュメント（Claude Code Docs、Claude API のドキュメント） | 解説のページの内容を確かめる |
| Udemy の講座 | 英語の動画の講座と、演習問題 |

## 確認の記録

- [Claude Certification Program（Pearson VUE）](https://www.pearsonvue.com/us/en/anthropic.html)
- [Four role-based certifications for the people who put Claude to work for customers（claude.com）](https://claude.com/resources/articles/four-role-based-claude-certifications)
- [Who can take a Claude certification exam（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/page/certification-eligibility)
- [FAQ - Certifications（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/page/faq-certifications)
- [Claude Certified Architect – Foundations（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)

最終確認日：2026 年 10 月 26 日
