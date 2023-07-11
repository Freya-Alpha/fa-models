from enum import Enum
from typing import List, Set, Optional
from famodels.models.direction import Direction
from famodels.models.order_type import OrderType
from famodels.models.side import Side
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
import os

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")


class StateOfOrder(str, Enum):    
    """Describing the possible states of an Order. Keep it simple. Also, we added the str to inherit from, so that the ENUM is serializable.         """
    NEW = "new"
    """It's new order, when the order is to be picked up by a fa-dex/cex-exchange-adapter. """
    SUBMITTED = "submitted"
    """The order is submitted and accepted but nothing was filled so far."""
    FILLING = "filling"
    """The order is about to be filled."""
    CANCELED = "canceled"
    """The order was canceled e.g. due to 'too long alive and not filled'."""
    FILLED = "filled"
    """Filled means the order filled completely and is thus closed."""

class Order(JsonModel):
    """This model is for hot orders ONLY! Use ColdOrder for paper trading.
    """
    id: str = Field(index=True)
    signal_id: str = Field(index=True)
    algo_id: str = Field(index=True)
    trade_id: str = Field(index=True)
    state: StateOfOrder = Field(index=True, default=StateOfOrder.NEW)
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