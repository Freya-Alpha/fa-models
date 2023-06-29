from datetime import datetime
import os
from typing import List
from pydantic import EmailStr
from redis_om import (Field, JsonModel)
from redis_om.connections import get_redis_connection

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Person(JsonModel):    
    given_name: str = Field(index=True)
    family_name: str = Field(index=True, full_text_search=True)
    email: EmailStr = Field(index=True)
    sex: int = Field(index=True)    
    nationality_iso3: str = Field(index=True)
    identification_type: str = Field(index=True)
    identification_refernce: str = Field(index=True)
    country_of_residence_iso3: str = Field(index=True)
    phone: str = Field(index=True)
    
    class Meta:
        global_key_prefix=""
        model_key_prefix="person"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)
