import email

DEF_TEST_MAIL = "./test/resources/ctq89s54b65oc9809dit427t13kqg6qp53c4kt01"


def _analyze(_part):
    charset = _part.get_content_charset()
    payload = _part.get_payload(decode=True)
    body = payload.decode(charset)
    lines = body.splitlines()
    for line in lines:
        if line.startswith("お届け予定日"):
            print(line)
        if line.startswith("■"):
            # 商品情報
            print(line)


with open(DEF_TEST_MAIL, "r", encoding="UTF-8") as f:
    msg = email.message_from_file(f)

for part in msg.walk():
    if part.get_content_type() == "text/plain":
        _analyze(part)
