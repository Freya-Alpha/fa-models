from datetime import datetime
import os, time, uuid
from famodels.models.direction import Direction
from typing import Optional
from redis_om import Migrator
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from enum import Enum


from enum import Enum
from typing import List, Set, Optional
from famodels.models.direction import Direction
from famodels.models.side import Side
from redis_om import (Field, EmbeddedJsonModel)
from redis_om.connections import get_redis_connection
import os

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

from enum import Enum

class OrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"

class StateOfOrder(str, Enum):    
    """Describing the possible states of an Order. Keep it simple. Also, we added the str to inherit from, so that the ENUM is serializable.         """
    NEW = "new"
    """It's new order, when the order is to be picked up by a fa-dex/cex-exchange-adapter. """
    SUBMITTED = "submitted"
    """The order is submitted and accepted but nothing was filled so far."""
    FILLING = "filling"
    """The order is about to be filled."""
    CANCELED = "canceled"
    """The order was canceled e.g. due to 'too long alive and not filled'."""
    FILLED = "filled"
    """Filled means the order filled completely and is thus closed."""

class Order(EmbeddedJsonModel):
    """This model is for hot orders ONLY! Use ColdOrder for paper trading.
    """
    id: str = Field(index=True)
    signal_id: str = Field(index=True)
    algo_id: str = Field(index=True)
    trade_id: str = Field(index=True)
    state: StateOfOrder = Field(index=True, default=StateOfOrder.NEW)
    order_type: OrderType = Field(index=True, default=OrderType.LIMIT)        
    market: str = Field(index=True)
    exchange: str = Field(index=True)
    direction: Direction = Field(index=True)
    side: Side = Field(index=True)
    price: float
    amount: float    
    account: str = Field(index=True)
    pos_idx: int = Field(index=True)
    timestamp_of_order: int = Field(index=True)
    comission: float    

    class Meta:
        # global_key_prefix="order-and-trade-processing"
        model_key_prefix="order"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def __getitem__(self, key):
        return self.__dict__[key]

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
    """A trade in our system is composed of a buy and a sell order (or multiple once.). Do not mistaken this trade for a trade from the CEX.
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
    """ This is one position of the fund. Which can consist of extra partial/scaled orders, if a provider_trade_id is supplied.
        The partial/scaled orders are tracked as orders.
    """
    market:str = Field(index=True)    
    state:StateOfTrade = Field(index=True, default=StateOfTrade.NEW)
    direction:Direction
    amount: float
    time_of_initiation:datetime = Field(index=True, default=int(time.time() * 1000))
    """When we decided to start this trade."""
    buy_order_list: Optional[Order] = None
    """ The list of opening/buying Orders. Mostly only one."""
    sell_order_list:Optional[Order] = None
    """ The list of closing/selling Orders. Mostly only one."""
    tp:Optional[float] = None
    """ The Take-Profit. The order engine will set a Sell-Limit-Order:
        a) once an order has been completely filled.
        b) if the order hast no completely been filled and a time-limit has been reached (only a few minutes) and thus partial Sell-Limit-Orders are being setup.
        """
    sl:Optional[float] = None
    """ The Stop-Loss. The order engine will set a Sell-Limit-Order:
        a) once an order has been completely filled.
        b) if the order hast no completely been filled and a time-limit has been reached (only a few minutes) and thus partial Sell-Limit-Orders are being setup.
        """
    """ The Stop-Loss.""" 
    profit_and_loss_percentage: Optional[float] = None
    """ Realized Percentage over all positions."""
    profit_and_loss_amount: Optional[float] = None
    """ Realized Amount over all positions."""

    class Meta:
        # global_key_prefix="order-and-trade-processing"
        model_key_prefix="trade"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def __getitem__(self, key):
        return self.__dict__[key]    
    
# Migrator().run()