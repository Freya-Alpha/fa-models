import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
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
    algo_id: str
    """Provide the id of your algorithm entity (you might have more than one algorithm), which is sending this signal.  We have issued this id."""
    provider_id: str
    """The ID of the provider, who emitted the signal."""
    market: str    
    exchange: str
    trade_correlation_id: str
    """A signal without a trade intention makes has no value to us. Thus there always must be a trade id."""
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
    