import logging
from core import utils
from core.auth import Auth


def handler(event, context):
    utils.logging_settings()
    try:
        logging.info(event)

        auth = Auth()
        token = auth.get_token(event)  # eventからトークン取得

        if token is None:
            logging.error('No token.')
            result = auth.generate_policy('sample', 'Deny', '*')
            return result
        logging.info(token)

        resource = event['methodArn']

        # トークン検証
        result = auth.verify(token, resource)
        return result

    except Exception as e:
        logging.error(e)
