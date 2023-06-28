from datetime import datetime
import os
from typing import List
from pydantic import EmailStr
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from models.exchange_key import ExchangeKey
from models.fund import Fund
import hashlib

from models.person import Person

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Investor(Person):
    investor_id: str = Field(index=True)
    email: EmailStr = Field(index=True)
    sex: int = Field(index=True)    
    _passphrase: str = Field(index=False)
    funds = List[Fund] = Field(index=True)
    exchange_keys = List[ExchangeKey] = Field(index=True)

    @property
    def passphrase(self):
        raise Exception("Cannot retrieve passphrase.")
        
    @passphrase.setter
    def passphrase(self, value):
        hashed_value = hashlib.sha256(value.encode()).hexdigest()
        self._passphrase = hashed_value

    def verify_passphrase(self, value):
        return self._passphrase == hashlib.sha256(value.encode()).hexdigest()

    class Meta:
        global_key_prefix="fa-investor-processing"
        model_key_prefix="investor"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
