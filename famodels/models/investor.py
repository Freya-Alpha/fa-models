from datetime import datetime
import os
from typing import List, Optional
from pydantic import EmailStr
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
# from famodels.models.exchange_key import ExchangeKey
# from famodels.models.fund import Fund
# from famodels.models.person import Person
import hashlib

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Investor(JsonModel):
    investor_id: str = Field(index=True)
    email: EmailStr = Field(index=True)
    # accountable: Person = Field(index=True)        
    # _passphrase: str = Field(index=False)
    # library constraint: "redis_om.model.model.RedisModelError: In this Preview release, list and tuple fields can only contain strings. Problem field: compounding"
    #funds: Optional[List[Fund]] = Field(default=None, index=False)
    # exchange_keys: Optional[List[ExchangeKey]] = Field(default=None, index=False)

    # @property
    # def passphrase(self):
    #     raise Exception("Cannot retrieve passphrase.")
        
    # @passphrase.setter
    # def passphrase(self, value):
    #     hashed_value = hashlib.sha256(value.encode()).hexdigest()
    #     self._passphrase = hashed_value

    # def verify_passphrase(self, value):
    #     return self._passphrase == hashlib.sha256(value.encode()).hexdigest()

    class Meta:
        global_key_prefix="fa-investor-processing"
        model_key_prefix="investor"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
