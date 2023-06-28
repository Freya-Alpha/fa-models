from datetime import datetime
import os
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode, urlsafe_b64decode

KEY = urlsafe_b64encode(os.environ.get("ENCRYPTION_KEY").encode())

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class ExchangeKey(JsonModel):
    exchange: str = Field(index=True)
    key_id: str = Field(index=True)
    _key_secret:str = Field(index=False)
    _key_passphrase:str = Field(index=False)

    @property
    def key_secret(self):
        f = Fernet(KEY)
        return f.decrypt(self._key_secret.encode()).decode()

    @key_secret.setter
    def key_secret(self, value):
        f = Fernet(KEY)
        self._key_secret = f.encrypt(value.encode()).decode()

    @property
    def key_passphrase(self):
        f = Fernet(KEY)
        return f.decrypt(self._key_passphrase.encode()).decode()

    @key_passphrase.setter
    def key_passphrase(self, value):
        f = Fernet(KEY)
        self._key_passphrase = f.encrypt(value.encode()).decode()
    
    class Meta:
        global_key_prefix="fa-investor-processing"
        model_key_prefix="exchange-key"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
