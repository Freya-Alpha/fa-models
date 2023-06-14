from enum import Enum

class StateOfSignal(str, Enum):    
    """Describing the possible states of a Signal (not a Trade). """
    SUBMITTED = "submitted"
    ERRONEOUS = "erroneous"   
    REJECTED = "rejected"
    QUALIFIED = "qualified"
    EXECUTED = "executed"