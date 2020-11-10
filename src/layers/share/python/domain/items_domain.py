from repository import items_repository
import os
from typing import Union, Any, Dict, List


DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))


class ItemService():
    def list(self, limit=DEFAULT_DATA_LIMIT, offset=None) -> List:
        """商品一覧を取得

        Parameters
        ----------
        limit : int, optional
            取得する件数, by default env DEFAULT_DATA_LIMIT
        offset : str, optional
            Acquisition start position, by default None

        Returns
        -------
        List
            商品一覧
        """
        return items_repository.list_items(limit, offset)

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
        return items_repository.get_item(item_id)
