import re
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from enum import Enum

class IdentificationType(str, Enum):
    PASSPORT = "PASSPORT"
    IDENTIFICATION_CARD = "IDENTIFICATION_CARD"

class Person(BaseModel):
    given_name: Optional[str] = Field(None)
    family_name: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    gender: str = Field(default="na")
    nationality_iso2: str = Field(...)
    identification_type: Optional[IdentificationType] = Field(None)
    identification_reference: Optional[str] = Field(None)
    country_of_residence_iso2: str = Field(...)
    building_address: Optional[str] = Field(None)
    street_address: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    zip: Optional[str] = Field(None)
    province: Optional[str] = Field(None)
    phone: Optional[str] = Field(default="")
    timestamp: Optional[int] = Field(None)

    @field_validator("identification_type")
    def convert_to_enum(cls, v):
        if isinstance(v, str):
            try:
                return IdentificationType(v)
            except ValueError:
                raise ValueError("Invalid identification type")
        return v

    @field_validator('gender')
    def validate_gender(cls, v):
        if v not in ["m", "f", "na"]:
            raise ValueError("gender must be 'm', 'f', or 'na'")
        return v

    @field_validator('nationality_iso2', 'country_of_residence_iso2')
    def validate_iso2(cls, v):
        if not re.match(r"^[A-Z]{2}$", v):
            raise ValueError("Value must be a valid ISO2 country code")
        return v
