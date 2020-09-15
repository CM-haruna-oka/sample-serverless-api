import json
import logging
import os
import boto3


def set_env():
    """
    ローカル実行時の環境変数を設定
    """
    if os.getenv('IS_LOCAL', False):
        os.environ['ENV'] = 'dev'
        os.environ['DEFAULT_DATA_LIMIT'] = '20'


set_env()

log_level = 'DEBUG' if os.getenv('ENV') == 'dev' else 'INFO'

logger = logging.getLogger()
logger.setLevel(log_level)


DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))  # ページングのデフォルトかつ最大値


def list_promotional_items(limit, last_key=None):
    logging.debug(limit)
    dynamodb = boto3.resource('dynamodb')
    TABLE_NAME = 'Items'
    table = dynamodb.Table(TABLE_NAME)

    scan_kwargs = {
        'ConsistentRead': True,
        'Limit': limit
    }

    if last_key:
        scan_kwargs['ExclusiveStartKey'] = last_key

    response = table.scan(**scan_kwargs)
    logging.info(response)
    result = response.get('Items', [])

    return result


def validator_params(query):
    try:
        limit = query['limit'] if (query and query.get(
            'limit')) else os.environ['DEFAULT_DATA_LIMIT']
        limit = int(limit)
    except ValueError as valueError:
        logger.info(valueError)
        limit = DEFAULT_DATA_LIMIT

    # 20以上の数値の場合は20を再代入
    if limit >= DEFAULT_DATA_LIMIT or limit <= 0:
        limit = DEFAULT_DATA_LIMIT

    return {'limit': limit}


def handler(event, context):
    try:
        logging.info(event)
        logging.info(context)

        query = event.get('queryStringParameters')
        params = validator_params(query)

        result = list_promotional_items(
            params['limit'], event.get('last_evaluated_key'))
        logging.debug(result)
        return {
            'statusCode': 200,
            # ensure_ascii: 日本語文字化け対応
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        logging.error(e)
