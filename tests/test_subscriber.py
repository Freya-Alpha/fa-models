import pytest
from famodels.subscriber import SubscriberIn, SubscriberInDb

@pytest.mark.parametrize("email, ip_address", [
    ("test@test.com", "127.0.0.1"),
    ("john.doe@swiss.com", "192.168.169.69"),
    ("alias001@microsoft.com", "192.168.169.226"),
    ("alias001@ubuntu.com", "100.128.0.0")
])
def test_subscriber_in_model(email: str, ip_address: str):
    """Test if we can create an subscriber model with various parameters."""
    subscriber = SubscriberIn(
        email=email,
        ip_address=ip_address)

    assert subscriber.email == email
    assert subscriber.ip_address == ip_address

@pytest.mark.parametrize("email, ip_address", [
    ("    name@domain.com    ", "100.128.0.0"),
])
def test_subscriber_in_model_with_whitspace_email(email: str, ip_address: str):
    """Test if we can create an subscriber model with various parameters."""
    subscriber = SubscriberIn(
        email=email,
        ip_address=ip_address)

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
def test_subscriber_in_model_for_validation_errors(email: str, ip_address: str):
    with pytest.raises(Exception):
        SubscriberIn(
            email=email,
            ip_address=ip_address)

@pytest.mark.parametrize("ip_address, ip_address_lat, ip_address_lon", [
    ("100.128.0.0", "30.2", "70.93838"),
    ("166.128.0.0", "89.2", "179.93838")])
def test_subscriber_in_db_model(ip_address: str, ip_address_lat: float, ip_address_lon: float):
    subscriberInDb = SubscriberInDb(
        ip_address=ip_address,
        ip_address_location_lat=ip_address_lat,
        ip_address_location_lon=ip_address_lon)

    assert subscriberInDb.ip_address == ip_address
    assert subscriberInDb.ip_address_location_lat == ip_address_lat
    assert subscriberInDb.ip_address_location_lon == ip_address_lon

@pytest.mark.parametrize("ip_address, ip_address_lat, ip_address_lon", [
    (None, "30.2", "70.93838"),
    ("100.128.0.0", "120", "60"),
    ("100.128.0.0", "89", "181")])
def test_subscriber_in_db_model_for_validation_errors(ip_address: str, ip_address_lat: str, ip_address_lon: str):
    with pytest.raises(Exception):
        SubscriberInDb(
            ip_address=ip_address,
            ip_address_location_lat=ip_address_lat,
            ip_address_location_lon=ip_address_lon)
