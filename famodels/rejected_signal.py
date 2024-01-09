from enum import Enum
from pydantic import Field
from datetime import datetime
from famodels.raw_signal import RawSignal

class ReasonForRejection(str, Enum):
    SCAM = "scam"
    BANNED_SUPPLIER = "banned_supplier"
    BANNED_STRATEGY = "banned_strategy"
    BANNED_IP = "banned_ip"
    DOS_ATTACK = "dos_attack" # any flood attack: slowloris, ping-of-death, query attack, etc.
    INVALID_DATA = "invalid_data"
    INVALID_PRICE = "invalid_price"
    INCLOMPLETE = "incomplete" # any kind of missing data

class RejectedSignal(RawSignal):
    """
    Rejected Signals are processed Raw Signals, wich are rejected for some reason.
    This signal wraps the RawSignal, which is derived from the TradingSignal.
    And adds new values to it.
    """
    date_of_rejection: datetime = Field(default_factory=datetime.now, description="The datetime when the signal was rejected.")
    reason_for_rejection: ReasonForRejection

    @classmethod
    def from_raw_signal(cls, raw_signal: RawSignal, reason_for_rejection: ReasonForRejection):
        # Ensure the reason for rejection is provided
        rejected_signal = cls(**raw_signal.model_dump(), reason_for_rejection=reason_for_rejection)
        return rejected_signal
