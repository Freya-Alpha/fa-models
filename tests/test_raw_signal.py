from datetime import datetime
from uuid import UUID
from famodels.raw_signal import RawSignal
from fasignalprovider.trading_signal import TradingSignal
from fasignalprovider.direction import Direction
from fasignalprovider.side import Side


def test_raw_signal_creation():
    # Create a TradingSignal instance
    trading_signal = TradingSignal(
        provider_id="provider1",
        strategy_id="strategy123",
        provider_signal_id="signal3746",
        provider_trade_id="trade456",
        is_hot_signal=True,
        market="BTC/USDT",
        data_source="CoinGecko",
        direction=Direction.LONG,
        side=Side.BUY,
        price=50000.0,
        tp=51000.0,
        sl=49500.0,
        position_size_in_percentage=50
    )

    # Wrap it into a RawSignal
    raw_signal = RawSignal.from_trading_signal(trading_signal)

    # Assert that all TradingSignal attributes are correctly copied
    assert raw_signal.provider_id == trading_signal.provider_id
    assert raw_signal.strategy_id == trading_signal.strategy_id
    assert raw_signal.provider_trade_id == trading_signal.provider_trade_id
    assert raw_signal.is_hot_signal == trading_signal.is_hot_signal
    assert raw_signal.market == trading_signal.market
    assert raw_signal.data_source == trading_signal.data_source
    assert raw_signal.direction == trading_signal.direction
    assert raw_signal.side == trading_signal.side
    assert raw_signal.price == trading_signal.price
    assert raw_signal.tp == trading_signal.tp
    assert raw_signal.sl == trading_signal.sl
    assert raw_signal.position_size_in_percentage == trading_signal.position_size_in_percentage

    # Assert that the id is a valid UUID4
    assert UUID(raw_signal.id, version=4)

    # Assert that the timestamp_of_registration is set and is a datetime object
    assert isinstance(raw_signal.date_of_registration, datetime)

def test_raw_signal_default_values():
    # Create a RawSignal with default values
    raw_signal = RawSignal(
        provider_id="default_provider",
        strategy_id="default_strategy",        
        provider_trade_id="default_trade_id",
        provider_signal_id="default_signal_id",
        is_hot_signal=False,
        market="ETH/USD",
        data_source="Chainlink",
        direction=Direction.LONG,
        side=Side.BUY,
        price=3000.0,
        tp=2900.0,
        sl=3050.0,
        position_size_in_percentage=100
    )

    # Assert default values for id and timestamp_of_registration
    assert UUID(raw_signal.id, version=4)
    assert isinstance(raw_signal.date_of_registration, datetime)

# Add more test cases as needed to cover different scenarios and edge cases.
