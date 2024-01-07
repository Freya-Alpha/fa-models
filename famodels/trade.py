from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from famodels.direction import Direction
from famodels.order import Order
from enum import Enum

class StatusOfTrade(str, Enum):
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

class Trade(BaseModel):
    """A trade in our system is composed of a buy and a sell order (or multiple once.). Do not mistaken this trade for a trade from the CEX.
        Create a new Trade record for every update and correlate them with trade_id. See attribute #trade_id"""
    id: str = Field(primary_key=True, description="The trade id is the reference that keeps the state updates correlated. It will generate a UUID by default. Use this for the first record you insert. Inserting updated records (new records should then have the trade_id provided to create the correlation.)")
    investor_id: str = Field(...)
    provider_id: str = Field(...)
    provider_trade_id: Optional[str] = Field(None, description="This id can be sent optionally (together with position_size_in_percent) by the signal provider to make this a multi-position-trade. CAUTION: This trade id has to be unique for each multi-position-trade one is attempting to run.")
    fund_id: str = Field(...)
    fund_pos_idx: int = Field(..., description="This is one position of the fund. Which can consist of extra partial/scaled orders, if a provider_trade_id is supplied. The partial/scaled orders are tracked as orders.")
    market: str = Field(...)
    status: StatusOfTrade = Field(default=StatusOfTrade.NEW)
    direction: Direction = Field(...)
    amount: float = Field(...)
    time_of_initiation: datetime = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="When an entity decided to call this trade.")
    buy_order_list: Optional[List[Order]] = None
    """ The list of opening/buying Orders. Mostly only one."""
    sell_order_list: Optional[List[Order]] = None
    """ The list of closing/selling Orders. Mostly only one."""

    tp: Optional[float] = None
    """ The Take-Profit price. The order engine will set a Sell-Limit-Order:
        a) once an order has been completely filled.
        b) if the order has not completely been filled and a time-limit has been reached (only a few minutes) and thus partial Sell-Limit-Orders are being setup.
        """
    sl: Optional[float] = None
    """ The Stop-Loss price. The order engine will set a Sell-Limit-Order:
        a) once an order has been completely filled.
        b) if the order has not completely been filled and a time-limit has been reached (only a few minutes) and thus partial Sell-Limit-Orders are being setup.
        """
    """ The Stop-Loss."""
    profit_and_loss_percentage: Optional[float] = None
    """ Realized Percentage over all positions."""
    profit_and_loss_amount: Optional[float] = None
    """ Realized Amount over all positions."""
