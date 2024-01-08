from enum import Enum

class StatusOfSignal(str, Enum):
    """Reports the Status to Signal suppliers."""
    SUBMITTED = "submitted"
    REJECTED = "rejected"
    QUALIFIED = "qualified"
