import time
from pydantic import Field
from typing import Optional
from uuid import uuid4
from fasignalprovider.trading_signal import TradingSignal

class RawSignal(TradingSignal):
    """
    This internal signal wraps the TradingSignal sent by the supplier into a RawSignal. 
    And adds new values to it, e.g., ID or registration time.
    """
    id: str = Field(default_factory=lambda: str(uuid4()), description="The ID of this raw signal created upon initiation.")
    date_of_registration: Optional[int] = Field(default_factory=lambda: int(time.time() * 1000), description="The POSIX UTC timestamp (int) in nanoseconds when the signal was entering our interface.")

    @classmethod
    def from_trading_signal(cls, trading_signal: TradingSignal):
        # Create a new internal (Raw)Signal instance, copying all attributes from TradingSignal
        raw_signal = cls(**trading_signal.model_dump())
        return raw_signal
