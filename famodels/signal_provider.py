from pydantic import BaseModel, Field, field_validator
from typing import List
from famodels.strategy import Strategy
from famodels.person import Person
from enum import Enum

class StatusOfProvider(str, Enum):
    """Describing the possible states of signal provider. """
    NOT_AUTHENTICATED = "not_authenticated"
    """When a signal provider is merely registered, but NOT authenticated with an official document. Registered allows cold trading."""
    QUALIFIED = "qualified"
    """When a signal provider is authenticated by an official document and qualified for hot trades. This is the highest state."""
    BANNED = "banned"
    """The signal provider was deliberately banned from the system."""

class SignalProvider(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    accountable: Person = Field(...)
    contact: Person = Field(...)
    status: StatusOfProvider = Field(default=StatusOfProvider.NOT_AUTHENTICATED)
    algorithms: List[Strategy] = Field(...)

    @field_validator('name')
    def validate_name(cls, v):
        if not v or len(v) < 3:
            raise ValueError('name must be at least 3 characters long')
        return v
