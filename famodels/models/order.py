from datetime import datetime
from typing import List, Set, Optional
from famodels.models.state_of_trade import StateOfTrade
from famodels.models.direction import Direction
from famodels.models.order_type import OrderType
from famodels.models.side import Side
from typing import Optional
from redis_om import Migrator
from redis_om import (Field, JsonModel)


class Order(JsonModel):
    """This model is for hot orders ONLY! Use ColdOrder for paper trading.
    """
    id: str = Field(index=True)
    signal_id: str = Field(index=True)
    order_type: OrderType = Field(index=True, default=OrderType.LIMIT)        
    market: str = Field(index=True)
    direction: Direction = Field(index=True)
    side: Side = Field(index=True)
    price: float
    amount: float    
    account: str = Field(index=True)
    pos_idx: int = Field(index=True)
    timestamp_of_order: int = Field(index=True)
    comission: float    

    class Meta:
        global_key_prefix="order-and-trade-processing"
        model_key_prefix="order"

    def __getitem__(self, key):
        return self.__dict__[key]