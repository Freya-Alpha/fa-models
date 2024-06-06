from datetime import datetime
import ipaddress
from enum import Enum
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr


class EmailSubscriptionAction(str, Enum):
    SUBSCRIBE = "Subscribe"
    UNSUBSCRIBE = "Unsubscribe"


class EmailSubscriberBaseModel(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True, str_strip_whitespace=True)

    ip_address: ipaddress.IPv4Address = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('ip_address')
    @classmethod
    def val_ip_address(cls, ip_address: ipaddress.IPv4Address) -> str:
        return str.strip(ip_address.compressed)


class EmailSubscriberIn(EmailSubscriberBaseModel):
    email: EmailStr = Field(...)
    subscription_action: EmailSubscriptionAction = Field(...)


class EmailSubscriberInForward(EmailSubscriberBaseModel):
    id: str = Field(default=str(uuid.uuid4()))
    email_encrypted: str = Field(...)
    subscription_action: EmailSubscriptionAction = Field(...)


class EmailSubscriberInDb(EmailSubscriberInForward):
    ip_address_city: Optional[str] = Field(None)
    ip_address_region: Optional[str] = Field(None)
    ip_address_country: Optional[str] = Field(None)
    ip_address_location_lat: Optional[str] = Field(default=None,
                                                   pattern=r"^-?([0-8]?[0-9]|90)(\.[0-9]{1,20})$")
    ip_address_location_lon: Optional[str] = Field(default=None,
                                                   pattern=r"^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,20})$")
