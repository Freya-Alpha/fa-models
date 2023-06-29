from datetime import datetime
import os
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Subscription(JsonModel):
    subscription_id: str = Field(index=False)
    algo_id:str = Field(index=True)
    
    class Meta:
        global_key_prefix="fa-investor-processing"
        model_key_prefix="subscription"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)