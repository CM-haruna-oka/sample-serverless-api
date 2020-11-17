from repository.items_repository import ItemRepository
import os
from typing import Any, List
from domain.models.item import Item
from aws_lambda_powertools import Logger
logger = Logger(child=True)

DEFAULT_DATA_LIMIT: int = int(
    os.getenv('DEFAULT_DATA_LIMIT'))  # type: ignore


class ItemService():
    item_repository = ItemRepository()

    def list(self, limit=None, offset=None) -> List[Item]:
        """商品一覧を取得

        Parameters
        ----------
        limit : int, optional
            取得する件数, by default None
        offset : str, optional
            Acquisition start position, by default None

        Returns
        -------
        List
            商品一覧
        """

        return self.item_repository.list(limit or DEFAULT_DATA_LIMIT, offset)

    def get(self, item_id: str) -> Any:
        """[summary]

        Parameters
        ----------
        item_id : str
            商品ID

        Returns
        -------
        Any
            商品情報
        """
        return self.item_repository.get(item_id)
