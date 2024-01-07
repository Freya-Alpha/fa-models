from pydantic import Field
from connection_event import ConnectionEvent

class ExchangeConnectionEvent(ConnectionEvent):
    """A model to describe Connection events specific to an exchange."""
    investor_id: str = Field(...)
    exchange: str = Field(...)

    # Additional validators can be added as needed
