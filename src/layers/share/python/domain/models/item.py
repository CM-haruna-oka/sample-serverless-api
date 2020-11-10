import dataclasses


@dataclasses.dataclass()
class Item:
    """販促品
    DDD: エンティティ
    """
    item_id: str
    item_name: str
    category: str
