import boto3
from typing import List, Union, Optional
from domain.models.item import Item
from aws_lambda_powertools import Logger
logger = Logger(child=True)


class ItemRepository():
    def list(self, limit: int,
             last_key: Optional[str]) -> List[Item]:
        """商品一覧をDBから取得する

        Parameters
        ----------
        limit : int
            [description]
        last_key : str, optional
            [description], by default None

        Returns
        -------
        List
            [description]
        """

        dynamodb = boto3.resource('dynamodb')
        TABLE_NAME = 'Items'
        table = dynamodb.Table(TABLE_NAME)

        scan_kwargs = {
            'ConsistentRead': True,
            'Limit': int(limit)
        }

        if last_key:
            scan_kwargs['ExclusiveStartKey'] = last_key

        logger.debug(scan_kwargs)
        response = table.scan(**scan_kwargs)

        return response.get('Items', [])

    def get(self, item_id: str) -> Union[Item, None]:
        """商品を一件取得する

        Parameters
        ----------
        item_id : str
            商品ID

        Returns
        -------
        Dict
            商品情報
        """
        # TODO
        if item_id == 'item_0001':
            item: Item = {
                'item_id': 'item_0001',
                'item_name': 'サンプル品1',
                'category': '販促物'
            }
            return item
        else:
            return

    def add(self, item: Item) -> Item:
        """商品を一件追加する

        Parameters
        ----------
        item : Dict
            商品情報

        Returns
        -------
        Dict
            商品情報
        """
        # TODO
        item = {
            'item_id': 'item_0001',
            'item_name': 'サンプル品1',
            'category': '販促物'
        }

        return item

    def drop(self, item_id: str) -> Item:
        """商品を一件削除する

        Parameters
        ----------
        item_id : str
            商品ID

        Returns
        -------
        Dict
            商品情報
        """
        # TODO
        item: Item = {
            'item_id': 'item_0001',
            'item_name': 'サンプル品1',
            'category': '販促物'
        }

        return item
