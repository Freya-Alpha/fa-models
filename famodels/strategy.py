from pydantic import BaseModel, Field
from enum import Enum

class StatusOfStrategy(str, Enum):
    """Describing the possible states of an algorithm."""
    REGISTERED = "registered"
    """When an algorithm is freshly registered but has not yet proven performant."""
    QUALIFIED = "qualified"
    """When an algorithm has performed robustly over a longer time period."""
    DISQUALIFIED = "disqualified"
    """When an algorithm was previously qualified but now disqualified due to under-performing or suspicious actions."""
    BANNED = "banned"
    """The algorithm was banned due to deliberately being banned/blocked from the system. No signals will be allowed - not even for virtual trades."""

class Strategy(BaseModel):
    algo_id: str = Field(...)
    provider_id: str = Field(...)
    status: StatusOfStrategy = Field(default=StatusOfStrategy.REGISTERED)
