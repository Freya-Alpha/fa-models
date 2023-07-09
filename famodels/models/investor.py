import os
import time
from typing import List, Optional
from pydantic import EmailStr
from redis_om import Field, JsonModel, EmbeddedJsonModel
from redis_om.connections import get_redis_connection
from famodels.models.person import Person
from cryptography.fernet import Fernet
from hashlib import sha256
import bcrypt
from base64 import urlsafe_b64encode

from enum import Enum

class StateOfInvestor(str, Enum):    
    """Describing the possible states of an Investor. Keep it simple. Also, we added the str to inherit from, so that the ENUM is serializable.         """
    REGISTERED = "registered"
    """When an investor is merely registered, but NOT authenticated with an official document. Registered allows cold trading."""
    QUALIFIED = "qualified"
    """When an investor is identified and authenticated by an offical document and qualified for hot trades. This is the highest state."""
    BANNED = "banned"
    """The investor was deliberatly banned from the system."""

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

key = os.environ.get("ENCRYPTION_KEY").encode()
ENCRYPTION_KEY = urlsafe_b64encode(sha256(key).digest())

class Subscription(EmbeddedJsonModel):
    id: str = Field(index=False)
    algo_id:str = Field(index=True)
    # redis model can only store these fields of the embedded json model as string
    start_timestamp:Optional[str]
    stop_timestamp: Optional[str]

    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="subscription"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

class Fund(EmbeddedJsonModel):
    id:str = Field(index=True)
    name:str = Field(index=True)    
    compounding: str = Field(index=True, default="true")
    """Marks the investment as to be compounded with every trade. CAUTION: Due to redis-om model restrictions this could not be a boolean as it's value suggests. The workaround is a str with values 'true' and 'false'. Default is 'true'. Will bechanged as soon the redis-om library has enhanced."""
    subscriptions: Optional[List[Subscription]]  
    number_of_positions: int = Field(index=False, default=5)
    max_amount: Optional[float]
    """The max amount in quote currency to invest. e.g. 10'000 (USDT)."""
    
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
    exchange: str = Field(index=True,)
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
    id: str = Field(index=True)
    name: str = Field(index=True, full_text_search=True)
    """company name or givenname & family name"""
    email: EmailStr = Field(index=True)
    accountable: Person = Field(index=True)        
    state: StateOfInvestor = Field(index=True, default=StateOfInvestor.REGISTERED.value)
    _passphrase: Optional[str]
    #library constraint: "redis_om.model.model.RedisModelError: In this Preview release, list and tuple fields can only contain strings. Problem field: compounding"
    funds: Optional[List[Fund]]
    exchange_keys: Optional[List[ExchangeKey]]
    priviledge_rank: int = Field(index=True, default=1, sortable=True)
    """The higher the value, the higher the priviledge."""

    @property
    def passphrase(self):
        raise Exception("Cannot retrieve passphrase.")
    
    def setPassphrase(self, passphrase:str):
        """Use this method to set a password. The pydantic setter method does not work with JsonModel."""
        encoded_pw = passphrase.encode()
        # Adding the salt to prefent Rainbow Table Attacks and avoiding to hash the same password with the same hash.
        # DO NOT USE A STATIC SALT!
        salt = bcrypt.gensalt()
        self._passphrase = bcrypt.hashpw(encoded_pw, salt)

    def verify_passphrase(self, passphrase: str):
        return bcrypt.checkpw(passphrase.encode(), self._passphrase)    
    
    def is_qualified(self):
        return self.state == StateOfInvestor.QUALIFIED
    
    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="investor"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
