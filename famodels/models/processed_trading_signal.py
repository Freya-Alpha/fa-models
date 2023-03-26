from ast import List
from famodels.models.trading_signal import TradingSignal
from famodels.models.state_of_signal import StateOfSignal

class ProcessedTradingSignal(TradingSignal):
    """As soon a Signal is process by the signal qualifier, it is declared as a Processed Signal."""

    def __init__(self, signal: TradingSignal, status: StateOfSignal = None, process_info: List[str] = None):
        super().__init__(
            id=signal.id,
            supplier_correlation_id=signal.supplier_correlation_id,
            trade_correlation_id=signal.trade_correlation_id,
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
        self.status: StateOfSignal = status
        self.process_info: List[str] = process_info
        

    