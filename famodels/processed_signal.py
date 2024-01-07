from typing import List, Optional
from trading_signal import TradingSignal
from status_of_signal import StatusOfSignal
from pydantic import Field

class ProcessedSignal(TradingSignal):
    """
    As soon as a trading signal is processed by the signal qualifier, it is declared as a Processed Signal.
    When instantiating, use the **kwargs to map the TradingSignal values to the attributes of the processed trading signal.
    e.g. ProcessedTradingSignal(status=StateOfSignal.ACCEPTED, process_info=[], **signal.__dict__)
    Caution: Attributes other than status and process_info need to be added to the signal first before initializing an object.
    """
    id: Optional[str] = Field(description="This id will be added by Freya Alpha.")
    status: StatusOfSignal = Field(...)
    process_info: List[str] = Field(default_factory=list)
