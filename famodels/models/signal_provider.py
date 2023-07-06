from datetime import datetime
import os
from typing import List
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from models.algorithm import Algorithm
from models.person import Person
from enum import Enum

class StateOfProvider(str, Enum):    
    """Describing the possible states of signal provider. """
    REGISTERED = "registered"
    """When an signal provider is merely registered, but NOT authenticated with an official document. Registered allows cold trading."""
    QUALIFIED = "qualified"
    """When an signal provider is identified and authenticated by an offical document and qualified for hot trades. This is the highest state."""
    BANNED = "banned"
    """The signal provider was deliberatly banned from the system."""

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class SignalProvider(JsonModel):
    id: str = Field(index=True)   
    name: str = Field(index=True)
    accountable: Person = Field(index=True) 
    contact: Person = Field(index=True)
    state: StateOfProvider = Field(index=True, default=StateOfProvider.BANNED)
    algorithms: List[Algorithm] = Field(index=True)
    
    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="signal-provider"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
