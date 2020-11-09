from infrastructure import items
import os


DEFAULT_DATA_LIMIT = int(os.getenv('DEFAULT_DATA_LIMIT'))


def list_items(limit=DEFAULT_DATA_LIMIT, offset=None):
    """[商品一覧を取得]

    Parameters
    ----------
    limit : [int], optional
        [description], by default env DEFAULT_DATA_LIMIT
    offset : [str], optional
        [Acquisition start position], by default None

    Returns
    -------
    [list]
        [list items]
    """
    return items.list_items(limit, offset)
