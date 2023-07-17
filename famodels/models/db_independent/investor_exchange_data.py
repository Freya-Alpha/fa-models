from base64 import urlsafe_b64encode
from hashlib import sha256
from cryptography.fernet import Fernet


class EncryptionService:
    def __init__(self, key: str):
        self.key = urlsafe_b64encode(sha256(key.encode()).digest())

    def encrypt(self, value: str) -> str:
        f = Fernet(self.key)
        return f.encrypt(value.encode()).decode()

    def decrypt(self, encrypted_value: str) -> str:
        f = Fernet(self.key)
        return f.decrypt(encrypted_value.encode()).decode()

class InvestorExchangeData():
    """This is a data extraction of the Investor model and redis-independent."""
    investor_id:id
    exchange:str
    key_id:str
    def set_key_secret(self, value: str, encryption_service: EncryptionService):
        self._key_secret = encryption_service.encrypt(value)

    def get_key_secret(self, encryption_service: EncryptionService) -> str:
        return encryption_service.decrypt(self._key_secret)

