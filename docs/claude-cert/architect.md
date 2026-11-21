# Architect – Foundations：概要と出題分野

Claude Certified Architect – Foundations（CCAR-F）の試験の概要と、このテーマでのページの構成です。4 つの資格に共通することは、[Claude 認定資格](./)のページにまとめています。

## 試験の概要

公式の試験ガイド（Version 1.1、2026 年 11 月）による内容です。Version 1.0（2026 年 7 月）からの変更は、登録、本人確認、サポートの記述だけです（ガイドの改訂履歴による）。出題分野、比重、場面は、1.0 と同じです。

| 項目 | 内容 |
|---|---|
| 問題数 | 60 問 |
| 出題の形 | 実際の仕事を想定した 6 つの場面から、4 つが出題される。場面ごとに、いくつかの問題に答える |
| 想定している受験者 | Claude API、Agent SDK、Claude Code、MCP で、6 か月以上ものを作ってきたソリューションアーキテクト |
| 12 月 7 日の変更 | 対象外 |

## 出題分野

| 出題分野 | 英語での名前 | 比重 | 問題数の目安 | 課題の数 | 主な内容 |
|---|---|---|---|---|---|
| 1. エージェントの設計と協調 | Agentic Architecture & Orchestration | 27% | 約 16 問 | 7 | エージェントの作業の繰り返し、複数のエージェントの協調、サブエージェントへの情報の渡し方、Agent SDK のフック、セッションの再開と分岐 |
| 2. 道具の設計と MCP の組み込み | Tool Design & MCP Integration | 18% | 約 11 問 | 5 | 道具の説明の書き方、エラーの返し方、道具の振り分け、Claude Code への MCP の組み込み、組み込みの道具の使い分け |
| 3. Claude Code の設定と使い方 | Claude Code Configuration & Workflows | 20% | 約 12 問 | 6 | CLAUDE.md の階層、スラッシュコマンドとスキル、ファイルの場所ごとのルール、Plan モードの使いどころ、CI への組み込み |
| 4. プロンプトと構造化した出力 | Prompt Engineering & Structured Output | 20% | 約 12 問 | 6 | 判断の基準を明示したプロンプト、例を添えるプロンプト、JSON スキーマで出力の形を決める方法、検証とやり直し、まとめて処理する API、複数回の見直し |
| 5. コンテキストの管理と信頼性 | Context Management & Reliability | 15% | 約 9 問 | 6 | 長い会話で大事な情報を残す、人に引き継ぐ判断、エラーの伝え方、大きなコードの探索、人による確認、情報の出どころの管理 |

- 問題数の目安は、60 問に比重を掛けて、このサイトで計算したものです。試験ガイドによると、比重は「おおよその割合」なので、実際の問題数は前後します。
- 課題の数は、試験ガイドが出題分野ごとに挙げている、具体的な課題（Task Statement）の数です。
- 出題分野の日本語の名前は、このサイトでの訳です。

## 課題の一覧

試験ガイドは、5 つの出題分野に、全部で 30 の課題（Task Statement）を挙げています。出題分野ごとに、課題の名前を、このサイトで訳して並べます。解説は、出題分野ごとのページに、課題ごとの節として書きます。まだ書いていない課題は、「準備中」です。

この一覧は、試験ガイドの課題名の訳です。公式ドキュメントでの確認は、出題分野のページを書くときに行います。

### 出題分野 1：エージェントの設計と協調（7 課題）

この出題分野で使う言葉です。

- **エージェント**：Claude が、ツールを使いながら、次にやることを自分で決めて、仕事を進める仕組み。
- **エージェントループ**（agentic loop）：Claude に依頼を送り、Claude がツールの実行を求めたら、そのツールを動かして結果を返す、という繰り返し。試験ガイドは、Claude が返す `stop_reason`（止まった理由）が `tool_use` のときは続け、`end_turn` のときは終える、と説明しています。
- **サブエージェント**（subagent）：調整役（coordinator）のエージェントから、仕事の一部を任される、別の Claude。
- **Agent SDK**：Claude を使ったエージェントを、プログラムで作るための道具（Claude Agent SDK）。
- **フック**（hook）：ツールを呼び出す前後など、決まった場面で自動で動く処理。
- **セッション**：1 つの会話の流れ。あとから再開（resume）したり、途中から分岐（fork）させたりできる。

| 課題 | 内容 | 解説のページ | 状態 |
|---|---|---|---|
| 1.1 | エージェントループを設計して、実装する | — | <span class="nowrap">準備中</span> |
| 1.2 | 調整役とサブエージェントで、複数のエージェントを協調させる | — | <span class="nowrap">準備中</span> |
| 1.3 | サブエージェントの呼び出し、情報の渡し方、起動の設定をする | — | <span class="nowrap">準備中</span> |
| 1.4 | 手順の強制と、人への引き継ぎを組み込んだ、複数手順のワークフローを作る | — | <span class="nowrap">準備中</span> |
| 1.5 | Agent SDK のフックで、ツールの呼び出しの横取りと、データの整形を行う | — | <span class="nowrap">準備中</span> |
| 1.6 | 複雑なワークフローのために、作業の分け方の方針を決める | — | <span class="nowrap">準備中</span> |
| 1.7 | セッションの状態、再開、分岐を管理する | — | <span class="nowrap">準備中</span> |

### 出題分野 2：道具の設計と MCP の組み込み（5 課題）

この出題分野で使う言葉です。

- **ツール**（tool）：Claude が呼び出せる機能。名前、説明、受け取る値の形で定義する。
- **MCP**（Model Context Protocol）：Claude に、外部のツールやデータをつなぐための共通の決まり。つなぐ側のプログラムを、MCP サーバーと呼ぶ。
- **`isError`**：MCP のツールが、失敗したことを Claude に伝えるための印。
- **`tool_choice`**：Claude がどのツールを使うかを指定する設定。試験ガイドは、`"auto"`、`"any"`、特定のツールの指定を挙げています。
- **組み込みのツール**：Claude Code が最初から持っている道具（Read、Write、Edit、Bash、Grep、Glob）。

| 課題 | 内容 | 解説のページ | 状態 |
|---|---|---|---|
| 2.1 | 説明と境界がはっきりした、ツールの形（インターフェース）を設計する | — | <span class="nowrap">準備中</span> |
| 2.2 | MCP のツールが、構造化したエラーを返すようにする | — | <span class="nowrap">準備中</span> |
| 2.3 | ツールをエージェントに適切に振り分け、`tool_choice` を設定する | — | <span class="nowrap">準備中</span> |
| 2.4 | MCP サーバーを、Claude Code とエージェントのワークフローに組み込む | — | <span class="nowrap">準備中</span> |
| 2.5 | 組み込みのツールを、場面に合わせて選んで使う | — | <span class="nowrap">準備中</span> |

### 出題分野 3：Claude Code の設定と使い方（6 課題）

| 課題 | 内容 | 解説のページ | 状態 |
|---|---|---|---|
| 3.1 | CLAUDE.md を、階層、範囲、分け方を考えて設定する | [分野 3](./architect-3-claude-code)、[3.1 の詳しいページ](./architect-3-1-claude-md) | <span class="nowrap">公開済み</span> |
| 3.2 | スラッシュコマンドとスキルを作って設定する | [分野 3](./architect-3-claude-code) | <span class="nowrap">公開済み</span> |
| 3.3 | ファイルの場所ごとのルールで、決まりを必要なときだけ読み込ませる | [分野 3](./architect-3-claude-code) | <span class="nowrap">公開済み</span> |
| 3.4 | Plan モードと、直接の実行を使い分ける | [分野 3](./architect-3-claude-code) | <span class="nowrap">公開済み</span> |
| 3.5 | 少しずつ良くしていく進め方を使う | [分野 3](./architect-3-claude-code) | <span class="nowrap">公開済み</span> |
| 3.6 | Claude Code を CI/CD の仕組みに組み込む | [分野 3](./architect-3-claude-code) | <span class="nowrap">公開済み</span> |

### 出題分野 4：プロンプトと構造化した出力（6 課題）

この出題分野で使う言葉です。

- **構造化した出力**：決まった形（JSON など）で返させる出力。
- **JSON スキーマ**：JSON の形（項目の名前、種類、必須かどうか）を定める書き方。
- **few-shot**（少数の例）：プロンプトに、入力と望ましい出力の例を、数個添える方法。
- **誤検出**（false positive）：問題がないのに、「問題がある」と指摘してしまうこと。
- **Message Batches API**：すぐの返答を求めない依頼を、まとめて処理する API。

| 課題 | 内容 | 解説のページ | 状態 |
|---|---|---|---|
| 4.1 | 判断の基準を明示したプロンプトで、精度を上げ、誤検出を減らす | — | <span class="nowrap">準備中</span> |
| 4.2 | 少数の例を添えて、出力の一貫性と品質を上げる | — | <span class="nowrap">準備中</span> |
| 4.3 | ツールの利用と JSON スキーマで、構造化した出力を守らせる | — | <span class="nowrap">準備中</span> |
| 4.4 | 検証、やり直し、フィードバックの繰り返しで、取り出しの品質を上げる | — | <span class="nowrap">準備中</span> |
| 4.5 | 効率のよい、まとめて処理する方法を設計する | — | <span class="nowrap">準備中</span> |
| 4.6 | 複数のインスタンス、複数回に分けた見直しの仕組みを設計する | — | <span class="nowrap">準備中</span> |

### 出題分野 5：コンテキストの管理と信頼性（6 課題）

この出題分野で使う言葉です。

- **コンテキスト**（context）：Claude が、その時点で読める情報の全体。会話の履歴や、ツールの結果などを含む。
- **エスカレーション**：Claude が対応を続けず、人に引き継ぐこと。
- **確信度**：Claude の答えを、どれくらい信頼してよいかの度合い。
- **情報の出どころ**（provenance）：ある主張が、どの情報源のどの部分に基づくかという記録。

| 課題 | 内容 | 解説のページ | 状態 |
|---|---|---|---|
| 5.1 | 長い対話でも、大事な情報が残るように、コンテキストを管理する | — | <span class="nowrap">準備中</span> |
| 5.2 | 人への引き継ぎと、曖昧な依頼の解決のパターンを設計する | — | <span class="nowrap">準備中</span> |
| 5.3 | 複数のエージェントの間で、エラーをどう伝えるかの方針を実装する | — | <span class="nowrap">準備中</span> |
| 5.4 | 大きなコードベースの調査で、コンテキストを管理する | — | <span class="nowrap">準備中</span> |
| 5.5 | 人が確認するワークフローと、確信度の調整を設計する | — | <span class="nowrap">準備中</span> |
| 5.6 | 複数の情報源をまとめるとき、情報の出どころを残し、不確かさを扱う | — | <span class="nowrap">準備中</span> |

## 出題される場面

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

## ページの構成

出題分野ごとに、入口のページ（全体の見取り図、実際にやってみる、確認問題）を置き、その下に、試験ガイドの課題ごとの詳しいページを置きます。

前の出題分野で身に付けたことが、次の出題分野の土台になる順番で学びます。

| 順番 | ページ | 出題分野 | この順番にした理由 | 状態 |
|---|---|---|---|---|
| 1 | [Claude Code の設定と使い方](./architect-3-claude-code) | 3 | 「Claude Code」のテーマの 01〜11 が、そのまま土台になる | <span class="nowrap">公開済み</span> |
| 2 | 道具の設計と MCP | 2 | 「Claude Code」のテーマの 08 で、MCP サーバーを作った。道具の作り方は、エージェントの前提になる | <span class="nowrap">準備中</span> |
| 3 | エージェントの設計と協調 | 1 | 比重がいちばん大きい。2 で学んだ道具を使って、エージェントを作る | <span class="nowrap">準備中</span> |
| 4 | プロンプトと構造化した出力 | 4 | 出力の形を決める方法の 1 つは、道具の呼び出しの形を使う。1 と 2 の知識を使う | <span class="nowrap">準備中</span> |
| 5 | コンテキストの管理と信頼性 | 5 | 1、2、4 をまたぐ内容が多い。全体の見直しを兼ねて、最後に学ぶ | <span class="nowrap">準備中</span> |

出題分野 3 のページには、6 つの課題すべての解説があります。課題 3.1 は、実際にやってみた結果を加えた詳しいページも、別にあります（[CLAUDE.md の階層と整理](./architect-3-1-claude-md)）。

ほかの出題分野も、出題分野ごとに 1 つのページを作り、課題を節として並べます。課題ごとにページを分けるのは、必要になったときだけにします。

「Claude Code」のテーマのページと内容が重なるところは、そちらへのリンクで説明します。

## 教材

### 公式の準備コース（Anthropic Partner Academy）

Partner Academy の「Claude Certified Architect – Foundations Prep Courses」のページは、無料のコースとして、次の 7 つを挙げています（2026 年 11 月 22 日に確認）。

- AI Fluency: Framework & Foundations
- Building with the Claude API
- Claude on Google Cloud
- Claude Code in Action
- Claude 101
- Claude with Amazon Bedrock
- Introduction to Model Context Protocol

コースの中身は、まだ見ていません。試験ガイドは、特定のクラウドの設定を、試験に出ない内容としています。このため、「Claude on Google Cloud」と「Claude with Amazon Bedrock」は、優先度が低いと、このサイトでは見ています。

### Claude Academy

Claude Academy の、この試験に関わるコースです。どの出題分野に当たるかは、コースの説明とレッスンの題名から、このサイトで判断しました。

| コース | 時間 | 主に関わる出題分野 |
|---|---|---|
| Claude Code 101 | 1.5 時間 | 3 |
| Claude Codeを実践する | 1 時間 | 3 |
| サブエージェント入門 | 45 分 | 1、3 |
| Agent Skills入門 | 1 時間 | 3 |
| Model Context Protocol入門 | 1 時間 | 2 |
| Model Context Protocol: 高度なトピック | 1.5 時間 | 2 |
| Claude APIを使った構築 | 9 時間 | 1、2、4、5。プロンプトの評価、プロンプトの書き方、構造化した出力、道具の使い方、エージェントとワークフローの章がある。進めるには、Claude API のキーが要る |

Udemy の日本語の講座は、出題分野ごとに次のものを使います。出題分野 4 に合う講座は、見つかっていません。

| 出題分野 | 講座 |
|---|---|
| 1 | AIマルチエージェント入門（我妻） |
| 2 | MCPがわかる・使える・作れる！（桑井） |
| 3 | Claude Code カスタマイズ完全ガイド（とまだ） |
| 5 | 実践 Claude Code ハーネス設計完全ガイド（石田） |

## 確認の記録

- Claude Certified Architect – Foundations Exam Guide（Version 1.1、2026 年 11 月。Anthropic Partner Academy で公開）
- [Claude Certified Architect – Foundations（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)
- [Claude Certified Architect – Foundations Prep Courses（Anthropic Partner Academy）](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
- [Claude Academy のコースの一覧](https://academy.claude.com/ja/courses)

最終確認日：2026 年 11 月 22 日（試験ガイドの版、出題分野の比重、場面、課題の名前、準備コースの一覧）。教材の対応表は、2026 年 10 月 28 日のままです。
