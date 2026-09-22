# Jev / System One 日本語サンプル

TypeSafe AI の公式 [Python SDK クイックスタート](https://docs.typesafe.ai/sdk/python)をもとに、Jev の System One API を `typesafe-sdk` から実行する例を日本語化したプロジェクトです。

1つの問い合わせ文に対して、次の3種類の質問を同時に評価します。

- `Noul`：Yes / No の度合いを `0` から `1` で返す
- `Choice`：指定した候補から最も適切なものを選ぶ
- `Score`：順序付けされた評価基準をスコアとして返す

このサンプルでは、問い合わせが請求に関するものか、顧客の口調、緊急度を判定します。

## ファイル

- `main.py`：公式クイックスタートをもとにした英語版
- `mainjp.py`：入力文、質問、評価基準、出力表示を日本語化した版
- `pyproject.toml`：Pythonのバージョンと依存パッケージの定義

## 必要なもの

- Python 3.13 以上
- [uv](https://docs.astral.sh/uv/)
- TypeSafe AI のAPIキー

APIキーは [TypeSafe Console](https://console.typesafe.ai/) で作成します。

## セットアップ

依存パッケージをインストールします。

```powershell
uv sync
```

プロジェクト直下に `.env` ファイルを作成し、APIキーを設定します。

```dotenv
TYPESAFE_API_KEY=取得したAPIキー
```

`.env` は `.gitignore` の対象です。APIキーをソースコードへ直接記述したり、Gitへコミットしたりしないでください。

## 実行方法

日本語版を実行します。

```powershell
uv run python mainjp.py
```

英語版は次のコマンドで実行できます。

```powershell
uv run python main.py
```

どちらのファイルも `python-dotenv` の `load_dotenv()` で `.env` を読み込むため、スクリプトから実行する場合は VS Code の `python.terminal.useEnvFile` 設定に依存しません。

## 日本語版の処理

`mainjp.py` は `AsyncTypeSafeClient` を使って、1つの `state` に対する3つの質問を非同期で送信します。

```python
response = await client.system_one(
    state={"document": document},
    questions={
        "billing": Noul(instructions="このチケットは請求に関するものですか？"),
        "tone": Choice(
            instructions="顧客はどのような口調ですか？",
            criteria={"冷静": None, "いら立っている": None, "怒っている": None},
        ),
        "urgency": Score(
            instructions="このチケットの緊急度はどの程度ですか？",
            criteria=["待てる", "今週中", "今日中"],
        ),
    },
)
```

## 結果の見方

### Noul

```python
response.nouls["billing"].noul
```

Yes / No の判定結果です。`1` に近いほど「請求に関する」、`0` に近いほど「請求に関しない」という評価になります。

### Choice

```python
response.choices["tone"].choice
```

`冷静`、`いら立っている`、`怒っている`の中から、最も確率の高い選択肢を返します。詳細な確信度と各候補の確率は、それぞれ `confidence` と `probabilities` から確認できます。

### Score

```python
response.scores["urgency"].score
```

評価基準の並び順に、`待てる = 0`、`今週中 = 1`、`今日中 = 2` が割り当てられます。`score` は各段階の確率を加味した加重平均であるため、小数になることがあります。対応表と各段階の確率は `legend` と `probabilities` から確認できます。

すべての詳細な回答は、次のように取得できます。

```python
print(response.answers)
```

## 参考資料

- [TypeSafe Python SDK 公式ドキュメント](https://docs.typesafe.ai/sdk/python)
- [TypeSafe Python SDK ソースコード](https://github.com/TypeSafe-AI/typesafe-python)
