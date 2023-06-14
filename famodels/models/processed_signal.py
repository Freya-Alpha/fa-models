from typing import List, Optional
from famodels.models.trading_signal import TradingSignal
from famodels.models.state_of_signal import StateOfSignal
from redis_om import Field

class ProcessedSignal(TradingSignal):
    """As soon a trading signal is processed by the signal qualifier, it is declared as a Processed Signal.
        When instantiating, use the **kwargs to map the TradingSignal values to the attributes of the processed trading signal.
        e.g. ProcessedTradingSignal(status=StateOfSignal.ACCEPTED, process_info=[], **signal.__dict__)
        Caution: Attributes other than status and process_info needs to added to the signal first before initializing an object.
    """
    id: Optional[str]
    """This id will be added by Freya Alpha."""
    status: StateOfSignal = Field(index=True)
    process_info: List[str]

    class Meta:
        global_key_prefix="signal-processing"
        model_key_prefix="processed-signal"

    # class Config:
    #     orm_mode = True


        

    