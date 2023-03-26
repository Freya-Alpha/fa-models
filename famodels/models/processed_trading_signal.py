from ast import List
from famodels.models.trading_signal import TradingSignal
from famodels.models.state_of_signal import StateOfSignal

class ProcessedTradingSignal(TradingSignal):
    """As soon a Signal is processed by the signal qualifier, it is declared as a Processed Signal."""

    def __init__(self, signal: TradingSignal, status: StateOfSignal, process_info: List = None):
        self.status: StateOfSignal = status
        super().__init__(
            id=signal.id,
            supplier_correlation_id=signal.provider_signal_id,
            trade_correlation_id=signal.provider_trade_id,
            is_hot_signal=signal.is_hot_signal,
            algo_id=signal.algo_id,
            provider_id=signal.provider_id,
            market=signal.market,
            exchange=signal.exchange,
            direction=signal.direction,
            side=signal.side,
            price=signal.price,
            tp=signal.tp,
            sl=signal.sl,
            timestamp_of_creation=signal.timestamp_of_creation,
            timestamp_of_registration=signal.timestamp_of_registration,
            position_size_of_investment=signal.position_size_of_investment
        )        
        self.process_info: List[str] = process_info
        

    