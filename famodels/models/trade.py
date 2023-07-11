from datetime import datetime
import os, time, uuid
from famodels.models.direction import Direction
from typing import Optional
from redis_om import Migrator
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from enum import Enum

class StateOfTrade(str, Enum):    
    """Describing the possible states of a Trade. Keep it simple. Also, we added the str to inherit from, so that the ENUM is serializable.         """
    NEW = "new"
    BUYING = "buying"    
    """BUYING means that we have at least submitted an order to buy."""
    WAITING_FOR_SELL_DECISION = "waiting_for_sell_decision"
    """Indicates, the the buy has been completed and we are waiting for a sell order to be sent."""
    SELLING = "selling"
    """SELLING means that a sell-order (close position) has been sent to the CEX. """
    CANCELED = "canceled"
    """Cancelled is the state where a trade was canceled but cleaned up (i.e. sold what was previously bought. Or bought-back what was previously sold)."""
    CLOSED = "closed"
    """Closed means the trade did buy completely and sold completely."""

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"the env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Trade(JsonModel):
    """A trade in our system is composed of a buy and a sell order. Do not mistaken it for a trade from the CEX.
        Create a new Trade record for every update and correlate them with trade_id. See attribute #trade_id"""   
    # id: Optional[int] = Field(default=None, primary_key=True)    
    id: str = Field(primary_key=True)
    # sort_index:int = field(init=False, repr=False)
    #trade_id: Optional[str] = Field(default=uuid.uuid4(), primary_key=True)
    """The trade id is the reference that keeps the state updates correlated. It will generate a UUID by default.
        Use this for the first record you insert. Inserting updated records (new records should then have the trade_id
        provided to create the correlation.)"""
    investor_id: str = Field(index=True)
    fund_id: str = Field(index=True)
    fund_pos_idx:int
    market:str = Field(index=True)    
    state:StateOfTrade = Field(index=True, default=StateOfTrade.NEW)
    direction:Direction
    amount: float
    time_of_initiation:datetime = Field(index=True, default=int(time.time() * 1000))
    """When we decided to start this trade."""
    buy_order_id: Optional[str] = None
    sell_order_id:Optional[str] = None
    take_profit:Optional[float] = None
    stop_loss:Optional[float] = None
    """This is usually the receiving timestamp."""        
    profit_and_loss_percentage: Optional[float] = None
    profit_and_loss_amount: Optional[float] = None

    class Meta:
        # global_key_prefix="order-and-trade-processing"
        model_key_prefix="trade"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def __getitem__(self, key):
        return self.__dict__[key]    
    
# Migrator().run()