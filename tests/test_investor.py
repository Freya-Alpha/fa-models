import pytest
from famodels.models.investor import Investor
import hashlib
import os
import time

@pytest.fixture(scope="function", autouse=True)
def setup_redis():
    if 'CI' not in os.environ:
        os.system('docker run --name redis-unit-test -d -p 6379:6379 redis/redis-stack:latest')
        # give some time for the Redis server to start
        time.sleep(2)
    yield
    if 'CI' not in os.environ:
        os.system('docker stop redis-unit-test')
        os.system('docker rm redis-unit-test')

# @pytest.fixture(scope="function", autouse=True)
# def setup_redis():
#     os.system('docker run -d --name redis-unit-test -p 6379:6379 -p 8001:8001 redis/redis-stack:latest ')
#     # give some time for the Redis server to start
#     time.sleep(2)
#     yield
#     os.system('docker stop redis-unit-test')
#     os.system('docker rm redis-unit-test')

def test_investor_model():
    # Now we can create an instance of `Investor` without connecting to a real Redis server
    investor = Investor(investor_id='123', email='test@example.com')

    # # The `passphrase` property raises an exception, as expected
    # with pytest.raises(Exception):
    #     pass

