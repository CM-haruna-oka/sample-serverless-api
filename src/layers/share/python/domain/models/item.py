import dataclasses
from typing import TypedDict


@dataclasses.dataclass()
class Item(TypedDict):
    """販促品
    DDD: エンティティ
    """
    item_id: str
    item_name: str
    category: str
