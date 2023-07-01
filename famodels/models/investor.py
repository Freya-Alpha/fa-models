from datetime import datetime
import os
from typing import List, Optional
from pydantic import EmailStr
from redis_om import Field, JsonModel, EmbeddedJsonModel
from redis_om.connections import get_redis_connection
from famodels.models.person import Person
import hashlib
from cryptography.fernet import Fernet
from hashlib import sha256
from base64 import urlsafe_b64encode, urlsafe_b64decode

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

key = os.environ.get("ENCRYPTION_KEY").encode()
ENCRYPTION_KEY = urlsafe_b64encode(sha256(key).digest())

class Subscription(EmbeddedJsonModel):
    subscription_id: str = Field(index=False)
    algo_id:str = Field(index=True)
    
    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="subscription"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

class Fund(EmbeddedJsonModel):
    fund_id:str = Field(index=True)
    name:str = Field(index=True)
    investor_id:str = Field(index=True)    
    subscriptions: Optional[List[Subscription]] = Field(index=False)  
    compounding: int = Field(index=True, default=1)
    absolute_max_amount: Optional[float]
    
    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="fund"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def add_subscription(self, subscription):
        if subscription not in self.subscriptions:
            self.subscriptions.append(subscription)


class EncryptionService:
    def __init__(self, key: str):
        self.key = urlsafe_b64encode(sha256(key.encode()).digest())

    def encrypt(self, value: str) -> str:
        f = Fernet(self.key)
        return f.encrypt(value.encode()).decode()

    def decrypt(self, encrypted_value: str) -> str:
        f = Fernet(self.key)
        return f.decrypt(encrypted_value.encode()).decode()


class ExchangeKey(EmbeddedJsonModel):
    exchange: str = Field(index=True)
    key_id: str = Field(index=True)
    _key_secret: str = Field(index=False)

    def set_key_secret(self, value: str, encryption_service: EncryptionService):
        self._key_secret = encryption_service.encrypt(value)

    def get_key_secret(self, encryption_service: EncryptionService) -> str:
        return encryption_service.decrypt(self._key_secret)

    class Meta:
        model_key_prefix = "exchange-key"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)



class Investor(JsonModel):
    investor_id: str = Field(index=True)
    email: EmailStr = Field(index=True)
    accountable: Person = Field(index=True)        
    _passphrase: str = Field(index=False)
    #library constraint: "redis_om.model.model.RedisModelError: In this Preview release, list and tuple fields can only contain strings. Problem field: compounding"
    # funds: Optional[List[Fund]]
    exchange_keys: Optional[List[ExchangeKey]]

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
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="investor"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
