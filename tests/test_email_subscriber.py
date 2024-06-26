import pytest
from famodels.email_subscriber import EmailSubscriberIn, EmailSubscriberInDb, EmailSubscriptionAction


@pytest.mark.parametrize("email, ip_address", [
    ("test@test.com", "127.0.0.1"),
    ("john.doe@swiss.com", "192.168.169.69"),
    ("alias001@microsoft.com", "192.168.169.226"),
    ("alias001@ubuntu.com", "100.128.0.0")
])
def test_email_subscriber_model(email: str, ip_address: str):
    """Test if we can create a subscriber model with various parameters."""
    subscriber = EmailSubscriberIn(
        email=email,
        ip_address=ip_address,
        subscription_action=EmailSubscriptionAction.SUBSCRIBE)

    assert subscriber.email == email
    assert subscriber.ip_address == ip_address


@pytest.mark.parametrize("email, ip_address", [
    ("    name@domain.com    ", "100.128.0.0"),
])
def test_email_subscriber_model_with_whitespace_email(email: str, ip_address: str):
    """Test if we can create a subscriber model with various parameters."""
    subscriber = EmailSubscriberIn(
        email=email,
        ip_address=ip_address,
        subscription_action=EmailSubscriptionAction.SUBSCRIBE)

    assert subscriber.email == email.strip()
    assert subscriber.ip_address == ip_address


@pytest.mark.parametrize("email, ip_address", [
    (None, "127.0.0.1"),
    ("test@test.com", None),
    (None, None),
    ("test@test.com", "127 .0.0.1"),
    ("john.doe@swiss.com", "999.255.255.255"),
    ("@microsoft.com", "192.168.169.226"),
    ("alias001@ubuntu", "100.128.0.0/222")])
def test_email_subscriber_model_for_validation_errors(email: str, ip_address: str):
    with pytest.raises(Exception):
        EmailSubscriberIn(
            email=email,
            ip_address=ip_address,
            subscription_action=EmailSubscriptionAction.SUBSCRIBE)


@pytest.mark.parametrize("email, ip_address, ip_address_lat, ip_address_lon", [
    ("info@swiss.ch", "100.128.0.0", "30.2", "70.93838"),
    ("info@freya-alpha.com", "166.128.0.0", "89.2", "179.93838")])
def test_email_subscriber_db_model(email: str, ip_address: str, ip_address_lat: str, ip_address_lon: str):
    subscriber_in_db = EmailSubscriberInDb(
        email_encrypted=email,
        subscription_action=EmailSubscriptionAction.SUBSCRIBE,
        ip_address=ip_address,
        ip_address_location_lat=ip_address_lat,
        ip_address_location_lon=ip_address_lon)

    assert subscriber_in_db.email_encrypted == email
    assert subscriber_in_db.ip_address == ip_address
    assert subscriber_in_db.ip_address_location_lat == ip_address_lat
    assert subscriber_in_db.ip_address_location_lon == ip_address_lon


@pytest.mark.parametrize("ip_address, ip_address_lat, ip_address_lon", [
    (None, "30.2", "70.93838"),
    ("100.128.0.0", "120", "60"),
    ("100.128.0.0", "89", "181")])
def test_email_subscriber_db_model_for_validation_errors(ip_address: str, ip_address_lat: str, ip_address_lon: str):
    with pytest.raises(Exception):
        EmailSubscriberInDb(
            ip_address=ip_address,
            subscription_action=EmailSubscriptionAction.SUBSCRIBE,
            ip_address_location_lat=ip_address_lat,
            ip_address_location_lon=ip_address_lon)


@pytest.mark.parametrize("email, ip_address", [
    ("info@swiss.ch", "100.128.0.0"),
    ("info@freya-alpha.com", "166.128.0.0")])
def test_email_subscriber_db_model_with_null_values(email: str, ip_address: str):
    subscriber_in_db = EmailSubscriberInDb(
        email_encrypted=email,
        subscription_action=EmailSubscriptionAction.SUBSCRIBE,
        ip_address=ip_address)

    assert subscriber_in_db.email_encrypted == email
    assert subscriber_in_db.ip_address == ip_address
    assert subscriber_in_db.ip_address_location_lat is None
    assert subscriber_in_db.ip_address_location_lon is None


def test_email_subscriber_db_model_default_id():
    subscriber_in_db = EmailSubscriberInDb(
        email_encrypted="test@test.com",
        subscription_action=EmailSubscriptionAction.SUBSCRIBE,
        ip_address="198.252.0.0")

    assert subscriber_in_db.id is not None
