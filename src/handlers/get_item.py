import json
import os
import boto3
from domain.items_domain import ItemService
from interface.handler import LambdaProxyHandler
from interface.error import ValidationError, EntityNotFound, LambdaException
from typing import Union, Any, Dict
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
logger = Logger()


class GetItemHandler(LambdaProxyHandler):
    def handle(self, params):
        logger.info(params)
        if 'item_id' not in params:
            raise ValidationError('item_id is required.')
        item_id = params['item_id']
        item_service = ItemService()
        item = item_service.get(item_id)
        logger.info(item)
        if item is None:
            message = f'item not found. item_id: {item_id}'
            raise EntityNotFound(message)
        return item


@logger.inject_lambda_context(log_event=True)
def handler(event: Union[APIGatewayProxyEvent, Dict[str, Any]],
            context: LambdaContext) -> Dict[str, Any]:
    get_item_handler = GetItemHandler(event)
    return get_item_handler.invoke(context, event)
