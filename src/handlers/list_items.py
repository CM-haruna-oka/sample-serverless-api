from domain.items_domain import ItemService
from interface.handler import LambdaProxyHandler
from typing import Any, Dict, TypeVar
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
logger = Logger()
T = TypeVar('T', APIGatewayProxyEvent, Dict[str, Any])


class ListItemHandler(LambdaProxyHandler):
    def handle(self, params: Dict):
        logger.info(params)
        item_service = ItemService()
        result = item_service.list(
            limit=params.get('limit'),
            offset=params.get('offset'))
        logger.info(result)
        return result


@logger.inject_lambda_context(log_event=True)
def handler(event: T, context: LambdaContext) -> Dict[str, Any]:
    list_item_handler = ListItemHandler(event)
    return list_item_handler.invoke(context, event)
