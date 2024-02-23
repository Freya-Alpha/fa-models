import pytest
from datetime import datetime
from famodels.raw_signal import RawSignal
from famodels.rejected_signal import RejectedSignal, ReasonForRejection
from fasignalprovider.direction import Direction
from fasignalprovider.side import Side

def create_example_raw_signal():
    # Create and return a RawSignal instance for testing
    # Replace these attribute values with those relevant for RawSignal in your application
    return RawSignal(
        provider_id="test_provider",
        strategy_id="test_strategy",
        provider_signal_id="signal_id_2324",
        provider_trade_id="test_trade_id",
        is_hot_signal=True,
        market="Test Market",
        data_source="chainlink",
        direction=Direction.LONG,
        side=Side.BUY,
        price=100.0,
        tp=110.0,
        sl=90.0,
        position_size_in_percentage=100
    )

def test_rejected_signal_creation():
    raw_signal = create_example_raw_signal()
    reasons = {ReasonForRejection.SCAM}

    rejected_signal = RejectedSignal.from_raw_signal(raw_signal, reasons)

    # Check if all RawSignal attributes are correctly copied
    assert rejected_signal.provider_id == raw_signal.provider_id
    assert rejected_signal.strategy_id == raw_signal.strategy_id
    # Check if the rejection reason is correctly set
    assert rejected_signal.reasons_for_rejection == reasons
    # Check if the date_of_rejection is set and is a datetime object
    assert isinstance(rejected_signal.date_of_rejection, datetime)

def test_rejected_signal_without_reason():
    raw_signal = create_example_raw_signal()

    # Expect an error when trying to create a RejectedSignal without a reason
    with pytest.raises(TypeError):
        RejectedSignal.from_raw_signal(raw_signal)
