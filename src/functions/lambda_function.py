"""_summary_

Raises:
    e: _description_

Returns:
    _type_: _description_
"""
import email
from datetime import datetime as dt

import boto3


def insert_item(items):
    """商品情報をDBに登録します。

    Args:
        items (_type_): 商品情報のリスト

    Returns:
        _type_: _description_
    """
    client = boto3.client("dynamodb")
    if not check_item_table(client):
        create_item_table(client)
    for item in items:
        client.put_item(TableName="item", Item=item)
    return 0


def create_item_table(client):
    """商品情報のテーブルを作成します。

    Args:
        client (_type_): _description_

    Returns:
        _type_: _description_
    """
    client.create_table(
        TableName="item",
        KeySchema=[
            {"AttributeName": "item_code", "KeyType": "HASH"},
            {"AttributeName": "received_date", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "item_code", "AttributeType": "N"},
            {"AttributeName": "received_date", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    return 0


def check_item_table(client):
    """商品情報のテーブルが存在するか確認します。

    Returns:
        _type_: _description_
    """
    response = client.list_tables()
    if "item" in response["TableNames"]:
        return True
    else:
        return False


def create_item(received_date, item_list, price_list):
    """商品情報を作成します。

    Args:
        received_date (_type_): 受取日
        item_list (_type_): 商品名のリスト
        price_list (_type_): 価格のリスト

    Returns:
        _type_: _description_
    """
    items = []
    # 日付はISO8601形式にする必要がある
    received_date = received_date.split(":")[1]
    year = dt.now().year
    month = received_date.split("月")[0]
    day = received_date.split("月")[1].split("日")[0]
    received_date = f"{year}-{month}-{day}"

    for item_line, price_line in zip(item_list, price_list):
        # 商品コードと商品名に分割
        item_line = item_line.replace("■", "").split(":")
        # 価格と量に分割
        amount = price_line.split(":")[1].replace("円", "").split("x")

        items.append(
            {
                "item_code": int(item_line[0]),
                "item_name": item_line[1],
                "received_date": received_date,
                "amount": int(amount[1]),
                "remaining": int(amount[1]),
                "price": int(amount[0]),
                "delete_flag": 0,
            }
        )
    return items


def analyze(_part):
    """メッセージを解析します。

    Args:
        _part (_type_): _description_

    Returns:
        _type_: _description_
    """
    payload = _part.get_payload(decode=True)
    body = payload.decode(_part.get_content_charset())
    lines = body.splitlines()

    received_date = ""
    item_list = []
    price_list = []

    for line in lines:
        if line.startswith("お届け予定日"):
            received_date = line
        if line.startswith("■"):
            item_list.append(line)
        if line.startswith("価格"):
            price_list.append(line)

    return create_item(received_date, item_list, price_list)


def read_message(file):
    """指定されたファイルを読み込み、メッセージを解析します。

    Args:
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file, "r", encoding="UTF-8") as f:
        msg = email.message_from_file(f)
        items = None
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                items = analyze(part)
        insert_item(items)

    return 0


def lambda_handler(event, context):
    """lambda関数ハンドラー

    lambda関数のハンドラー。詳細は[公式ドキュメント](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-handler.html)

    Args:
        event (dict): [イベントオブジェクト](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-concepts.html)
        context (_type_): [コンテキストオブジェクト](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html)

    Raises:
        e: ファイルの読み込みに失敗した場合
    """
    s3 = boto3.client("s3")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    try:
        file = s3.get_object(Bucket=bucket, Key=key)
        read_message(file)

    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}.".format(key, bucket))
        raise e
