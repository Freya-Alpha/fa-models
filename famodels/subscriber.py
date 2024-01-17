from datetime import datetime
import ipaddress
from pydantic import BaseModel, Field, field_validator, EmailStr

class Subscriber(BaseModel):
    email: EmailStr = None
    ip_address: ipaddress.IPv4Address = None
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('email')
    def val_email(cls, v: str) -> str:
        return str.strip(v)
