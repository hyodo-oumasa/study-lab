# sentence-transformers と pgvector で、自分のメモを意味で検索する

このページでは、手元にためた Markdown のメモを「キーワード」ではなく「意味」で検索する小さなツールを作ったときに使ったライブラリと、試して分かったことをまとめます。

作ったのは、ターミナルから次のように使うコマンドです。

```bash
python note_search.py "過学習への対処"
```

```text
1. [0.875] 10_daily/2026-04-20_daily.md (chunk 2)
   学習ループを作って終わりではなく、その結果から過学習を読み取り、
   評価方法を見直し、validation と early stopping を導入する...
```

「過学習」という単語を含まないメモでも、内容が近ければ上位に出てきます。たとえば「early stopping を入れた日の日記」は、本文に「過学習への対処」と書いていなくても見つかります。これが「意味で検索する」ということです。

## 使った部品

| 部品 | 種類 | 役割 |
|---|---|---|
| [sentence-transformers](https://sbert.net/) | Python ライブラリ | 文章を「埋め込み」（後述）に変換する |
| [pgvector](https://github.com/pgvector/pgvector) | PostgreSQL の拡張 | データベースにベクトル型の列と「近い順に並べる」検索を追加する |
| [pgvector（Python パッケージ）](https://github.com/pgvector/pgvector-python) | Python ライブラリ | Python の配列と pgvector の型を橋渡しする |
| [psycopg](https://www.psycopg.org/) | Python ライブラリ | Python から PostgreSQL に接続して SQL を実行する |
| [Supabase](https://supabase.com/) | クラウドサービス | PostgreSQL（pgvector 入り）を無料で借りられる |

モデルは [intfloat/multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small) を使いました。日本語を含む多言語に対応していて、約 120 MB と小さく、Mac の CPU だけで動きます。

## 「意味で検索」の仕組み：埋め込み

**埋め込み（embedding）** とは、文章を数百個の数値の並び（ベクトル）に変換したものです。意味が近い文章ほど近い数値になるように学習されているため、「文章どうしの意味の近さ」を数値どうしの近さ（コサイン類似度）として計算できます。

最小のサンプルコードです。

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")

query = model.encode("query: 学習率を下げたら損失が安定した話",
                     normalize_embeddings=True)
passages = model.encode(
    ["passage: 学習率スケジューラを導入したら発散しなくなった。",
     "passage: 今日の夕食はカレーだった。"],
    normalize_embeddings=True)

print(query @ passages[0])  # 0.889（内容が近い）
print(query @ passages[1])  # 0.782（内容が遠い）
```

このモデルの出力は 384 個の数値です。`normalize_embeddings=True` でベクトルの長さを 1 にそろえると、内積（`@`）がそのままコサイン類似度になります。

## pgvector 側：テーブルと検索の SQL

メモを段落ごとに分割（チャンク化）して、本文とベクトルをテーブルに入れます。

```sql
create extension if not exists vector;

create table notes_chunks (
    id bigint generated always as identity primary key,
    path text not null,          -- どのメモか
    chunk_index int not null,    -- メモの何番目の部分か
    content text not null,       -- 本文
    embedding vector(384) not null,  -- 埋め込み（モデルの次元数に合わせる）
    unique (path, chunk_index)
);
```

検索は、クエリ文の埋め込みに近い順に並べるだけです。`<=>` が pgvector のコサイン距離の演算子です。

```sql
select path, content, 1 - (embedding <=> %(q)s) as score
from notes_chunks
order by embedding <=> %(q)s
limit 5;
```

Python 側は psycopg で接続し、pgvector パッケージの `register_vector(conn)` を呼んでおくと、NumPy の配列をそのまま SQL に渡せます。

## 試して分かったこと・注意点

### E5 系モデルは接頭辞を忘れると精度が落ちる

このモデルは、検索される側の文章には `passage: `、検索クエリには `query: ` を先頭に付けて使う決まりで学習されています（モデルカードに記載があります）。この接頭辞を付け忘れても動いてしまうので、気づきにくい落とし穴です。接頭辞を付ける処理はラッパー関数の中に閉じ込めて、呼び出し側が忘れられない作りにしました。

### スコアは絶対値ではなく順位で読む

上のサンプルのとおり、このモデルは**無関係な文どうしでも 0.7 台**が出ます。「0.8 を超えたら関連あり」のような絶対値のしきい値は機能しません。「上位 5 件を出して人間が見る」という順位ベースの使い方が正解でした。

### 件数が少ないうちは、近似インデックスは不要

pgvector には検索を高速化する近似インデックス（HNSW など）がありますが、数百〜数千チャンク程度なら全件走査で十分速く、正確な順位がそのまま得られます。最初からインデックスの設定で悩む必要はありませんでした。

### Supabase 無料枠の「自動一時停止」を前提に設計する

Supabase の無料プランは、1 週間ほど使わないとプロジェクトが自動で一時停止します（データは消えず、ダッシュボードから復元できます。公式ドキュメントの現行版では、停止から最大 1 年間は復元できると書かれています。以前は 90 日とされていたので、古い記事の数字には注意してください）。

そこで、**メモの正本は手元に置き、データベース側は「いつでも作り直せる索引」** と位置づけました。`index` コマンド一発で全チャンクを再登録できるようにしておけば、一時停止も削除も怖くありません。手元の約 90 ファイル（334 チャンク）の埋め込み計算は、Mac の CPU で 4 秒ほどでした。

### 接続は「Session pooler」を使う

無料プランのデータベースへの直接接続は IPv6 のみで、一般的な家庭の回線（IPv4）からはつながらないことがあります。Supabase の接続画面にある **Session pooler** の接続文字列（`...pooler.supabase.com:5432`）を使うと IPv4 からも接続できます。

また、接続文字列のような長いランダム文字列は、**手で書き写すと必ずどこかで間違えます**。実際、1 文字どころか全く別の文字列を書き写してしまい、原因究明に時間を使いました。コピー＆ペーストできる経路を必ず用意すること、間違いを疑うときは DNS の登録確認など機械的な検証をすることが教訓です。

## 似た選択肢との違い

| 選択肢 | 特徴 | 今回選ばなかった/選んだ理由 |
|---|---|---|
| grep（文字列検索） | 速くて確実。ただし言葉が一致しないと見つからない | 「どんな単語で書いたか忘れた」場面で無力 |
| FAISS / Chroma（ローカルのベクトル検索） | サーバー不要で手軽。ファイルとして持ち歩ける | 1 台で完結するならこちらが簡単。今回は複数マシンから同じ索引を使いたかった |
| pgvector（PostgreSQL 拡張） | 普通の SQL と同居できる。where 句との組み合わせも自由 | SQL の学習を兼ねられる点と、クラウドに置けば端末をまたげる点で採用 |
| OpenAI などの埋め込み API | 精度が高く、重いモデルを手元に置かなくてよい | 少額の従量課金と API キー管理が発生する。今回は無料で完結する構成を優先 |

## まとめ

- 文章の「意味の近さ」は、埋め込みに変換すれば数値の近さとして計算できる
- sentence-transformers なら、埋め込みの生成はコード数行。小さい多言語モデルでも日本語メモの検索には十分だった
- pgvector を使うと、ベクトル検索が「普通の SQL の order by」として書ける
- 無料のクラウドサービスを使うときは、「消えても手元から作り直せる」構造にしておくと、制約（自動一時停止など）に振り回されない
