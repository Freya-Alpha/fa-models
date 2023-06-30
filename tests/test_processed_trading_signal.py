
# from time import time
# import pytest
# from famodels.models.direction import Direction
# from famodels.models.side import Side
# from famodels.models.state_of_signal import StateOfSignal

# from famodels.models.trading_signal import TradingSignal

# set the redis om env variable before instantiating the object.
# SIGNAL_1 = TradingSignal(id="10", provider_signal_id="sifwi", provider_trade_id="wuwor232", is_hot_signal=False, algo_id="232424", market="BTC/USDT", 
#                          exchange="binance", direction=Direction.LONG, side=Side.BUY, price=20000, tp=22000, sl=19000, timestamp_of_creation=int(time()*1000), timestamp_of_registration=int(time()*1000))
# SIGNAL_2 = TradingSignal(id="10", provider_signal_id="sifwi", provider_trade_id="wuwor232", is_hot_signal=False, algo_id="232424", market="BTC/USDT", 
#                          exchange="binance", direction=Direction.LONG, side=Side.BUY, price=20000, tp=22000, sl=19000, timestamp_of_creation=int(time()*1000) )

# @pytest.mark.parametrize("signal, invalidations, expectation", [
#     (SIGNAL_1, ["Failed to do something smart.", "And also this"] ,True),
#     (SIGNAL_2, [], True)
# ])
# def test_instantiation(signal:TradingSignal, invalidations, expectation):
#     proc_signal = ProcessedTradingSignal(status=StateOfSignal.ACCEPTED, process_info=[], **signal.__dict__)
#     assert proc_signal.id == "10"
#     assert proc_signal.status == StateOfSignal.ACCEPTED


def test_dummy():
    pass

def test_dummy_2():
    pass