from typing import Optional

from sqlmodel import Field, SQLModel

from models.direction import Direction
from models.side import Side


class Signal(SQLModel, table=False):
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
