from enum import Enum

class StateOfTrade(str, Enum):    
    """Describing the possible states of a Trade. Keep it simple. Also, we added the str to inherit from, so that the ENUM is serializable.         """
    NEW = "new"
    BUYING = "buying"    
    """BUYING means that we have at least submitted an order to buy."""
    WAITING_FOR_SELL_DECISION = "waiting_for_sell_decision"
    """Indicates, the the buy has been completed and we are waiting for a sell order to be sent."""
    SELLING = "selling"
    """SELLING means that a sell-order (close position) has been sent to the CEX. """
    CANCELED = "canceled"
    """Cancelled is the state where a trade was canceled but cleaned up (i.e. sold what was previously bought. Or bought-back what was previously sold)."""
    CLOSED = "closed"
    """Closed means the trade did buy completely and sold completely."""