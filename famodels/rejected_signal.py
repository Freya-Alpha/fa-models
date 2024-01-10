from enum import Enum
from pydantic import Field
from datetime import datetime
from famodels.raw_signal import RawSignal

class ReasonForRejection(str, Enum):
    SCAM = "scam"
    DOS_ATTACK = "dos_attack" # any flood attack: slowloris, ping-of-death, query attack, etc.
    BANNED_SUPPLIER = "banned_supplier"
    BANNED_STRATEGY = "banned_strategy"
    PROVIDER_NOT_ELIGABLE_FOR_HOT_SIGNAL = "provider_not_eligable_for_hot_signal"
    STRATEGY_NOT_QUALIFIED = "strategy_not_qualified"
    DISQUALIFIED_STRATEGY = "disqualified_strategy" # Used to be qualified
    BANNED_IP = "banned_ip"
    MARKET_NOT_ALLOWED = "market_not_allowed"
    INVALID_DATA = "invalid_data"
    INVALID_PRICE = "invalid_price"
    INCLOMPLETE = "incomplete" # any kind of missing data
    SYSTEM_IS_COLD = "system_is_cold" # The system is cold.
    

class RejectedSignal(RawSignal):
    """
    Rejected Signals are processed Raw Signals, wich are rejected for some reason.
    This signal wraps the RawSignal, which is derived from the TradingSignal.
    And adds new values to it.
    """
    date_of_rejection: datetime = Field(default_factory=datetime.now, description="The UTC datetime when the signal was rejected.")
    reasons_for_rejection: set[ReasonForRejection] = set()

    @classmethod
    def from_raw_signal(cls, raw_signal: RawSignal, reasons_for_rejection: ReasonForRejection):
        # Ensure the reason for rejection is provided
        rejected_signal = cls(**raw_signal.model_dump(), reasons_for_rejection=reasons_for_rejection)
        return rejected_signal
