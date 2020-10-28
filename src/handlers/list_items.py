import json
import os
import boto3
from core import utils
from infrastructure import items
from aws_lambda_powertools import Logger
logger = Logger(service="sample-api", level="DEBUG")


DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))  # ページングのデフォルトかつ最大値


@logger.inject_lambda_context
def handler(event, context):
    logger.info(event)
    try:
        params = utils.get_params(event)
        result = items.list_items(
            params['limit'],
            event.get('last_evaluated_key'))
        logger.info(result)
        return {
            'statusCode': 200,
            # ensure_ascii: 日本語文字化け対応
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        logger.error(e)
        raise e
