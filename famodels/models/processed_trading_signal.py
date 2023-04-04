from typing import List
from famodels.models.trading_signal import TradingSignal
from famodels.models.state_of_signal import StateOfSignal

class ProcessedTradingSignal(TradingSignal):
    """As soon a trading signal is processed by the signal qualifier, it is declared as a Processed Signal.
        When instantiating, use the **kwargs to map the TradingSignal values to the attributes of the processed trading signal.
        e.g. ProcessedTradingSignal(status=StateOfSignal.ACCEPTED, process_info=[], **signal.__dict__)
    """
    status: StateOfSignal
    process_info: List[str]

    class Config:
        orm_mode = True


        

    