import json
from abc import ABCMeta, abstractmethod
from typing import Union, Any, Dict
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
logger = Logger(child=True)


class Handler():
    """Lambdaハンドラ共通処理群

    Returns
    -------
    [type]
        [description]
    """

    timestamp: int
    principal_id: str

    def __init__(self, event: Union[APIGatewayProxyEvent, Dict[str, Any]],
                 context: LambdaContext):
        self.event = event
        self.context = context
        self.handle(event, context)
        self.__set_params(event)

    def handle(self, event: Union[APIGatewayProxyEvent, Dict[str, Any]],
               context: LambdaContext):
        logger.debug('handle')

    def invoke(self):
        pass

    def __set_params(self, event):
        self.principal_id = event.get(
            'requestContext',
            {}).get(
            'authorizer',
            {}).get('principalId')
        user_id = self.principal_id or 'test_user'
        logger.structure_logs(append=True, user_id=user_id)

    def get_params(self, event):
        """Lambdaプロキシ統合のパラメータをフラットにして返す

        Parameters
        ----------
        event : any
            [description]

        Returns
        -------
        params : any
            [description]
        """
        params = {}

        if event.get('httpMethod') is None:
            # Lambda直実行(デバッグ時のみ)
            params.update(event)
        elif event.get('httpMethod') == 'GET':
            query = event.get('queryStringParameters', {})
            params.update(query)
        else:
            body = event.get('body', {})
            params.update(body)

        path = event.get('pathParameters', {})
        params.update(path)
        logger.debug(params)

        return params

    def create_list_response(self, status_code, result):

        return {
            'statusCode': status_code,
            'body': {'items': json.dumps(result)}
        }

    def create_response(self, status_code, result):

        return {
            'statusCode': status_code,
            'body': json.dumps(result)
        }
