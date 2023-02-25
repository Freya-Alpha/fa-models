from famodels.direction import Direction
from famodels.side import Side
from famodels.trading_signal import TradingSignal
import uuid, random

class Generator:
    
    def generate_batch_of_signals(self, number_of_signals:int=10):
        """ Generates a random block of signals. 
            Upcoming versions will allow sequencing (id, timestamp, etc.)
        """
        signals = []
        for i in range(1,number_of_signals):
            signals.append(self.generate_random_signal())
        return signals
    
    # This needs to be moved into the fa-model library
    def generate_random_signal(self, dir:Direction = Direction.LONG):
        id = str(uuid.uuid4())
        algo_id = str(uuid.uuid4())
        provider_id = str(uuid.uuid4())        
        stable = random.choice(["USD", "USDT", "USDC", "BUSD", "CHF"])
        asset = random.choice(["BTC", "ETH", "BNB", "NEAR", "MATIC", "AAPL", "TSLA", "CS"])
        market = f"{asset}/{stable}"
        exchange = random.choice(["BINANCE", "Binance", "Kucoin", "KUCOIN", "dydx", "perp", "uni"])
        trade_correlation_id = str(uuid.uuid4())        
        direction = random.choice(list(Direction))        
        side = random.choice(list(Side))
        price = random.uniform(0.01, 68000)
        
        if dir == Direction.LONG:
            tp = random.uniform(price * 1.03, price * 1.20)
            sl = random.uniform(price * 0.97, price * 0.8)
        else:
            tp = random.uniform(price * 0.97, price * 0.8)
            sl = random.uniform(price * 1.03, price * 1.20)
            
        return TradingSignal(id=id, algo_id=algo_id, provider_id=provider_id, market=market, exchange=exchange, 
                      trade_correlation_id=trade_correlation_id, direction=direction, side=side, price=price,
                       tp=tp, sl=sl)