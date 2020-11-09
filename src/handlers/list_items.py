import json
import os
import boto3
from core import utils
from domain import items_domain
from interface.handler import Handler
from typing import Union, Any, Dict
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event: Union[APIGatewayProxyEvent, Dict[str, Any]],
            context: LambdaContext) -> Dict[str, Any]:
    try:
        handle = Handler(event, context)
        params = handle.get_params(event)
        result = items_domain.list_items(
            limit=params.get('limit'),
            offset=params.get('offset'))
        logger.info(result)
        return handle.create_list_response(200, result)

    except Exception as e:
        logger.exception(e)
        raise e
