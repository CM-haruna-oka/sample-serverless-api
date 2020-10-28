import json
import logging
import os
import boto3


DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))


def logging_settings():
    logger = logging.getLogger()
    log_level = 'DEBUG' if os.getenv('ENV') == 'itg' else 'INFO'
    logger.setLevel(log_level)


def validator(query):
    try:
        limit = query['limit'] if (query and query.get(
            'limit')) else os.environ['DEFAULT_DATA_LIMIT']
        limit = int(limit)
    except ValueError as valueError:
        logging.info(valueError)
        limit = DEFAULT_DATA_LIMIT

    # 20以上の数値の場合は20を再代入
    if limit >= DEFAULT_DATA_LIMIT or limit <= 0:
        limit = DEFAULT_DATA_LIMIT

    return {'limit': limit}


def get_params(event):
    params = {}

    if event.httpMethod == 'GET':
        query = event.get('queryStringParameters', {})
        params.update(query)
    else:
        body = event.get('body', {})
        params.update(body)

    path = event.get('pathParameters', {})
    params.update(path)

    return params
