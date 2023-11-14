import email
from datetime import datetime as dt

import boto3


def create_item(received_date, item_list, price_list):
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
    with open(file, "r", encoding="UTF-8") as f:
        msg = email.message_from_file(f)
        items = None
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                items = analyze(part)
        print(items)

    return 0


def lambda_handler(event, context):
    s3 = boto3.client("s3")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    try:
        file = s3.get_object(Bucket=bucket, Key=key)
        read_message(file)
        print(file)

    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}.".format(key, bucket))
        raise e
