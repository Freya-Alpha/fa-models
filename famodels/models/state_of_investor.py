from enum import Enum

class StateOfInvestor(str, Enum):    
    """Describing the possible states of an Inde. Keep it simple. Also, we added the str to inherit from, so that the ENUM is serializable.         """
    REGISTERED = "registered"
    """When an investor is merely registered, but NOT authenticated with an official document. Registered allows cold trading."""
    QUALIFIED = "qualified"
    """When an investor is identified and authenticated by an offical document and qualified for hot trades. This is the highest state."""
    BANNED = "banned"
    """The user was deliberatly banned from the system."""
