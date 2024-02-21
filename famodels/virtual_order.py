from pydantic import BaseModel, Field, field_validator
from typing import Optional
from famodels.direction import Direction
from famodels.order_type import OrderType
from datetime import datetime

class VirtualOrder(BaseModel):
    """Virtual Orders are a representation of cold orders. They are not expected to be executed on any exchange.."""
    id: str = Field(...)
    signal_id: str = Field(...)
    invoked_by_hot_signal: bool = Field(...)
    order_type: OrderType = Field(default=OrderType.LIMIT)
    market: str = Field(...)
    direction: Direction = Field(...)
    price: float = Field(...)
    position_size_of_investment: float = Field(...)
    amount: Optional[float] = Field(None)
    account: Optional[str] = Field(None)
    pos_idx: Optional[int] = Field(None)
    timestamp_of_order: datetime = Field(default_factory=datetime.now)
    commission: float = Field(default=0.1)
    commission_amount: Optional[float] = Field(None)

    @field_validator('invoked_by_hot_signal')
    def validate_invoked_by_hot_signal(cls, v):
        if not isinstance(v, bool):
            raise ValueError('invoked_by_hot_signal must be a boolean')
        return v

