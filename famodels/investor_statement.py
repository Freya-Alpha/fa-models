from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import time

class InvestorStatement(BaseModel):
    """Describes a snapshot of an investor at a given time."""
    id: str = Field(...)
    investor_id: str = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.fromtimestamp(time.time()))
    available_cash: float = Field(default=0, description="All the available cash (in USDT)")
    invested_assets_valued_in_quote: float = Field(default=0, description="All the available assets - except the cash/quote currency - valued in quote currency (USDT).")
    total_assets_value: float = Field(default=0, description="Total values of invested assets + available cash")

    @field_validator('available_cash', 'invested_assets_valued_in_quote', 'total_assets_value')
    def validate_asset_values(cls, v):
        if v < 0:
            raise ValueError("Asset values must be non-negative")
        return v
