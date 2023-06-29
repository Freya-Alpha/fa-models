from datetime import datetime
import os
from typing import List, Optional
from redis_om import (Field, JsonModel, EmbeddedJsonModel)
from redis_om.connections import get_redis_connection

from famodels.models.subscription import Subscription

REDIS_OM_URL = os.environ.get("REDIS_OM_URL")
print(f"The env-var REDIS_OM_URL is: {REDIS_OM_URL}")

class Fund(EmbeddedJsonModel):
    fund_id:str = Field(index=True)
    name:str = Field(index=True)
    investor_id:str = Field(index=True)    
    subscriptions: Optional[List[Subscription]] = Field(index=False)  
    compounding: bool = Field(index=True)
    absolute_max_amount: float

    
    class Meta:
        global_key_prefix="fa-investor-processing"
        model_key_prefix="fund"
        database = get_redis_connection(url=REDIS_OM_URL, decode_responses=True)

    def add_subscription(self, subscription):
        if subscription not in self.list_of_subscriptions:
            self.list_of_subscriptions.append(subscription)