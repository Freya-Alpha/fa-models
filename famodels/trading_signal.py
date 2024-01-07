from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from famodels.direction import Direction
from famodels.side import Side

class TradingSignal(BaseModel):
    """
    A trading signal represents a suggestion to buy or sell. It is issued by a signal supplier 
    (manually or algorithmically). It must have a correlating id to a trade.
    """
    provider_id: str = Field(..., description="The ID of the provider, who emitted the signal.")
    strategy_id: str = Field(..., description="Provide the id of the strategy (you might have more than one algorithm), which is sending a signal.")
    provider_signal_id: Optional[str] = Field(None, description="You can use this correlation id as your own 'signal id' of your internal system. #Do not mistaken this correlation id with the trade correlation id.")
    provider_trade_id: str = Field(..., description="FA Models describes a Trade as a buy and a sell (not soley a buy or a sell). Every trade is expected to consist of at least one buy order and at least one sell order. Thus, the provider_trade_id is mandatory if a provider wants to scale in and out on a fund-position. This will create a multi-position-trade. E.g. one can send one long signal with a provider_trade_id 77 and another long signal a few hours later also with the provider_trade_id 77. Provided that the position_size_in_percentage is less than 100 on the first one. All updates provided by the system will hold the trade id.")
    is_hot_signal: bool = Field(default=True, description="By default, every signal is marked as a cold signal. Thus, set to 0. That is a paper-trading signal and will only be processed for forward-performance testing. Hot signals are suggested to be processed by the order engines - provided all other requirements for hot trading are fulfilled. Set 1 (not true) to this value to suggest a hot trade.")
    market: str = Field(..., description="The market you want to trade. e.g. BTC/USDT")
    exchange: str = Field(..., description="The exchange you pulled your data from - or - wish to trade on.")
    direction: Direction = Field(..., description="Simply LONG or SHORT.")
    side: Side = Field(..., description="Simply BUY (open trade) or SELL (close trade).")
    price: float = Field(..., description="The price to buy use for the limit-order or limit-stop-order")
    tp: float = Field(..., description="Take-profit in absolute price.")
    sl: float = Field(..., description="Stop-loss in absolute price.")
    position_size_in_percentage: float = Field(default=100, description="Caution, if one chooses another value than 100, the system will create a multi-position-trade (for scaling-in and scaling-out on a trade). In addition, one has to provide a provider_trade_id in order for the system to create a multi-position-trade. Any consecutive trades (scale-in/out), need to have provide the same provider_trade_id. Percentage of the trade position this algortihm is allowed to trade. Default is 100%, which is 1 position of your fund's positions. Another number than 100, will assume this trade has multiple positions. If a signal provider has one partial position open and then closes it, it will also regard the trade as fully closed.")
    timestamp_of_creation: datetime = Field(default_factory=datetime.now, description="The datetime when the signal was created by the signal supplier.")
    timestamp_of_registration: Optional[datetime] = Field(None, description="The datetime when the signal was entering our interface. This will be overridden.")
