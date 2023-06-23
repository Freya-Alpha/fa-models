from datetime import datetime
import os
from famodels.models.state_of_trade import StateOfTrade
from famodels.models.direction import Direction
from typing import Optional
import uuid
from redis_om import Migrator
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"the env-var REDIS_OM_URL is: {REDIS_OM_URL}")


class Trade(JsonModel):
    """A trade in our system is composed of a buy and a sell order. Do not mistaken it for a trade from the CEX.
        Create a new Trade record for every update and correlate them with trade_id. See attribute #trade_id"""   
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

    class Meta:
        global_key_prefix="order-and-trade-processing"
        model_key_prefix="trade"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def __getitem__(self, key):
        return self.__dict__[key]    
    
# Migrator().run()