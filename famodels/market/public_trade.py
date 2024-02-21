from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from famodels.direction import Direction

class PublicTrade(BaseModel):
    market: str = Field(...)
    exchange: str = Field(...)
    price: float = Field(...)
    quantity: float = Field(...)
    direction: Direction = Field(...)
    timestamp: datetime = Field(...)

    @field_validator('price', 'quantity')
    def check_positive(cls, v, field):
        if v <= 0:
            raise ValueError(f"{field.name} must be positive")
        return v

    @field_validator('timestamp')
    def validate_timestamp(cls, v):
        if v < datetime(1970, 1, 1):
            raise ValueError("timestamp must be a datetime after Unix epoch (1970-01-01)")
        return v
