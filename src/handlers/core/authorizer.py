import logging
from core import utils
from core.auth import Auth


def handler(event, context):
    utils.logging_settings()
    logging.info(event)
    auth = Auth()
    token = auth.get_token(event)  # eventからトークン取得
    if token is None:
        logging.error('No token.')
        result = auth.generate_policy('sample', 'Deny', '*')
        return result
    logging.info(token)

    try:
        resource = event['methodArn']  # TODO

        # トークン検証
        result = auth.verify(token, resource)
        return result

    except Exception as e:
        logging.error(e)
