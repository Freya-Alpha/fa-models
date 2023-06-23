from datetime import datetime
from os import environ
import os
from typing import List, Set, Optional
from famodels.models.state_of_trade import StateOfTrade
from famodels.models.direction import Direction
from famodels.models.order_type import OrderType
from famodels.models.side import Side
from typing import Optional
from redis_om import Migrator
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class VirtualOrder(JsonModel):
    """A cold order is used for forward testing / paper trading.
    """
    id: str = Field(index=True)
    signal_id: str = Field(index=True)
    invoked_by_hot_signal: int = Field(index=True)
    order_type: OrderType = Field(index=True, default=OrderType.LIMIT)        
    market: str = Field(index=True)
    direction: Direction = Field(index=True)
    side: Side = Field(index=True)
    price: float
    position_size_of_investment: float
    """The position size in % of the entire investment available."""
    amount: Optional[float]
    account: Optional[str]
    pos_idx: Optional[int]
    timestamp_of_order: int = Field(index=True)
    commission: float = Field(default=0.1)
    commission_amount: Optional[float]
    """The comission in percent. Default is 0.1%"""

    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    class Meta:
        global_key_prefix="performance-validation"
        model_key_prefix="virtual-order"        
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def __getitem__(self, key):
        return self.__dict__[key]
    
# Migrator().run()