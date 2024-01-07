from enum import Enum

class StatusOfSignal(str, Enum):
    SUBMITTED = "submitted"
    ERRONEOUS = "erroneous"
    REJECTED = "rejected"
    QUALIFIED = "qualified"
    EXECUTED = "executed"
