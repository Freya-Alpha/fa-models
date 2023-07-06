from typing import List, Set, Optional
from famodels.models.direction import Direction
from famodels.models.order_type import OrderType
from famodels.models.side import Side
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
import os

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")


class Order(JsonModel):
    """This model is for hot orders ONLY! Use ColdOrder for paper trading.
    """
    id: str = Field(index=True)
    signal_id: str = Field(index=True)
    algo_id: str = Field(index=True)
    order_type: OrderType = Field(index=True, default=OrderType.LIMIT)        
    market: str = Field(index=True)
    exchange: str = Field(index=True)
    direction: Direction = Field(index=True)
    side: Side = Field(index=True)
    price: float
    amount: float    
    account: str = Field(index=True)
    pos_idx: int = Field(index=True)
    timestamp_of_order: int = Field(index=True)
    comission: float    

    class Meta:
        # global_key_prefix="order-and-trade-processing"
        model_key_prefix="order"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def __getitem__(self, key):
        return self.__dict__[key]