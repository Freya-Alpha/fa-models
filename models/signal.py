from typing import Optional

from sqlmodel import Field, SQLModel

from models.direction import Direction
from models.side import Side

class BaseSignalSQLModel(SQLModel):
    def __init__(self, **kwargs):
        self.__config__.table = False
        super().__init__(**kwargs)
        self.__config__.table = True

    class Config:
        validate_assignment = True

class Signal(SQLModel, table=True):
    """A signal represents a signal from a algorithm and supplier. It must have a correlating id to a trade."""
    id: Optional[int] = Field(default=None, primary_key=True)
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
    # price: Optional[int] = None
