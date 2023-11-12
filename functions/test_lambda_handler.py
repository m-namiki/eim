from lambda_handler import read_message

DEF_TEST_MAIL = "test/resources/test_mail"


def test_read_message():
    assert 0 == read_message(DEF_TEST_MAIL)
