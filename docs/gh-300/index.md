# GH-300（GitHub Copilot）

GitHub Copilot の認定試験 GH-300 に向けた学習ノートです。公式の試験範囲をもとに、1 ページ 1 主題でまとめています。

::: warning 掲載ルール
GitHub の認定試験は、出題内容に守秘義務があります。このテーマのページには、試験問題やその再現は載せません。公式ドキュメントで確認した内容と、自分の理解をもとにした説明だけを載せます。確認問題は、すべて自作です。
:::

## 学習の状況（2026 年 10 月 31 日時点：休止中）

::: info 更新を休止しています
Claude の認定資格の学習を優先するため、2026 年 10 月 31 日から、GH-300 の学習とこのテーマの更新を休止しています。公開済みの 5 ページ（03、10、12、13、14）は、そのまま読めます。残りのページは、再開したあとに順に公開します。再開の時期は未定です。
:::

### 学習した領域

| 領域 | 学習した内容 | 状況 |
|---|---|---|
| 責任ある AI（Responsible AI） | 公平性、安全性、プライバシーなどの 6 つの原則 | 完了 |
| GitHub Copilot の概要 | チャット、コードの補完、プルリクエストの支援、CLI、Spaces など | 学習済み |
| Copilot のプラン | 個人向けと企業向けのプランの種類と違い | 学習済み |
| エージェントモードの基礎 | 自律的なコードの編集、テスト、繰り返しの修正 | 完了 |
| 自律的な開発支援 | 複数の工程の調整、ひな形の生成、自己修復 | 完了 |
| GitHub スキルの演習 | エージェントモードを実際に使う演習 | 次に再開する位置 |

エージェントモード（Agent Mode）は、GitHub Copilot が、複数の手順からなる作業を自分で進める機能です。表の下の 3 行は、Microsoft Learn の **<span class="nowrap">Part 2-1</span>**（GitHub Copilot エージェント モードを使用したアプリケーションのビルド）の単元です。

この表は、Microsoft Learn の教材で学習した範囲の記録です。公式の試験範囲全体に対する進み具合ではありません。

### 直近で学んだ用語

| 用語 | 意味 |
|---|---|
| 複数ステップの作業（Multi-step Tasks） | 複雑な作業を、複数の手順に分けて進めること |
| オーケストレーション（Orchestration） | 作業やツールを連携させ、調整すること |
| スキャフォールディング（Scaffolding） | プロジェクトのひな形を生成すること |
| コンテキストの認識（Context Awareness） | 既存のコードや依存関係を理解すること |
| 自己修復（Self-healing） | エラーを見つけて直し、もう一度確かめること |
| 人間による監督（Human Oversight） | 最終的な判断を、人間が行うこと |

要点：エージェントモードは、コードを生成するだけではありません。分析 → 編集 → 実行 → 検証 → 修正を、自分で繰り返します。

用語の意味は、教材で学んだときのメモです。各ページを書くときに、公式ドキュメントで確かめます。

## GH-300 とは

GH-300 は、GitHub Copilot（開発者の作業を支援する AI ツール）を使いこなす力を問う認定試験です。公式の学習ガイドでは、対象者を次のように説明しています。

- GitHub Copilot を使って、ソフトウェア開発の生産性・品質・セキュリティを高められる
- 責任ある AI の使い方、プロンプトエンジニアリング、プランごとの機能、プライバシーの保護について理解している
- GitHub の基礎を理解していて、1 つ以上のプログラミング言語の経験がある

合格には、700 点以上が必要です。出題の多くは一般提供（GA）されている機能についてですが、広く使われているプレビュー機能が出題されることもあります。

## 試験範囲

公式の学習ガイド（2026 年 8 月 7 日適用版）による、出題分野と比重です。

| 出題分野 | 英語での名前 | 比重 |
|---|---|---|
| GitHub Copilot を責任を持って使用する | Use GitHub Copilot responsibly | 15〜20% |
| GitHub Copilot の機能を使用する | Use GitHub Copilot features | 25〜30% |
| GitHub Copilot のデータとアーキテクチャを理解する | Understand GitHub Copilot data and architecture | 10〜15% |
| プロンプトエンジニアリングとコンテキストの作成を適用する | Apply prompt engineering and context crafting | 10〜15% |
| GitHub Copilot で開発者の生産性を向上させる | Improve developer productivity with GitHub Copilot | 10〜15% |
| プライバシー、コンテンツの除外、セーフガードを構成する | Configure privacy, content exclusions, and safeguards | 10〜15% |

出題分野の日本語の名前は、このサイトでの訳です。

試験範囲は改訂されることがあります。受験の前に、公式の学習ガイドで最新の内容を確認してください。

## ページの構成

ページは、**公式の試験範囲（6 つの出題分野）をもとに**、5 部・18 ページに分けています。これに加えて、Microsoft Learn の教材にはあるものの、試験範囲の項目には直接対応しない内容を、補足の部（第 6 部・3 ページ）にまとめます。書けたページから順に公開しています。

「MS Learn の対応モジュール」の列は、そのページの内容に対応する、Microsoft Learn のトレーニングパスのモジュールです。「Part 1-3」は、「Part 1 の 3 番目のモジュール」という意味です。モジュールのタイトルは、Microsoft Learn の日本語のサイトに表示されているとおりに書いています。

### 第 1 部：基礎と責任ある AI

| # | ページ | 出題分野 | MS Learn の対応モジュール | 状態 |
|---|---|---|---|---|
| 01 | GitHub Copilot とは何か | 機能、生産性 | **<span class="nowrap">Part 1-2</span>**　GitHub Copilot の概要 | <span class="nowrap">準備中</span> |
| 02 | GitHub Copilot のプランと利用環境 | 機能、プライバシー | **<span class="nowrap">Part 1-2</span>**　GitHub Copilot の概要<br>**<span class="nowrap">Part 1-7</span>**　GitHub Copilot での管理とカスタマイズに関する考慮事項 | <span class="nowrap">準備中</span> |
| 03 | [責任ある AI の 6 つの原則](./03-responsible-ai-principles) | 責任ある使用 | **<span class="nowrap">Part 1-1</span>**　GitHub Copilot を使用した責任ある AI | <span class="nowrap">公開済み</span> |
| 04 | AI 生成コードのリスクと検証 | 責任ある使用 | **<span class="nowrap">Part 1-1</span>**　GitHub Copilot を使用した責任ある AI<br>**<span class="nowrap">Part 1-8</span>**　GitHub Copilot を使用した AI の開発者ユース ケース | <span class="nowrap">準備中</span> |

### 第 2 部：Copilot の機能と操作

| # | ページ | 出題分野 | MS Learn の対応モジュール | 状態 |
|---|---|---|---|---|
| 05 | IDE での Copilot の基本操作 | 機能 | **<span class="nowrap">Part 1-2</span>**　GitHub Copilot の概要<br>**<span class="nowrap">Part 1-6</span>**　環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ | <span class="nowrap">準備中</span> |
| 06 | GitHub Copilot Chat の活用 | 機能、プロンプト | **<span class="nowrap">Part 1-5</span>**　高度な GitHub Copilot の機能の使用<br>**<span class="nowrap">Part 1-6</span>**　環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ | <span class="nowrap">準備中</span> |
| 07 | Agent Mode と自律的な開発支援 | 機能 | **<span class="nowrap">Part 2-1</span>**　GitHub Copilot エージェント モードを使用したアプリケーションのビルド<br>**<span class="nowrap">Part 2-2</span>**　GitHub Copilot クラウド エージェントを使用して開発を加速する<br>**<span class="nowrap">Part 2-3</span>**　MCP サーバーの概要 | <span class="nowrap">準備中</span> |
| 08 | GitHub Copilot CLI | 機能 | **<span class="nowrap">Part 1-6</span>**　環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ | <span class="nowrap">準備中</span> |
| 09 | GitHub 上の Copilot 機能 | 機能 | **<span class="nowrap">Part 1-4</span>**　コピロット空間の概要<br>**<span class="nowrap">Part 1-6</span>**　環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ<br>**<span class="nowrap">Part 2-4</span>**　GitHub Copilot を使用したコード レビューと pull request の平準化 | <span class="nowrap">準備中</span> |

### 第 3 部：プロンプトと内部の仕組み

| # | ページ | 出題分野 | MS Learn の対応モジュール | 状態 |
|---|---|---|---|---|
| 10 | [プロンプトエンジニアリングの基本](./10-prompt-engineering-basics) | プロンプト | **<span class="nowrap">Part 1-3</span>**　GitHub Copilot を使用したプロンプト エンジニアリングの概要 | <span class="nowrap">公開済み</span> |
| 11 | コンテキスト設計とプロンプトの高度化 | プロンプト | **<span class="nowrap">Part 1-3</span>**　GitHub Copilot を使用したプロンプト エンジニアリングの概要<br>**<span class="nowrap">Part 1-6</span>**　環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ | <span class="nowrap">準備中</span> |
| 12 | [GitHub Copilot の仕組みとデータフロー](./12-copilot-data-flow) | データとアーキテクチャ | **<span class="nowrap">Part 1-3</span>**　GitHub Copilot を使用したプロンプト エンジニアリングの概要 | <span class="nowrap">公開済み</span> |

### 第 4 部：プライバシーと管理

| # | ページ | 出題分野 | MS Learn の対応モジュール | 状態 |
|---|---|---|---|---|
| 13 | [GitHub Copilot のプライバシーとデータ保護](./13-privacy-and-content-exclusion) | プライバシー、機能 | **<span class="nowrap">Part 1-7</span>**　GitHub Copilot での管理とカスタマイズに関する考慮事項 | <span class="nowrap">公開済み</span> |
| 14 | [生成コードの著作権と安全対策](./14-ip-and-safeguards) | プライバシー | **<span class="nowrap">Part 1-7</span>**　GitHub Copilot での管理とカスタマイズに関する考慮事項 | <span class="nowrap">公開済み</span> |
| 15 | 組織での Copilot の管理とガバナンス | 機能 | **<span class="nowrap">Part 1-7</span>**　GitHub Copilot での管理とカスタマイズに関する考慮事項 | <span class="nowrap">準備中</span> |

### 第 5 部：開発への応用と総復習

| # | ページ | 出題分野 | MS Learn の対応モジュール | 状態 |
|---|---|---|---|---|
| 16 | Copilot による開発生産性の向上 | 生産性 | **<span class="nowrap">Part 1-8</span>**　GitHub Copilot を使用した AI の開発者ユース ケース | <span class="nowrap">準備中</span> |
| 17 | Copilot によるテストと品質向上 | 生産性 | **<span class="nowrap">Part 1-9</span>**　GitHub Copilot ツールを使用して単体テストを開発する | <span class="nowrap">準備中</span> |
| 18 | GH-300 学習の総まとめと機能選択ガイド | 全分野 | — | <span class="nowrap">準備中</span> |

### 第 6 部：MS Learn の補足

Microsoft Learn の教材で扱われているものの、公式の試験範囲の項目には、直接は挙げられていない内容です。試験範囲にもとづく第 1 部〜第 5 部とは、区別して置いています。

| # | ページ | 出題分野 | MS Learn の対応モジュール | 状態 |
|---|---|---|---|---|
| 19 | GitHub Copilot アプリ | — | **<span class="nowrap">Part 1-6</span>**　環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ（「GitHub Copilot アプリ」の単元） | <span class="nowrap">準備中</span> |
| 20 | JavaScript での GitHub Copilot の利用 | — | **<span class="nowrap">Part 2-5</span>**　JavaScript で GitHub Copilot を使う | <span class="nowrap">準備中</span> |
| 21 | Python での GitHub Copilot の利用 | — | **<span class="nowrap">Part 2-6</span>**　Python で GitHub Copilot を使用する | <span class="nowrap">準備中</span> |

「出題分野」の列は、分野の名前を短くして書いています。

## 試験範囲のチェック表

公式の学習ガイドに載っている項目ごとに、どのページで扱うかをまとめた表です。まだ扱えていない項目が、一目で分かるようにしています。

公式の学習ガイドには、「項目は、何を評価するかを示す例で、関連する内容が出題されることがある」という注意書きがあります。この表の項目をすべて扱っても、試験範囲を完全に覆ったことにはなりません。

### GitHub Copilot を責任を持って使用する（15〜20%）

| 公式の項目 | ページ | 状態 |
|---|---|---|
| 生成 AI ツールのリスクと限界を説明する | 03、04 | <span class="nowrap">一部を公開済み</span>（03） |
| 倫理的で、責任ある AI の使い方を説明する | 03 | <span class="nowrap">公開済み</span> |
| AI を使うことで起こりうる害と、その軽減策を特定する | 03、04 | <span class="nowrap">一部を公開済み</span>（03） |
| AI の出力を検証する必要性を説明する | 04 | <span class="nowrap">準備中</span> |
| GitHub Copilot を責任を持って運用する方法を特定する | 04 | <span class="nowrap">準備中</span> |

### GitHub Copilot の機能を使用する（25〜30%）

| 公式の項目 | ページ | 状態 |
|---|---|---|
| IDE で Copilot を有効にする | 05 | <span class="nowrap">準備中</span> |
| インラインの提案、チャット、CLI、エージェントモードで Copilot を呼び出す | 05、06、07、08 | <span class="nowrap">準備中</span> |
| 特定のファイルやリポジトリに、コンテンツの除外を設定する | 13 | <span class="nowrap">公開済み</span> |
| GitHub Copilot CLI（定義と利点、インストールの手順、主な機能とコマンド、対話的な使い方とセッション、スクリプトの生成とファイルの管理） | 08 | <span class="nowrap">準備中</span> |
| エージェントモード、Copilot Edits、MCP を使う。エージェントのセッションを管理し、サブエージェントに作業を任せる | 07 | <span class="nowrap">準備中</span> |
| コードレビューと、コーディングの支援に Copilot を使う | 09 | <span class="nowrap">準備中</span> |
| Spaces、Spark、プルリクエストの要約、指示ファイルによるレビュー基準のカスタマイズを使う | 09 | <span class="nowrap">準備中</span> |
| Copilot Chat の制限、オプション、フィードバック、コマンドを理解する。プロンプトファイルを再利用する | 06 | <span class="nowrap">準備中</span> |
| 組織全体の方針の管理を設定する。Copilot のコードレビューの方針を有効にし、IDE と github.com での機能の利用可否を管理する | 15 | <span class="nowrap">準備中</span> |
| 監査ログのイベントを使う | 15 | <span class="nowrap">準備中</span> |
| REST API で、サブスクリプションを管理する | 15 | <span class="nowrap">準備中</span> |

### GitHub Copilot のデータとアーキテクチャを理解する（10〜15%）

| 公式の項目 | ページ | 状態 |
|---|---|---|
| データの使われ方、流れ、共有について説明する | 12 | <span class="nowrap">公開済み</span> |
| 入力の処理と、プロンプトの組み立てについて説明する | 12 | <span class="nowrap">公開済み</span> |
| プロキシでのフィルターと、後処理について説明する | 12 | <span class="nowrap">公開済み</span> |
| コードの提案が作られて、届くまでの流れを図で理解する | 12 | <span class="nowrap">公開済み</span> |
| LLM と Copilot の限界を説明する | 12、04 | <span class="nowrap">一部を公開済み</span>（12 で、コンテキストウィンドウの制限だけを扱った） |

### プロンプトエンジニアリングとコンテキストの作成を適用する（10〜15%）

| 公式の項目 | ページ | 状態 |
|---|---|---|
| プロンプトの構造と、コンテキストについて説明する | 10、11 | <span class="nowrap">一部を公開済み</span>（10） |
| コンテキストがどのように決まるかを理解する | 11、12 | <span class="nowrap">一部を公開済み</span>（12 で、集められるコンテキストを扱った） |
| ゼロショットと、少数ショットのプロンプトを使う | 10 | <span class="nowrap">公開済み</span> |
| プロンプトの作成の、ベストプラクティスを適用する | 10 | <span class="nowrap">公開済み</span> |
| プロンプトエンジニアリングの原則を説明する | 10 | <span class="nowrap">公開済み</span> |
| プロンプトの処理の流れと、チャット履歴の使われ方を説明する | 10、12 | <span class="nowrap">公開済み</span> |

### GitHub Copilot で開発者の生産性を向上させる（10〜15%）

| 公式の項目 | ページ | 状態 |
|---|---|---|
| コードの生成、リファクタリング、ドキュメントの作成に Copilot を使う | 16 | <span class="nowrap">準備中</span> |
| 学習を加速し、作業の切り替えを減らす | 16 | <span class="nowrap">準備中</span> |
| サンプルデータを生成し、古いコードを現代的な形に直す | 16 | <span class="nowrap">準備中</span> |
| 単体テストと、結合テストを生成する | 17 | <span class="nowrap">準備中</span> |
| 特殊な条件を見つけ、アサーション（期待する結果の確認）を書く | 17 | <span class="nowrap">準備中</span> |
| セキュリティの改善と、性能の最適化を提案させる | 17 | <span class="nowrap">準備中</span> |

### プライバシー、コンテンツの除外、セーフガードを構成する（10〜15%）

| 公式の項目 | ページ | 状態 |
|---|---|---|
| コンテンツの除外を設定する | 13 | <span class="nowrap">公開済み</span> |
| エディターの設定を行う | 05 | <span class="nowrap">準備中</span> |
| 出力の所有と、限界について説明する | 14 | <span class="nowrap">公開済み</span> |
| 公開されているコードと一致する提案の、フィルターを有効にする | 14 | <span class="nowrap">公開済み</span> |
| 提案と、コンテンツの除外に関する問題を解決する | 13 | <span class="nowrap">公開済み</span> |

公式の項目の日本語の表現は、このサイトでの訳です。

## MS Learn のトレーニングパスとの対応

公式の学習ガイドでは、学習の手段として、Microsoft Learn の 2 つのトレーニングパスが紹介されています。合計で 15 のモジュールがあります。各モジュールの内容が、このサイトのどのページに対応するかをまとめます。

| | 日本語のサイトでのタイトル | 英語でのタイトル | モジュールの数 |
|---|---|---|---|
| <span class="nowrap">Part 1</span> | GitHub Copilot 基本編 第1回（全2回） | GitHub Copilot Fundamentals Part 1 of 2 | 9 |
| <span class="nowrap">Part 2</span> | GitHub Copilot の基礎パート 2/2 | GitHub Copilot Fundamentals Part 2 of 2 | 6 |

日本語のサイトのタイトルは、機械翻訳のものが多く、不自然な表現が含まれます。たとえば、「コピロット空間の概要」は、Copilot Spaces のモジュールです。日本語のサイトで探しやすいように、表示されているとおりに書いて、英語のタイトルを併記しています。

### Part 1：GitHub Copilot 基本編 第1回（全2回）

| モジュール | タイトル（日本語のサイト） | タイトル（英語） | 内容 | 対応するページ |
|---|---|---|---|---|
| <span class="nowrap">Part 1-1</span> | GitHub Copilot を使用した責任ある AI | Responsible AI with GitHub Copilot | 責任ある AI | 03、04 |
| <span class="nowrap">Part 1-2</span> | GitHub Copilot の概要 | Introduction to GitHub Copilot | Copilot の概要、使い方、プランの違い、設定と問題の解決 | 01、02、05 |
| <span class="nowrap">Part 1-3</span> | GitHub Copilot を使用したプロンプト エンジニアリングの概要 | Introduction to prompt engineering with GitHub Copilot | プロンプトエンジニアリング、処理の流れ、データ、LLM | 10、11、12 |
| <span class="nowrap">Part 1-4</span> | コピロット空間の概要 | Introduction to Copilot Spaces | Copilot Spaces | 09 |
| <span class="nowrap">Part 1-5</span> | 高度な GitHub Copilot の機能の使用 | Using advanced GitHub Copilot features | スラッシュコマンド、チャット、エージェント | 06 |
| <span class="nowrap">Part 1-6</span> | 環境間でのGitHub Copilot: IDE、チャット、GitHub.com、コマンド ライン手法、GitHub Copilot アプリ | GitHub Copilot Across Environments: IDE, Chat, GitHub.com, Command Line Techniques, and the GitHub Copilot App | コード補完、Copilot Chat、GitHub.com、コマンドライン、GitHub Copilot アプリ | 05、06、08、09、11、19 |
| <span class="nowrap">Part 1-7</span> | GitHub Copilot での管理とカスタマイズに関する考慮事項 | Management and customization considerations with GitHub Copilot | プランと管理機能、契約上の保護、コンテンツの除外、問題の解決 | 02、13、14、15 |
| <span class="nowrap">Part 1-8</span> | GitHub Copilot を使用した AI の開発者ユース ケース | Developer use cases for AI with GitHub Copilot | 生産性の向上、開発工程全体での AI、限界と効果の測定 | 04、16 |
| <span class="nowrap">Part 1-9</span> | GitHub Copilot ツールを使用して単体テストを開発する | Develop unit tests using GitHub Copilot tools | 単体テストの作成 | 17 |

### Part 2：GitHub Copilot の基礎パート 2/2

| モジュール | タイトル（日本語のサイト） | タイトル（英語） | 内容 | 対応するページ |
|---|---|---|---|---|
| <span class="nowrap">Part 2-1</span> | GitHub Copilot エージェント モードを使用したアプリケーションのビルド | Building applications with GitHub Copilot agent mode | エージェントモード | 07 |
| <span class="nowrap">Part 2-2</span> | GitHub Copilot クラウド エージェントを使用して開発を加速する | Accelerate development with GitHub Copilot cloud agent | クラウドエージェント | 07 |
| <span class="nowrap">Part 2-3</span> | MCP サーバーの概要 | Introduction to MCP Server | MCP サーバー | 07 |
| <span class="nowrap">Part 2-4</span> | GitHub Copilot を使用したコード レビューと pull request の平準化 | Leveling up code reviews and pull requests with GitHub Copilot | コードレビューとプルリクエスト | 09 |
| <span class="nowrap">Part 2-5</span> | JavaScript で GitHub Copilot を使う | Using GitHub Copilot with JavaScript | JavaScript での実習 | 20 |
| <span class="nowrap">Part 2-6</span> | Python で GitHub Copilot を使用する | Using GitHub Copilot with Python | Python での実習 | 21 |

### 試験範囲の項目に、直接は対応しない内容

次の内容は、MS Learn にはありますが、公式の試験範囲の項目には、直接は挙げられていません。試験範囲にもとづく 18 ページには入れず、補足の部（第 6 部）で扱います。

| MS Learn の内容 | 扱うページ |
|---|---|
| Part 1-6 の「GitHub Copilot アプリ」の単元 | 19 |
| Part 2-5（JavaScript で GitHub Copilot を使う）。特定の言語での実習 | 20 |
| Part 2-6（Python で GitHub Copilot を使用する）。特定の言語での実習 | 21 |

対応は、モジュールの単元の一覧をもとに、このサイトで判断したものです。Part 2 のモジュールは、モジュールのタイトルと説明だけをもとに対応づけています。Part 2 の単元を確認した結果、試験範囲の項目に対応しない内容がほかにも見つかった場合は、補足の部に追加します。

## 各ページの書き方

各ページは、次の方針で書いています。

- **公式の試験範囲の項目を、現在の公式情報で確認して書く。** 確認には、GitHub の公式ドキュメントと、GitHub Copilot の Trust Center（GitHub がデータの扱いなどを説明しているページ）を使います。
- **MS Learn の教材の有用な内容を加える。** ただし、教材には、内容が古くなっている箇所があります。現在の公式情報と違う場合は、両方を載せて、違いを明記します。

GitHub Copilot は、機能や名称の変更が多い製品です。情報が古くなったときに見直せるよう、各ページの最後に、次の記録を付けます。

- 参照した公式ドキュメント
- 内容を最後に確認した日
- 検証の状況（公式ドキュメントで確認したのか、実際に操作して確認したのか）
- 公式の情報で確認できていない内容

## 参考資料

- [Study guide for Exam GH-300: GitHub Copilot（Microsoft Learn）](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-300)
- [GitHub Copilot 基本編 第1回（全2回）（Microsoft Learn・日本語版）](https://learn.microsoft.com/ja-jp/training/paths/copilot/)
- [GitHub Copilot の基礎パート 2/2（Microsoft Learn・日本語版）](https://learn.microsoft.com/ja-jp/training/paths/gh-copilot-2/)
- [GitHub Copilot Fundamentals Part 1 of 2（Microsoft Learn）](https://learn.microsoft.com/en-us/training/paths/copilot/)
- [GitHub Copilot Fundamentals Part 2 of 2（Microsoft Learn）](https://learn.microsoft.com/en-us/training/paths/gh-copilot-2/)

最終確認日：2026 年 10 月 11 日
