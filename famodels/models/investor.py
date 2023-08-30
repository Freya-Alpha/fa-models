from datetime import datetime
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
    DELETED = "deleted"
    """ This investor is flagged for deletion."""


REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

key = os.getenv("ENCRYPTION_KEY","my_value").encode()
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
    investment_ratio: float = Field(index=False, default=None)
    """ The ratio of the total assets this investment can manage. It is a number between 1 and 0. 
        The ratio-balancer will consume this value, the total assets, the fixed_max_amount to compute the max_amount.
    None means: as much as one can."""
    number_of_positions: int = Field(index=False, default=5)
    """ Number of positions this fund allows. 
        Do not mistaken it for trade-positions, a signal provider uses to scale-in and out on positions with a shared TP/SL."""
    fixed_max_amount: float = Field(index=False, default=None)
    """This can be optional set by the investor. The max_amount can NEVER be higher than the fixed_max_amount."""
    max_amount: Optional[float]
    """The max amount in quote currency to invest. e.g. 10'000 (USDT)
    It is computed possible in real time by the ratio-balancer triggered by events like: new or deleted funds, closed orders, investor statements, depositing money, withdrawing money, change of fixed_max_amount.
    """
    
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
    name: str = Field(index=True, full_text_search=True, default="")
    """company name or full private name"""
    email: EmailStr = Field(index=True)
    is_company: int = Field(index=True, default=0)
    accountable: Optional[Person] #= Field(index=True) # cannot be optional, otherwise, we need to send full person data on creation-time.      
    """Mandatory, if it is a company."""
    state: StateOfInvestor = Field(index=True, default=StateOfInvestor.REGISTERED.value)
    # credential: Credential = Field(index=False)
    _passphrase: Optional[str]
    #library constraint: "redis_om.model.model.RedisModelError: In this Preview release, list and tuple fields can only contain strings. Problem field: compounding"
    funds: Optional[List[Fund]]
    exchange_keys: Optional[List[ExchangeKey]]
    priviledge_rank: int = Field(index=True, default=1, sortable=True)
    """The higher the value, the higher the priviledge."""
    timestamp: Optional[int] = Field(index=True, sortable=True)
    """Record, when this record was created. Needs to be determined by the business logic, not by the data logic."""    

    @property
    def passphrase(self):
        raise Exception("Cannot retrieve passphrase.")
    
    def get_encrypted_passphrase(self):
        """Return the password, but not encrypted. Use verify_password to check passwords."""
        return self._passphrase

    def set_encrypted_password(self, encrypted_password:str):
        """Only use this function to set an already encrypted password. E.g. for field-copying actions."""
        self._passphrase = encrypted_password
    
    def set_passphrase(self, passphrase:str):
        """Use this method to set a password. The pydantic setter method does not work with JsonModel."""
        if isinstance(passphrase, str):
            passphrase = passphrase.encode()
        # Adding the salt to prefent Rainbow Table Attacks and avoiding to hash the same password with the same hash.
        # DO NOT USE A STATIC SALT!
        salt = bcrypt.gensalt()
        self._passphrase = bcrypt.hashpw(passphrase, salt)

    def verify_passphrase(self, passphrase: str):
        if isinstance(passphrase, str):
            passphrase = passphrase.encode()
        encoded_passphrase = self._passphrase.encode() if isinstance(self._passphrase, str) else self._passphrase
        return bcrypt.checkpw(passphrase, encoded_passphrase)    
    
    def is_qualified(self):
        return self.state == StateOfInvestor.QUALIFIED
    
    class Meta:
        # global_key_prefix="fa-investor-processing"
        model_key_prefix="investor"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
