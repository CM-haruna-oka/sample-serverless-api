import json
from abc import ABCMeta, abstractmethod
from typing import Any, Dict
from interface.error import ValidationError, EntityNotFound
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools import Logger
logger = Logger(child=True)


class Handler(metaclass=ABCMeta):
    """Handlerのメタクラス

    Args:
        metaclass ([type], optional): [description]. Defaults to ABCMeta.
    """

    timestamp: int
    principal_id: str

    @abstractmethod
    def handle(self, params: Dict):
        """このメソッドを各Lambda Function内でオーバーライドしてFunction毎の処理を記述する

        Parameters
        ----------
        params : Dict
            [description]
        """

    def invoke(self, context: Any, event: Any):
        """このメソッドを各ハンドラークラスでオーバーライドしてLambda内の共通処理を記述する

        Parameters
        ----------
        context : Any
            [description]
        event : Any
            [description]
        """

    def set_logs(self):
        logger.structure_logs(append=True, user_id=self.principal_id)


class LambdaProxyHandler(Handler):
    """Lambdaプロキシ統合ハンドラ用クラス
    """

    def __init__(self, event):
        self.__set_principal_id(event)
        self.set_logs()

    def invoke(self, context: Any, event: Any):
        params = self.__get_params(event)
        try:
            result = self.handle(params)
            logger.info(result)
            return self.create_response(200, result)
        except ValidationError as err:
            logger.warning(err)
            return self.create_error_response(err)
        except EntityNotFound as err:
            logger.warning(err)
            return self.create_error_response(err)
        except Exception as e:
            logger.exception(e)
            raise e

    def __set_principal_id(self, event):
        self.principal_id = event.get(
            'requestContext',
            {}).get(
            'authorizer',
            {}).get('principalId') or 'test_user'

    def __get_params(self, event):
        """Lambdaプロキシ統合のパラメータをフラットにして返す

        Parameters
        ----------
        event : any
            Lambdaプロキシで渡されるイベント

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

    def create_response(self, status_code, result):

        return {
            'statusCode': status_code,
            'body': json.dumps(result, ensure_ascii=False)
        }

    def create_error_response(self, error):

        result = {
            'errorCode': error.error_code,
            'message': error.message
        }

        return {
            'statusCode': error.status_code,
            'body': json.dumps(result)
        }


class LambdaEventHandler(Handler):
    """Lambdaイベント実行ハンドラ用クラス

    Parameters
    ----------
    Handler : [type]
        [description]
    """
