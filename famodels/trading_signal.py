from typing import Optional
from sqlmodel import Field, SQLModel
from famodels.direction import Direction
from famodels.side import Side

class BaseSignalSQLModel(SQLModel):
    def __init__(self, **kwargs):
        self.__config__.table = False
        super().__init__(**kwargs)
        self.__config__.table = True

    class Config:
        validate_assignment = True

class TradingSignal(SQLModel, table=True):
    """A trading signal represents a suggestion to buy or sell. It is issued by a signal supplier (manually or algorithmically). It must have a correlating id to a trade."""
    id: Optional[int] = Field(default=None, primary_key=True)
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
    datetime_of_creation: Optional[str]
    """An ISO-UTC-compatible date and time of when the signal was created by the signal supplier."""
    datetime_of_registration: Optional[str]
    """The ISO-UTC-compatible date and time of when the signal was entering our interface."""
    position_size_of_investement: float = 100
    """Percentage of the investment position this algortihm is allowed to trade. Default is 100%, which is 1 position."""  
    
    __avro_type__ = {
        "type": "record",
        "name": "TradingSignal",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "algo_id", "type": "string"},
            {"name": "provider_id", "type": "string"},
            {"name": "market", "type": "string"},
            {"name": "exchange", "type": "string"},
            {"name": "trade_correlation_id", "type": "string"},
            {"name": "direction", "type": {"type": "enum", "name": "Direction", "symbols": ["long", "short"]}},
            {"name": "side", "type": {"type": "enum", "name": "Side", "symbols": ["buy", "sell"]}},
            {"name": "price", "type": "float"},
            {"name": "tp", "type": ["null", "float"]},
            {"name": "sl", "type": ["null", "float"]},
            {"name": "datetime_of_creation", "type": {"type": "long", "logicalType": "timestamp-millis"}},
            {"name": "datetime_of_registration", "type": {"type": "long", "logicalType": "timestamp-millis"}},
            {"name": "position_size_of_investement", "type": "float", "default": 100}
        ]
    }
