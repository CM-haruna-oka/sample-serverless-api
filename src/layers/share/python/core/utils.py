import json
import logging
import os
import boto3

log_level = 'DEBUG' if os.getenv('ENV') == 'dev' else 'INFO'
logger = logging.getLogger()
logger.setLevel(log_level)
DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))


def validator(query):
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
