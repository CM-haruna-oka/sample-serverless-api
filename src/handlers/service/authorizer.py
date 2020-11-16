from service.authentication import Auth
from aws_lambda_powertools import Logger
logger = Logger()


@logger.inject_lambda_context
def handler(event, context):
    logger.info(event)
    auth = Auth()
    token = auth.get_token(event)  # eventからトークン取得
    if token is None:
        logger.exception('No token.')
        result = auth.generate_policy('sample', 'Deny', '*')
        return result
    logger.info(token)

    try:
        resource = event['methodArn']  # TODO

        # トークン検証
        result = auth.verify(token, resource)
        return result

    except Exception as e:
        logger.exception(e)
