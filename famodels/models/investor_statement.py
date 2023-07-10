from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
import os, time

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")


class InvestorStatement(JsonModel):
    id: str = Field(primary_key=True)
    investor_id: str = Field(index=True)
    timestamp: int = Field(index=True, default=int(time.time() * 1000))
    available_cash: float = Field(index=True, default=0)
    """All the available cash (in USDT)"""
    invested_assets_valued_in_quote: float = Field(index=True, default=0)
    """All the available assets - except the cash/quote currency - valued in quote currency (USDT)."""
    total_assets_value = float = (Field(index=True, default=0))
    total_assets_value = float = (Field(index=True, default=0))
    """Total values of invested assets + available cash = total_assets_value"""

    class Meta:
        # global_key_prefix="order-and-trade-processing"
        model_key_prefix="investor-statement"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)