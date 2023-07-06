from datetime import datetime
import os
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from enum import Enum

class StateOfAlgorithm(str, Enum):    
    """Describing the possible states of an algorithm."""
    REGISTERED = "registered"
    """When an algorith is freshly registered but has not yet prooven performant."""
    QUALIFIED = "qualified"
    """When an algorithm has performed robustly over a longer time period."""
    DISQUALIFIED = "disqualified"
    """When an algorithm was previously qualified but now disqualified due to under-performing or suspicious actions."""
    BANNED = "banned"
    """The algorithm was banned due to deliberatly banned/blocked from the system. No signals will be allowed - not even for virtal trades."""

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Algorithm(JsonModel):
    algo_id: str = Field(index=True)   
    provider_id: str = Field(index=True) 
    state: StateOfAlgorithm = Field(index=True, default=StateOfAlgorithm)
    
    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="algorithm"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)


