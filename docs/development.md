# eim development document

[FastAPI](http://127.0.0.1:8000/)

[DynamoDB Admin](http://127.0.0.1:8001/)

## start application

```
# rye run devserver
```

`devserver`は `pyproject.toml`で以下のコマンドをカスタムスクリプトとして登録している。

```
uvicorn eim.main:app --reload --host 0.0.0.0
```

詳細については[Rye公式サイト](https://rye-up.com/guide/pyproject/#toolryescripts)を参照のこと。