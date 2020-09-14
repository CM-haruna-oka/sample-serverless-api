import json
import logging
import os
import boto3


def set_env_local():
    """
    ローカル実行時の環境変数を設定
    """
    if os.getenv('IS_LOCAL', False):
        os.environ['ENV'] = 'dev'
        os.environ['DEFAULT_DATA_LIMIT'] = '20'


set_env_local()
log_level = 'DEBUG' if os.getenv('ENV') == 'dev' else 'INFO'

logger = logging.getLogger()
logger.setLevel(log_level)

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'Items'
table = dynamodb.Table(TABLE_NAME)

DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))  # 最大値


def list_promotional_items(limit):
    logging.debug(limit)

    res = table.scan(TableName=TABLE_NAME, ConsistentRead=True)
    logging.info(res)
    return res['Items']


def validator_limit(limit):
    try:
        limit = int(limit)
    except ValueError as valueError:
        logger.info(valueError)
        limit = DEFAULT_DATA_LIMIT

    # 20以上の数値の場合は20を再代入
    if limit >= DEFAULT_DATA_LIMIT:
        limit = DEFAULT_DATA_LIMIT

    return limit


def handler(event, context):
    try:
        logging.info(event)
        logging.info(context)

        query = event.get('queryStringParameters')
        limit = query['limit'] if (query and query.get(
            'limit')) else os.environ['DEFAULT_DATA_LIMIT']

        result = list_promotional_items(limit)
        logging.debug(result)
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            # ensure_ascii: 日本語文字化け対応
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        logging.error(e)
