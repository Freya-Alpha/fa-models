from enum import Enum

class OrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"
