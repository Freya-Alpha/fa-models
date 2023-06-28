from datetime import datetime
import os
from typing import List
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from models.person import Person

from models.algorithm import Algorithm

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class SignalSupplier(JsonModel):    
    provider_id: str = Field(index=True) 
    name: str = Field(index=True)
    accountable: Person = Field(index=True)
    contact: Person = Field(index=True)
    is_qualified: bool = Field(index=True, default=0)
    algorithms: List[Algorithm] = Field(index=True)
    
    class Meta:
        global_key_prefix="fa-investor-processing"
        model_key_prefix="signal-supplier"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
