# Claude 認定資格

Anthropic が実施している Claude の認定資格に向けた学習ノートです。公式の試験ガイドをもとに、試験ごと、出題分野ごとにまとめていきます。

::: warning 掲載ルール
このテーマのページには、試験問題やその再現、試験ガイドの例題は載せません。公式ドキュメントで確認した内容と、実際に試した結果をもとにした説明だけを載せます。確認問題は、すべて自作です。
:::

## Claude の認定資格とは

Claude の認定資格は、Claude を使った仕事の力を確かめる、Anthropic の公式の資格です。2026 年 7 月に、4 つの資格がそろいました。

| 資格 | 試験コード | 対象 | 主な範囲 |
|---|---|---|---|
| Claude Certified Associate – Foundations | CCAO-F | 仕事の道具として Claude を使う人。技術者でなくてもよい | 日常の業務での Claude の使い方、プロンプト、出力の確かめ方、製品やモデルの選び方、責任ある使い方 |
| Claude Certified Developer – Foundations | CCDV-F | 開発者 | Claude API、エージェントの開発、MCP サーバーの開発、評価とデバッグ、セキュリティ |
| Claude Certified Architect – Foundations | CCAR-F | ソリューションアーキテクト（システムの設計を担う人） | Claude Code の設定、Claude Agent SDK、Claude API、MCP、複数のエージェントの協調 |
| Claude Certified Architect – Professional | CCAR-P | 経験のあるアーキテクト | 本番で動かすシステムの設計、システム間の連携、評価、ガバナンス、関係者との調整 |

このテーマでは、4 つすべてを扱います。

### 4 つに共通すること

| 項目 | 内容 |
|---|---|
| 試験時間 | 120 分。受付などを含めると、全体で約 135 分 |
| 問題の形式 | 選択式。答えを 1 つ選ぶ問題と、複数選ぶ問題がある。何個選ぶかは、問題に書かれている |
| 合格点 | 100〜1,000 点の換算点で、720 点以上 |
| 成績表 | 合否と換算点に加えて、出題分野ごとの正答率 |
| 受験の方法 | オンライン受験（試験官が画面越しに見張る）、または Pearson の試験会場 |
| 言語 | 英語と日本語 |
| 受け直し | 不合格のあと、1 回目は 14 日、2 回目は 30 日、3 回目は 90 日あける。1 つの試験につき、12 か月で 4 回まで |
| 有効期限 | 合格から 12 か月。期限内の更新は、無料の確認テストで行う |
| 受験できる人 | Claude Partner Network（Anthropic のパートナー企業の集まり）に加盟している組織で働く人。会社のメールアドレスで登録する |

### 12 月 7 日の内容の変更

2026 年 12 月 7 日から、Associate、Developer、Architect – Professional の 3 つは、試験の内容が新しくなります。新しい試験ガイドは、11 月 17 日に公開されます。Architect – Foundations は、この変更の対象外です。

## 学習の進め方

1 つの出題分野を、次の 3 つの段階で学びます。

| 段階 | すること |
|---|---|
| ① 解説を読む | このテーマの解説のページで、出題分野の内容を学ぶ。公式ドキュメントで確かめた内容と、このサイトのリポジトリで試した結果をまとめる |
| ② 教材で確かめる | Anthropic の公式の学習サイト「Claude Academy」のコースで、同じ出題分野を学ぶ。足りないところは、日本語の Udemy の講座で補う |
| ③ 問題を解く | 確認問題と、模擬試験を解く。間違えた出題分野は、① に戻って見直す |

試験は日本語でも受けられますが、問題は英語から訳されたものです。訳の違いに気づけるように、各ページには、出題分野でよく使われる用語の英語と日本語を並べた表を付けます。

## 受ける順番

| 順番 | 試験 | この順番にした理由 |
|---|---|---|
| 1 | Associate – Foundations | 4 つの中でいちばんやさしい。試験の形式に、先に慣れられる |
| 2 | Architect – Foundations | 「Claude Code」のテーマの 01〜11 が、そのまま土台になる。12 月 7 日の変更の対象外 |
| 3 | Developer – Foundations | Architect – Foundations と範囲が重なる。新しい試験ガイドで学ぶ |
| 4 | Architect – Professional | 上の 3 つの内容を土台にして、本番で動かすシステムの設計を学ぶ。新しい試験ガイドで学ぶ |

## 試験ごとのページ

| 試験 | ページ | 状態 |
|---|---|---|
| Associate – Foundations | [概要と出題分野](./associate) | <span class="nowrap">準備中</span> |
| Architect – Foundations | [概要と出題分野](./architect) | <span class="nowrap">執筆中</span> |
| Developer – Foundations | 11 月 17 日の新しい試験ガイドを見てから作る | <span class="nowrap">準備中</span> |
| Architect – Professional | 11 月 17 日の新しい試験ガイドを見てから作る | <span class="nowrap">準備中</span> |

ほかの試験と重なる出題分野は、そのページへのリンクで済ませ、重ならない部分だけを新しく書きます。

## 教材

| 教材 | 使い方 |
|---|---|
| 公式の試験ガイド | 出題範囲の基準。Anthropic Partner Academy の資格のページで、4 つとも公開されている |
| [Claude Academy](https://academy.claude.com/ja) | Anthropic の公式の学習サイト。日本語で読める。無料で、コースごとに修了のバッジがもらえる |
| 公式ドキュメント（Claude Code Docs、Claude API のドキュメント、claude.ai のヘルプ） | 解説のページの内容を確かめる |
| Udemy の講座 | Claude Academy で足りないところを補う。日本語の講座を使う |

## 確認の記録

- [Claude Certification Program（Pearson VUE）](https://www.pearsonvue.com/us/en/anthropic.html)
- [Four role-based certifications for the people who put Claude to work for customers（claude.com）](https://claude.com/resources/articles/four-role-based-claude-certifications)
- [Who can take a Claude certification exam（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/page/certification-eligibility)
- [FAQ - Certifications（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/page/faq-certifications)
- [Partner certifications（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/page/partner-certifications)
- [Claude Academy のコースの一覧](https://academy.claude.com/ja/courses)
- 各試験の Exam Guide（Version 1.0、2026 年 7 月）

最終確認日：2026 年 10 月 28 日
