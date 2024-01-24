from datetime import datetime
import ipaddress
from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr

class SubscriberBaseModel(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    ip_address: ipaddress.IPv4Address = Field(..., strip_withspace=True)
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('ip_address')
    def val_ip_address(cls, v: ipaddress.IPv4Address) -> ipaddress.IPv4Address:
        return str.strip(v.compressed)    

class SubscriberIn(SubscriberBaseModel):
    email: EmailStr = Field(..., strip_withspace=True)

class SubscriberInDb(SubscriberBaseModel):
    id: str = None
    email_encrypted: str = None
    ip_address_city: str = None
    ip_address_region: str = None
    ip_address_country: str = None
    ip_address_location_lat: str = Field(pattern=r"^-?([0-8]?[0-9]|90)(\.[0-9]{1,10})$")
    ip_address_location_lon: str = Field(pattern=r"^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,10})$")
