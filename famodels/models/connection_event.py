from datetime import datetime
from enum import Enum
import os
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class ConnectionStatus(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"

class ConnectionEvent(JsonModel):
    """A model to describe Connection events."""        
    targetSystem: str = Field(index=True)
    status: ConnectionStatus = Field()
    timestamp: int = Field(index=True, sortable=True, default=int(datetime.now().timestamp() * 1000))
    
