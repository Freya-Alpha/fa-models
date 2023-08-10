from datetime import datetime
from enum import Enum
import os
from typing import List, Optional
from pydantic import EmailStr, validator
from redis_om import (Field, JsonModel, EmbeddedJsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class IdentificationType(Enum):
    PASSPORT = "PASSPORT"
    IDENTIFICATION_CARD = "IDENTIFICATION_CARD"

class Person(EmbeddedJsonModel):    
    given_name: Optional[str] = Field(index=True)
    family_name: Optional[str] = Field(index=True, full_text_search=True)
    email: Optional[EmailStr] = Field(index=True)
    gender: str = Field(index=True, max_length=2, default="na")    
    """m, f, na"""
    nationality_iso2: str = Field(index=True, max_length=2, min_length=2)
    identification_type: Optional[IdentificationType]
    identification_reference: Optional[str]
    country_of_residence_iso2: str = Field(index=True, max_length=2, min_length=2)
    building_address: Optional[str] = Field(index=True) 
    street_address: Optional[str] = Field(index=True)
    city: Optional[str] = Field(index=True)
    zip: Optional[str] = Field(index=True)
    province: Optional[str] = Field(index=True)
    phone: Optional[str] = Field(index=True, default="")
    timestamp: Optional[int] = Field(sortable=True)

    # this validator will help to keep the identification type valid.
    # If the values has been passed as a string, it will try to convert it.
    @validator("identification_type", pre=True)
    def convert_to_enum(cls, v):
        if isinstance(v, str):
            return IdentificationType(v)
        return v
    
    class Meta:
        # global_key_prefix=""
        model_key_prefix="person"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
