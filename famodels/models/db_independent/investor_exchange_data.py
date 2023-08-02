from base64 import urlsafe_b64encode
from hashlib import sha256
import os
from cryptography.fernet import Fernet

class InvestorExchangeData():
    """This is a data extraction of the Investor model and redis-independent."""
    investor_id:id
    exchange:str

