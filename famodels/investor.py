from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
from famodels.person import Person
from famodels.fund.fund import Fund  # Assuming Fund is also refactored as a Pydantic model
from enum import Enum
import bcrypt

class StatusOfInvestor(str, Enum):
    REGISTERED = "registered"
    QUALIFIED = "qualified"
    BANNED = "banned"
    DELETED = "deleted"

class Investor(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    is_company: int = Field(default=False)
    accountable: Optional[Person]
    status: StatusOfInvestor = Field(default=StatusOfInvestor.REGISTERED)
    _passphrase: Optional[str]
    funds: Optional[List[Fund]] = []
    priviledge_rank: int = Field(default=1)
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("name must be at least 3 characters long")
        return v

    @property
    def passphrase(self):
        raise Exception("Cannot retrieve passphrase.")

    def set_passphrase(self, passphrase: str):
        if isinstance(passphrase, str):
            passphrase = passphrase.encode()
        salt = bcrypt.gensalt()
        self._passphrase = bcrypt.hashpw(passphrase, salt).decode()

    def verify_passphrase(self, passphrase: str):
        if isinstance(passphrase, str):
            passphrase = passphrase.encode()
        encoded_passphrase = self._passphrase.encode() if isinstance(self._passphrase, str) else self._passphrase
        return bcrypt.checkpw(passphrase, encoded_passphrase)

    def is_qualified(self) -> bool:
        return self.status == StatusOfInvestor.QUALIFIED
