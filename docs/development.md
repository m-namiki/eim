# eim development document

## endpoint

[eim application](http://127.0.0.1:8000/)

[DynamoDB Admin](http://127.0.0.1:8001/)

## アプリケーション開発

### 初回起動後

初回起動後は以下のコマンドを実行してください。必要なライブラリがインストールされます。

```bash
# rye sync
```

### Webアプリケーションの起動

```bash
# rye run devserver
```

`devserver`は `pyproject.toml`で以下のコマンドをカスタムスクリプトとして登録している。

```
uvicorn eim.main:app --reload --host 0.0.0.0
```

詳細については[Rye公式サイト](https://rye-up.com/guide/pyproject/#toolryescripts)を参照のこと。

### lambda functionの実行

### テストの実行

```bash
# rye run pytest
```

### directories

- docs
  - アプリケーション開発に関するドキュメントを格納するディレクトリ
- provisioning
  - AWS CDKに関するコードを格納するディレクトリ
- src
  - eim
    - Webアプリケーションのソースコードを格納するディレクトリ
  - functions
    - lambda functionのソースコードを格納するディレクトリ
- test
  - テストに関するリソースなどを格納するディレクトリ
