import os
from pydantic import ValidationError
import pytest
import hashlib
import time
import redis
os.environ["REDIS_OM_URL"] = "redis://localhost:6379"
os.environ["ENCRYPTION_KEY"] = 'MySecretEncryptionKey1234567890'
from famodels.models.investor import EncryptionService, Fund, Investor, ExchangeKey, Subscription
from famodels.models.person import Person


@pytest.fixture(scope="session", autouse=True)
def setup_redis():
    if 'CI' not in os.environ:
        os.system('docker run --name redis-unit-test -d -p 6379:6379 redis/redis-stack-server:latest')
        os.environ["REDIS_OM_URL"] = "redis://localhost:6379"
        # give some time for the Redis server to start
        time.sleep(2)        
        
    yield

    if 'CI' not in os.environ:
        os.system('docker stop redis-unit-test')
        os.system('docker rm redis-unit-test')


def test_investor_model():
    # Now we can create an instance of `Investor` without connecting to a real Redis server
    person = Person(given_name="john", family_name="Doe", email="john@doe.com", sex=0, nationality_iso3="GBR", country_of_residence_iso3="IRE", phone="+43 681 11 24")
    investor = Investor(investor_id='123', email='test@example.com', accountable=person)    


@pytest.mark.parametrize(
    "email, nationality_iso3, country_of_residence_iso3",
    [
        ("invalidemail", "GBR", "IRE"),  # invalid email
        ("john@doe.com", "GB", "IRE"),  # invalid nationality_iso3
        ("john@doe.com", "GBR", "IR"),  # invalid country_of_residence_iso3
        ("john@doe.com", "GBRRA", "IRE"),  # invalid nationality_iso3
        ("john@doe.com", "GBR", "IRELA"),  # invalid country_of_residence_iso3
    ],
)
def test_negative_person(email, nationality_iso3, country_of_residence_iso3):
    with pytest.raises(ValidationError):
        Person(
            given_name="john",
            family_name="Doe",
            email=email,
            sex=0,
            nationality_iso3=nationality_iso3,
            country_of_residence_iso3=country_of_residence_iso3,
            phone="+43 681 11 24",
        )

@pytest.mark.parametrize(
    "email, nationality_iso3, country_of_residence_iso3",
    [
        ("john.doe+test@domain.com", "GBR", "IRE"),  # valid email with plus addressing and country codes
        ("jane-doe@sub.domain.com", "USA", "CAN"),  # valid email with hyphen and subdomain
        ("bob_smith@edu.domain.ac.uk", "AUS", "NZL"),  # valid email with underscore and multiple domain levels
        ("alice.johnson@long-domain-name.com", "IND", "GBR"),  # valid email with long domain name
        ("charles-brown@domain.io", "BRA", "ARG"),  # valid email with country code top-level domain (ccTLD)
    ],
)
def test_positive_person(email, nationality_iso3, country_of_residence_iso3):
    try:
        Person(
            given_name="john",
            family_name="Doe",
            email=email,
            sex=0,
            nationality_iso3=nationality_iso3,
            country_of_residence_iso3=country_of_residence_iso3,
            phone="+43 681 11 24",
        )
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")


@pytest.mark.parametrize(
    "exchange, key_id, key_secret",
    [
        ("Binance", "key1", "secret1"),
        ("Kucoin", "key2", "secret2")
    ]
)
def test_exchange_key(exchange, key_id, key_secret):
    # Instantiate an EncryptionService
    encryption_service = EncryptionService('MySecretEncryptionKey1234567890')

    # Instantiate an ExchangeKey object with placeholder values
    exchange_key = ExchangeKey(exchange=exchange, key_id=key_id, _key_secret="")
    
    # Set key_secret, which will trigger encryption
    exchange_key.set_key_secret(key_secret, encryption_service)

    # Assert the attributes of the ExchangeKey
    assert exchange_key.exchange == exchange
    assert exchange_key.key_id == key_id
    assert exchange_key.get_key_secret(encryption_service) == key_secret

@pytest.mark.parametrize(
    "investor_id, email, funds",
    [
        ("1", "investor1@example.com", [{"fund_id": "f1", "name": "fund1", "investor_id": "1", "subscriptions": [{"subscription_id": "s1", "algo_id": "a1"}], "compounding": 1, "absolute_max_amount": 1000.0}, {"fund_id": "f2", "name": "fund2", "investor_id": "1", "subscriptions": [{"subscription_id": "s2", "algo_id": "a2"}, {"subscription_id": "s3", "algo_id": "a3"}], "compounding": "false", "absolute_max_amount": 500.0}]),
        ("2", "investor2@example.com", [{"fund_id": "f3", "name": "fund3", "investor_id": "2", "subscriptions": [{"subscription_id": "s4", "algo_id": "a4"}, {"subscription_id": "s5", "algo_id": "a5"}, {"subscription_id": "s6", "algo_id": "a6"}], "compounding": 1}]),
        ("3", "investor3@example.com", [{"fund_id": "f4", "name": "fund4", "investor_id": "3", "subscriptions": [{"subscription_id": "s7", "algo_id": "a7"}], "compounding": 0, "absolute_max_amount": 10000.0}, {"fund_id": "f5", "name": "fund5", "investor_id": "3", "subscriptions": [{"subscription_id": "s8", "algo_id": "a8"}, {"subscription_id": "s9", "algo_id": "a9"}, {"subscription_id": "s10", "algo_id": "a10"}]}])
    ]
)
def test_investor_funds(investor_id, email, funds):
    person = Person(given_name="john", family_name="Doe", email=email, sex=0, nationality_iso3="GBR", country_of_residence_iso3="IRE", phone="+43 681 11 24")

    funds_objects = []
    for fund in funds:
        subscriptions = [Subscription(**subscription) for subscription in fund.pop('subscriptions')]
        fund_obj = Fund(subscriptions=subscriptions, **fund)
        funds_objects.append(fund_obj)

    investor = Investor(investor_id=investor_id, email=email, accountable=person, funds=funds_objects)

    assert investor.investor_id == investor_id
    assert investor.email == email
    assert len(investor.funds) == len(funds_objects)
    for i in range(len(funds_objects)):
        assert investor.funds[i].fund_id == funds_objects[i].fund_id
        assert investor.funds[i].name == funds_objects[i].name
        assert investor.funds[i].compounding == funds_objects[i].compounding
        assert len(investor.funds[i].subscriptions) == len(funds_objects[i].subscriptions)


def test_passphrase():
    # Create an Investor instance
    person = Person(given_name="john", family_name="Doe", email="john@doe.com", sex=0, nationality_iso3="GBR", country_of_residence_iso3="IRE", phone="+43 681 11 24")
    investor = Investor(investor_id='123', email='test@example.com', accountable=person)
    investor.setPassphrase("testpass")
    # Check that passphrase can't be retrieved directly
    with pytest.raises(Exception) as e:
        print(f"INVOKING IS FORBIDDEN --> {investor.passphrase}")
    assert str(e.value) == "Cannot retrieve passphrase."

    # Check the passphrase
    assert investor.verify_passphrase("testpass") is True

    # Check with an incorrect passphrase
    assert investor.verify_passphrase("wrongpass") is False
