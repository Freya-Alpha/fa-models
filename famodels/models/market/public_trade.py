from datetime import datetime
import os
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class PublicTrade(JsonModel):
    market: str = Field(index=True)
    exchange: str = Field(index = True)
    price: float = Field(index=True)
    quantity: float = Field(index=True)
    side: str = Field(index=True)
    timestamp: int = Field(index=True)

    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="public-trade"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)