import pytest
import hashlib
import os
import time
import redis

@pytest.fixture(scope="function", autouse=True)
def setup_redis():
    if 'CI' not in os.environ:
        os.system('docker run --name redis-unit-test -d -p 6379:6379 redis/redis-stack-server:latest')
        # give some time for the Redis server to start
        time.sleep(2)        
        
    yield
    if 'CI' not in os.environ:
        os.system('docker stop redis-unit-test')
        os.system('docker rm redis-unit-test')


def test_investor_model():
    # Now we can create an instance of `Investor` without connecting to a real Redis server
    from famodels.models.investor import Investor
    investor = Investor(investor_id='123', email='test@example.com')
    print(investor.email)

