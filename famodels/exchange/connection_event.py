from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ConnectionStatus(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"

class ConnectionEvent(BaseModel):
    """A model to describe Connection events."""
    targetSystem: str = Field(...)
    status: ConnectionStatus = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
