from datetime import datetime
from typing import List, Set, Optional
from state_of_trade import StateOfTrade
from direction import Direction
from order_type import OrderType
from side import Side
from typing import Optional
from sqlmodel import Field, SQLModel

###### JSON TO CLASS MAPPING EXAMPLE
# external_data = {
#     'id': '123',
#     'signup_ts': '2019-06-01 12:22',
#     'friends': [1, 2, '3'],
# }
# user = User(**external_data)

class BaseTradeSQLModel(SQLModel):
    def __init__(self, **kwargs):
        self.__config__.table = False
        super().__init__(**kwargs)
        self.__config__.table = True

    class Config:
        validate_assignment = True

class Order(BaseTradeSQLModel, table=True):
    """Our order model (not the order model from the CEX). It can be part of a trade."""

    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account: str
    pos_idx: int
    market: str
    correlation_id: float
    direction: Direction
    side: Side
    price: float
    amount: float    
    time_of_order: datetime
    last_update: datetime
    order_type: OrderType = OrderType.LIMIT

    def __getitem__(self, key):
        return self.__dict__[key]