from pydantic import Field
from typing import Optional
from datetime import datetime
from famodels.raw_signal import RawSignal

class QualifiedSignal(RawSignal):
    """
    This signal wraps the RawSignal, which is derived from the TradingSignal.
    And adds new values to it.
    """
    date_of_qualification: Optional[datetime] = Field(default_factory=datetime.now, description="The UTC datetime when the signal was qualified.")
    qualification_comments: str = None

    @classmethod
    def from_raw_signal(cls, raw_signal: RawSignal):
        # Create a new RawSignal instance, copying all attributes from TradingSignal
        qualified_signal = cls(**raw_signal.model_dump())
        return qualified_signal
