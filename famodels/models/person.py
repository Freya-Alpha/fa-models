from datetime import datetime
import os
from typing import List, Optional
from pydantic import EmailStr
from redis_om import (Field, JsonModel, EmbeddedJsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Person(EmbeddedJsonModel):    
    given_name: str = Field(index=True)
    family_name: str = Field(index=True, full_text_search=True)
    email: EmailStr = Field(index=True)
    gender: str = Field(index=True, max_length=1)    
    """m or f"""
    nationality_iso3: str = Field(index=True, max_length=3, min_length=3)
    identification_type: Optional[str]
    identification_reference: Optional[str]
    country_of_residence_iso3: str = Field(index=True, max_length=3, min_length=3)
    phone: str = Field(index=True)
    
    class Meta:
        # global_key_prefix=""
        model_key_prefix="person"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
