from pydantic import BaseModel, Field
from datetime import datetime
from famodels.direction import Direction
from enum import Enum

class OrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"

class StatusOfOrder(str, Enum):
    NEW = "new"
    SUBMITTED = "submitted"
    FILLING = "filling"
    CANCELED = "canceled"
    FILLED = "filled"

class Order(BaseModel):
    """An order is inherent part of a trade. Thus, a trade has at least one order.
        An this order is an order in different state. See that status attribute for execusion.
    """
    id: str = Field(...)
    signal_id: str = Field(...)
    algo_id: str = Field(...)
    status: StatusOfOrder = Field(default=StatusOfOrder.NEW)
    order_type: OrderType = Field(default=OrderType.LIMIT)
    market: str = Field(...)
    exchange: str = Field(...)
    direction: Direction = Field(...)
    price: float
    amount: float
    tp: float
    sl: float
    timestamp_of_order: datetime = Field(default_factory=datetime.now)
