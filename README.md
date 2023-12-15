# EIM

- おうちCO-OP 在庫管理システム
    - Efriends Inventory Management

## 概要

- `お届け商品ご案内メール` の内容をもとに在庫情報として登録する
- Webページで在庫情報を表示する
- 消費したものは削除できる

## 永続化情報

### 商品情報（Item）

|論理名|物理名|型|桁数|概要・備考|
|-|-|-|-|-|
| id | `id` | bigint | | サロゲートキー |
| 商品コード | `item_codde` | integer | | |
| 商品名 | `item_name` | varchar | | |
| 受取日 | `received_date` | date | | |
| 個数 | `amount` | integer | | |
| 残数 | `remaining` | integer | | |
| 価格 | `price` | integer | | |
| 削除フラグ | `delete_flag` | integer | | |

#### 

- メールで届く1行（抜粋）
```
■110:産地指定チリ産塩銀鮭切身（甘口）
　４切（２４０ｇ）
　価格:520円x1
```
- 項目移送
```
■${商品コード}:${商品名}
　４切（２４０ｇ） # この行は無視
　価格:${価格}円x${個数}
```

## アーキテクチャ

- Webフロントエンド
    - SPA
        - React or Vue.js
- バックエンド
    - AWS lambda
        - 商品情報の登録
    - Python + FastAPI
- データベース
    - DynamoDB
- インフラ
    - CloudFormation
    - サーバレス
