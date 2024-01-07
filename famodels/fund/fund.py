from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Fund(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    risk_level: Optional[int] = Field(None, description="Risk level from 1 (low risk) to 10 (extreme risk). None is acceptable.")
    compounding: bool = Field(default=True)

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("name must be at least 3 characters long")
        return v

    @field_validator('risk_level')
    def validate_risk_level(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError("risk_level must be between 1 and 10")
        return v
