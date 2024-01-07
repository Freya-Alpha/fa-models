from ast import List
from pydantic import ValidationError
import pytest
from famodels.investor import Fund, Investor
from famodels.person import Person

@pytest.mark.parametrize("given_name, family_name, email, gender, nationality_iso2, country_of_residence_iso2, phone, investor_id, investor_name, investor_email", [
    ("John", "Doe", "john@doe.com", "m", "UK", "US", "+44 123456789", "123", "Jonathans Investments Ltd", "contact@jonathans.com"),
    ("Jane", "Smith", "jane@smith.com", "f", "US", "UK", "+1 987654321", "456", "Jane's Ventures", "info@janesventures.com"),
])
def test_investor_model(given_name, family_name, email, gender, nationality_iso2, country_of_residence_iso2, phone, investor_id, investor_name, investor_email):
    """Test if we can create an Investor model with various parameters."""
    person = Person(
        given_name=given_name,
        family_name=family_name,
        email=email,
        gender=gender,
        nationality_iso2=nationality_iso2,
        country_of_residence_iso2=country_of_residence_iso2,
        phone=phone
    )
    investor = Investor(
        id=investor_id,
        name=investor_name,
        email=investor_email,
        accountable=person
    )
    assert investor.id == investor_id
    assert investor.name == investor_name
    assert investor.email == investor_email
    assert investor.accountable == person
    assert investor.accountable.gender == gender

@pytest.mark.parametrize(
    "email, nationality_iso2, country_of_residence_iso2",
    [
        ("invalidemail", "UK", "IRE"),  # invalid email
        ("john@doe.com", "GB", "IRE"),  # invalid nationality_iso2
        ("john@doe.com", "UKI", "IR"),  # invalid country_of_residence_iso2
        ("john@doe.com", "UKRA", "IRE"),  # invalid nationality_iso2
        ("john@doe.com", "UK", "IRELA"),  # invalid country_of_residence_iso2
    ],
)
def test_negative_person(email, nationality_iso2, country_of_residence_iso2):
    with pytest.raises(ValidationError):
        Person(
            given_name="john",
            family_name="Doe",
            email=email,
            gender="f",
            nationality_iso2=nationality_iso2,
            country_of_residence_iso2=country_of_residence_iso2,
            phone="+43 681 11 24",
        )

@pytest.mark.parametrize(
    "email, nationality_iso2, country_of_residence_iso2",
    [
        ("john.doe+test@domain.com", "UK", "IR"),  # valid email with plus addressing and country codes
        ("jane-doe@sub.domain.com", "US", "CA"),  # valid email with hyphen and subdomain
        ("bob_smith@edu.domain.ac.uk", "AU", "NZ"),  # valid email with underscore and multiple domain levels
        ("alice.johnson@long-domain-name.com", "IN", "UK"),  # valid email with long domain name
        ("charles-brown@domain.io", "BR", "AR"),  # valid email with country code top-level domain (ccTLD)
    ],
)
def test_positive_person(email, nationality_iso2, country_of_residence_iso2):
    try:
        Person(
            given_name="john",
            family_name="Doe",
            email=email,
            gender="f",
            nationality_iso2=nationality_iso2,
            country_of_residence_iso2=country_of_residence_iso2,
            phone="+43 681 11 24",
        )
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")


# @pytest.mark.parametrize(
#     "exchange, key_id, key_secret",
#     [
#         ("Binance", "key1", "secret1"),
#         ("Kucoin", "key2", "secret2")
#     ]
# )
# def test_exchange_key(exchange, key_id, key_secret):
#     # Instantiate an EncryptionService
#     encryption_service = EncryptionService('MySecretEncryptionKey1234567890')

#     # Instantiate an ExchangeKey object with placeholder values
#     exchange_key = ExchangeKey(exchange=exchange, key_id=key_id, _key_secret="")

#     # Set key_secret, which will trigger encryption
#     exchange_key.set_key_secret(key_secret, encryption_service)

#     # Assert the attributes of the ExchangeKey
#     assert exchange_key.exchange == exchange
#     assert exchange_key.key_id == key_id
#     assert exchange_key.get_key_secret(encryption_service) == key_secret

@pytest.mark.parametrize(
    "investor_id, name, email, funds",
    [
        ("1", "Superion Corp.", "investor1@example.com", [{"id": "f1", "name": "fund1", "investor_id": "1", "subscriptions": [{"id": "s1", "algo_id": "a1"}], "compounding": 1, "absolute_max_amount": 1000.0}, {"id": "f2", "name": "fund2", "investor_id": "1", "subscriptions": [{"id": "s2", "algo_id": "a2"}, {"id": "s3", "algo_id": "a3"}], "compounding": "false", "absolute_max_amount": 500.0}]),
        ("2", "Super Investment Ltd", "investor2@example.com", [{"id": "f3", "name": "fund3", "investor_id": "2", "subscriptions": [{"id": "s4", "algo_id": "a4"}, {"id": "s5", "algo_id": "a5"}, {"id": "s6", "algo_id": "a6"}], "compounding": 1}]),
        ("3", "XY Funds", "investor3@example.com", [{"id": "f4", "name": "fund4", "investor_id": "3", "subscriptions": [{"id": "s7", "algo_id": "a7"}], "compounding": 0, "absolute_max_amount": 10000.0}, {"id": "f5", "name": "fund5", "investor_id": "3", "subscriptions": [{"id": "s8", "algo_id": "a8"}, {"id": "s9", "algo_id": "a9"}, {"id": "s10", "algo_id": "a10"}]}])
    ]
)
def test_investor_funds(investor_id, name, email, funds):
    person = Person(given_name="john", family_name="Doe", email=email, gender="f", nationality_iso2="UK", country_of_residence_iso2="IR", phone="+43 681 11 24")

    funds_objects: List[Fund] = []
    for fund in funds:
        # subscriptions = [Subscription(**subscription) for subscription in fund.pop('subscriptions')]
        fund_obj: Fund = Fund(**fund)
        funds_objects.append(fund_obj)

    investor = Investor(id=investor_id, name=name, email=email, accountable=person, funds=funds_objects)

    assert investor.id == investor_id
    assert investor.name == name
    assert investor.email == email
    assert len(investor.funds) == len(funds_objects)
    for i in range(len(funds_objects)):
        assert investor.funds[i].id == funds_objects[i].id
        assert investor.funds[i].name == funds_objects[i].name
        assert investor.funds[i].compounding == funds_objects[i].compounding
        # assert len(investor.funds[i].subscriptions) == len(funds_objects[i].subscriptions)


def test_passphrase():
    # Create an Investor instance
    person = Person(given_name="john", family_name="Doe", email="john@doe.com", gender="f", nationality_iso2="UK", country_of_residence_iso2="IR", phone="+43 681 11 24")
    investor = Investor(id='123', name="Johnny's Investments", email='test@example.com', accountable=person)
    investor.set_passphrase("testpass")
    # Check that passphrase can't be retrieved directly
    with pytest.raises(Exception) as e:
        print(f"INVOKING IS FORBIDDEN --> {investor.passphrase}")
    assert str(e.value) == "Cannot retrieve passphrase."

    # Check the passphrase
    assert investor.verify_passphrase("testpass") is True

    # Check with an incorrect passphrase
    assert investor.verify_passphrase("wrongpass") is False
