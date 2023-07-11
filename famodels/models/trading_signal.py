import os
from enum import Enum
from typing import Optional
from uuid import UUID
from famodels.models.direction import Direction
from famodels.models.side import Side
from redis_om import Migrator
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection
from enum import Enum

class StateOfSignal(str, Enum):    
    """Describing the possible states of a Signal (not a Trade). """
    SUBMITTED = "submitted"
    ERRONEOUS = "erroneous"   
    REJECTED = "rejected"
    QUALIFIED = "qualified"
    EXECUTED = "executed"

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class TradingSignal(JsonModel):
    """A trading signal represents a suggestion to buy or sell. It is issued by a signal supplier (manually or algorithmically). It must have a correlating id to a trade."""    
    provider_id: str = Field(index=True)
    """The ID of the provider, who emitted the signal."""
    algo_id: str = Field(index=True)
    """Provide the id of your algorithm id (you might have more than one algorithm), which is sending a signal. """
    provider_signal_id: Optional[str]
    """You can use this correlation id as your own 'signal id' of your internal system. 
    #Do not mistaken this correlation id with the trade correlation id."""    
    provider_trade_id: str = Field(index=True)
    """FA Models describes a Trade as a buy and a sell (not soley a buy or a sell). 
    # Every trade is expected to consist of at least one buy order and zero or more sell orders. 
    # Thus, the trade_correlation_id is mandatory. Use this correlation id to link your signals to a trade. All updates provided by the system will hold the trade id."""    
    is_hot_signal: int = Field(default=0, index=True)
    """By default, every signal is marked as a cold signal. Thus, set to 0. That is a paper-trading signal and will only be processed for forward-performance testing. 
    Hot signals are suggested to be processed by the order engines - provided all other requirements for hot trading are fulfilled.
    Set 1 (not true) to this value to suggest a hot trade."""    
    market: str = Field(index=True)
    """The market you want to trade. e.g. BTC/USDT"""
    exchange: str = Field(index=True)
    """The exchange you pulled your data from - or - wish to trade on."""
    direction: Direction = Field(index=True)
    """Simply LONG or SHORT."""
    side: Side = Field(index=True)
    """Simply BUY (open trade) or SELL (close trade)."""
    price: float
    """The price to buy use for the limit-order or limit-stop-order"""
    tp: float
    """Take-profit in absolute price."""
    sl: float
    """Stop-loss in absolute price."""
    position_size_in_percentage: float = 100
    """Percentage of the trade position this algortihm is allowed to trade. 
    Default is 100%, which is 1 position of your fund's positions.
    Another number than 100, will assume this provider-trade has multiple positions. 
    If a signal provider has one partial position open and then closes it, it will also regard the trade as fully closed."""  
    # datatime.datetime would be fully serializable in REDIS. 
    # https://www.youtube.com/watch?v=ZP2j7bmWfmU
    timestamp_of_creation: int = Field(index=True)
    """The timestamp in milliseconds when the signal was created by the signal supplier."""
    timestamp_of_registration: Optional[int]
    """The timestamp in milliseconds when the signal was entering our interface. This will be overridden."""    

    class Meta:
        # global_key_prefix="signal-processing"
        model_key_prefix="raw-signal"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

# Migrator().run()