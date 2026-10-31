# Associate – Foundations：概要と出題分野

Claude Certified Associate – Foundations（CCAO-F）の試験の概要と、このテーマでのページの構成です。4 つの資格に共通することは、[Claude 認定資格](./)のページにまとめています。

## 試験の概要

公式の試験ガイド（Version 1.0、2026 年 7 月）による内容です。

| 項目 | 内容 |
|---|---|
| 問題数 | 60 問 |
| 想定している受験者 | 運用、マーケティング、プロジェクト管理、教育、広報などの仕事で、Claude を道具として使い、Claude の Projects を作る人 |
| 求められる技術の知識 | 限られた〜中程度。プログラムの開発や API の経験は要らない |
| 対象外の人 | API で開発する人、エージェントの仕組みを設計する人。それは Developer と Architect の範囲で、Associate は、そうした難しい仕事を、その人たちに引き継ぐ側とされている |
| 12 月 7 日の変更 | 対象。この試験ガイドは、12 月 6 日までの試験の内容 |

## 出題分野

| 出題分野 | 英語での名前 | 比重 | 問題数の目安 | 主な内容 |
|---|---|---|---|---|
| 1. プロンプト作成とタスク実行 | Prompting and Task Execution | 14% | 約 8 問 | 仕事の依頼の書き方、複雑な依頼の分け方、やり直して良くする方法、作業の種類（分析、調査、下書き、アイデア出し）に合わせた書き方 |
| 2. 出力の評価と検証 | Output Evaluation and Validation | 21% | 約 13 問 | 正しさと抜けの確認、事実と違う内容や偏りの見つけ方、事実の確かめ方、人の確認が要る場面、読み手に合わせた直し方、出力の形の選び方 |
| 3. 製品とモデルの選択 | Product and Model Selection | 12% | 約 7 問 | 機能（Projects、リサーチ、チャット、Artifacts）の選び方、Haiku・Sonnet・Opus の違いと選び方、会話の長さの限界と、やり直す・要約する・残すの判断 |
| 4. ワークフロー統合とソリューション設計 | Workflow Integration and Solution Design | 16% | 約 10 問 | 要件の分析、調査と計画、解決策の設計の手伝い、今の業務への組み込み、Claude の価値と限界の説明 |
| 5. 設定とナレッジ管理 | Configuration and Knowledge Management | 12% | 約 7 問 | Projects の指示と資料、アップロードした資料とコネクター（Google Drive など）、全体に効く指示の書き方、設定の見直し |
| 6. ガバナンス、リスク、責任ある利用 | Governance, Risk, and Responsible Use | 15% | 約 9 問 | 向く使い方と向かない使い方、機密のデータ・法律・プライバシーへの配慮、組織の方針に従うこと、倫理の問題 |
| 7. トラブルシューティングと最適化 | Troubleshooting and Optimization | 10% | 約 6 問 | うまくいかないプロンプトや出力の原因を探って直す、結果に応じたやり方の調整、業務の効率化 |

- 問題数の目安は、60 問に比重を掛けて、このサイトで計算したものです。実際の問題数は前後します。
- 出題分野の日本語の名前は、日本語版の試験ガイドに合わせています。主な内容は、このサイトでの要約です。
- 「事実と違う内容」は、AI がもっともらしい誤りを作ることで、英語では hallucination（ハルシネーション）と呼ばれます。

Architect – Foundations と違い、場面ごとの出題ではありません。

### 注意が要る出題分野

出題分野 3 と 5 は、Claude Code ではなく、claude.ai（ブラウザーやアプリで使う Claude）の機能が中心です。このサイトの「[Claude Code](../claude-code/)」のテーマでは扱っていないので、claude.ai で実際に触って確かめます。

## ページの構成

出題分野ごとに 1 ページを書きます。成績表は出題分野ごとの正答率で出るので、ページと出題分野を 1 対 1 にして、見直す場所を探しやすくします。

比重の大きい順に書きます。

| 順番 | ページ | 出題分野 | 比重 | 状態 |
|---|---|---|---|---|
| 1 | [出力の評価と検証](./associate-2-output-evaluation) | 2 | 21% | <span class="nowrap">公開済み</span> |
| 2 | [ワークフロー統合とソリューション設計](./associate-4-workflow-integration) | 4 | 16% | <span class="nowrap">公開済み</span> |
| 3 | [ガバナンス、リスク、責任ある利用](./associate-6-governance) | 6 | 15% | <span class="nowrap">公開済み</span> |
| 4 | [プロンプト作成とタスク実行](./associate-1-prompting) | 1 | 14% | <span class="nowrap">公開済み</span> |
| 5 | [製品とモデルの選択](./associate-3-product-model-selection) | 3 | 12% | <span class="nowrap">公開済み</span> |
| 6 | 設定とナレッジ管理 | 5 | 12% | <span class="nowrap">準備中</span> |
| 7 | トラブルシューティングと最適化 | 7 | 10% | <span class="nowrap">準備中</span> |

## 教材

Claude Academy の、この試験に関わるコースです。どの出題分野に当たるかは、コースの説明とレッスンの題名から、このサイトで判断しました。

| コース | 時間 | 主に関わる出題分野 |
|---|---|---|
| Claude 101 | 2.5 時間 | 1、3、4、5。最初の会話、プロンプト、Projects、Artifacts、Skills、コネクター、リサーチ、職種ごとの使い方 |
| AI活用力：フレームワーク&基礎 | 4 時間 | 1、2、4、6。AI との協働の 4 つの力（委任力、記述力、評価力、倫理的責任。4D フレームワーク）を学ぶ |
| AIの能力と限界 | 3.5 時間 | 2、3、7。もっともらしい誤りが生まれる理由、知識の限界、会話の長さの限界、指示が効きにくい場面と、予期しない出力の原因の探り方 |

## 確認の記録

- Claude Certified Associate – Foundations Exam Guide（Version 1.0、2026 年 7 月。Anthropic Partner Academy で公開）
- [Claude Certified Associate – Foundations（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/claude-certified-associate-foundations-certification)
- [Claude 101（Claude Academy）](https://academy.claude.com/ja/courses/claude-101)
- [Claude Academy のコースの一覧](https://academy.claude.com/ja/courses)

最終確認日：2026 年 10 月 28 日
