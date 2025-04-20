from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    item_type: str
    type: str
    rarity: str
    is_rate_up: bool