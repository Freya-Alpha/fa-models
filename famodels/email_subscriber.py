from datetime import datetime
import ipaddress
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr

class EmailSubscriberBaseModel(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True, str_strip_whitespace=True)

    ip_address: ipaddress.IPv4Address = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('ip_address')
    def val_ip_address(cls, v: ipaddress.IPv4Address) -> ipaddress.IPv4Address:
        return str.strip(v.compressed)

class EmailSubscriberIn(EmailSubscriberBaseModel):
    email: EmailStr = Field(...)

class EmailSubscriberInDb(EmailSubscriberBaseModel):
    id: str = Field(default=str(uuid.uuid4()))
    email_encrypted: str = Field(...)
    ip_address_city: Optional[str] = Field(None)
    ip_address_region: Optional[str] = Field(None)
    ip_address_country: Optional[str] = Field(None)
    ip_address_location_lat: str = Field(pattern=r"^-?([0-8]?[0-9]|90)(\.[0-9]{1,20})$")
    ip_address_location_lon: str = Field(pattern=r"^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,20})$")
