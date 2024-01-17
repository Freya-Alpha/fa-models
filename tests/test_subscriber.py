import pytest
from famodels.subscriber import Subscriber

@pytest.mark.parametrize("email, ip_address", [
    ("test@test.com", "127.0.0.1"),
    ("john.doe@swiss.com", "192.168.169.69"),
    ("alias001@microsoft.com", "192.168.169.226"),
    ("alias001@ubuntu.com", "100.128.0.0")
])
def test_subscriber_model(email: str, ip_address: str):
    """Test if we can create an subscriber model with various parameters."""
    subscriber = Subscriber(
        email=email,
        ip_address=ip_address,
    )

    assert subscriber.email == email
    assert subscriber.ip_address.compressed == ip_address

@pytest.mark.parametrize("email, ip_address", [
    ("    name@domain.com    ", "100.128.0.0"),
])
def test_subscriber_model_with_whitspace_email(email: str, ip_address: str):
    """Test if we can create an subscriber model with various parameters."""
    subscriber = Subscriber(
        email=email,
        ip_address=ip_address,
    )

    assert subscriber.email == email.strip()
    assert subscriber.ip_address.compressed == ip_address

@pytest.mark.parametrize("email, ip_address", [
    (None, "127.0.0.1"),
    ("test@test.com", None),
    (None, None),
    ("test@test.com", "127 .0.0.1"),
    ("john.doe@swiss.com", "999.255.255.255"),
    ("@microsoft.com", "192.168.169.226"),
    ("alias001@ubuntu", "100.128.0.0/222")])
def test_subscriber_model_for_validation_errors(email: str, ip_address: str):
    with pytest.raises(Exception):
        Subscriber(
            email=email,
            ip_address=ip_address,
        )
