from redis_om import Field, JsonModel, EmbeddedJsonModel
from redis_om.connections import get_redis_connection
import time

class InvestorStatement(JsonModel):
    id: str = Field(primary_key=True)
    investor_id: str = Field(index=True)
    timestamp: int = Field(index=True, default=int(time.time() * 1000))
    available_cash: float = Field(index=True, default=0)
    """All the available cash (in USDT)"""
    invested_assets_valued_in_quote: float = Field(index=True, default=0)
    """All the available assets - except the cash/quote currency - valued in quote currency (USDT)."""
    total_assets_value = float (Field(index=True, default=0))
    """Total values of invested assets + available cash = total_assets_value"""