import src.handlers.list_promotional_items as handler


def test_limit_apply():
    limit = 25
    response = handler.validator_limit(limit)
    print(response)
    assert response == 20


def test_limit_not_decimal():
    limit = 'abc'
    response = handler.validator_limit(limit)
    print(response)
    assert response == 20


def test_limit_float():
    limit = 10.5
    response = handler.validator_limit(limit)
    print(response)
    assert response == 10
