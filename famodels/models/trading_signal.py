import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
import uuid
from sqlmodel import Field, SQLModel
from famodels.models.direction import Direction
from famodels.models.side import Side

class BaseSignalSQLModel(SQLModel):
    def __init__(self, **kwargs):
        self.__config__.table = False
        super().__init__(**kwargs)
        self.__config__.table = True

    class Config:
        validate_assignment = True

class TradingSignal(SQLModel, table=True):
    """A trading signal represents a suggestion to buy or sell. It is issued by a signal supplier (manually or algorithmically). It must have a correlating id to a trade."""
    id: Optional[str] = Field(default=None, primary_key=True)
    """The id is marked optional - because it will be created by either SQL DB or a async method in an event-driven system.
        If you add an id here, it will be copied to the trade_correlation_id.
    """
    supplier_correlation_id: Optional[str]
    """You can use this correlation id as your own 'signal id' of your internal system. 
    Do not mistaken this correlation id with the trade correlation id."""    
    trade_correlation_id: str
    """FA Models describes a Trade as a buy and a sell (not soley a buy or a sell). 
    Every trade is expected to consist of at least one buy order and zero or more sell orders. 
    Thus, the trade_correlation_id is mandatory. Use this correlation id to link your signals to a trade. In other words, it is a grouping functionality."""
    is_hot_signal: bool = False
    """By default, every signal is marked as a cold signal. Thus, set to false. That is a paper-trading signal and will only be processed for forward-performance testing. 
    Hot signals are suggested to be processed by the order engines - provided all other requirements for hot trading are fulfilled."""    
    algo_id: str
    """Provide the id of your algorithm id (you might have more than one algorithm), which is sending a signal. """
    provider_id: str
    """The ID of the provider, who emitted the signal."""
    market: str    
    """The market you want to trade. e.g. TSLA/USD"""
    exchange: str
    """The exchange you pulled your data from - or - wish to trade on."""
    direction: Direction
    """The direction is actually provided by the trade, which is referenced by the correlation id. """
    side: Side
    price: float
    tp: float
    sl: float
    timestamp_of_creation: int
    """The timestamp in milliseconds when the signal was created by the signal supplier."""
    timestamp_of_registration: Optional[int]
    """The timestamp in milliseconds when the signal was entering our interface. This will be overridden."""
    position_size_of_investment: float = 100
    """Percentage of the investment position this algortihm is allowed to trade. Default is 100%, which is 1 position."""  
    