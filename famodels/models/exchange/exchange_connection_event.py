from famodels.models.connection_event import ConnectionEvent
from redis_om import (Field)

class ExchangeConnectionEvent(ConnectionEvent):
    """A model to describe Connection events."""   
    investor_id: str = Field(index=True)
    exchange: str = Field(index=True)