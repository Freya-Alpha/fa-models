from datetime import datetime
from enum import Enum
import ipaddress
import uuid
from pydantic import BaseModel, ConfigDict, Field, field_validator

class BlockedIpReasonType(str, Enum):
    ATTEMPTING_MULTIPLE_LOGINS = "Attempting multiple logins"
    EXCESSIVE_FAILED_LOGIN_ATTEMPTS = "Excessive failed login attempts"
    IP_SPOOFING = "IP spoofing"
    MALWARE = "Malware"
    BLACKLISTED_IP_ADDRESS = "Blacklisted IP address"
    REPEATED_ERROR_RESPONSE_CODES = "Repeated error response codes"
    SUSPICIOUS_OPERATIONS = "Suspicious operations"
    INAPPROPRIATE_WEBSITE = "Inappropriate website"
    RULE_VIOLATION = "Rule violation"

class BlockedIp(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: str = Field(default=str(uuid.uuid4()))
    ip_address: ipaddress.IPv4Address = Field(..., strip_withspace=True)
    blocking_reason: BlockedIpReasonType = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('ip_address')
    def val_ip_address(cls, v: ipaddress.IPv4Address) -> ipaddress.IPv4Address:
        return str.strip(v.compressed)
