from datetime import datetime
from famodels.state_of_trade import StateOfTrade
from famodels.direction import Direction
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid

class BaseTradeSQLModel(SQLModel):
    def __init__(self, **kwargs):
        self.__config__.table = False
        super().__init__(**kwargs)
        self.__config__.table = True

    class Config:
        validate_assignment = True

class Trade(BaseTradeSQLModel, table=True):
    """A trade in our system is composed of a buy and a sell order. Do not mistaken it for a trade from the CEX.
        Create a new Trade record for every update and correlate them with trade_id. See attribute #trade_id"""   

    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)    
    trade_id: Optional[str] = Field(default=str(uuid.uuid4()), nullable=False)
    # sort_index:int = field(init=False, repr=False)
    #trade_id: Optional[str] = Field(default=uuid.uuid4(), primary_key=True)
    """The trade id is the reference that keeps the state updates correlated. It will generate a UUID by default.
        Use this for the first record you insert. Inserting updated records (new records should then have the trade_id
        provided to create the correlation.)"""
    pos_idx:int
    market:str
    status:StateOfTrade
    direction:Direction
    time_of_initiation:datetime
    """When we decided to start this trade."""
    buy_order_id:str
    sell_order_id:Optional[str] = None
    take_profit:Optional[int] = None
    stop_loss:Optional[int] = None
    """This is usually the receiving timestamp."""        
    profit_and_loss_percentage: Optional[float] = None
    profit_and_loss_amount: Optional[float] = None

    def __getitem__(self, key):
        return self.__dict__[key]    