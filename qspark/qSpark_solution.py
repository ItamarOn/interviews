from dataclasses import dataclass
from typing import Dict, Literal
from decimal import Decimal
import logging

from collections import deque

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


Side = Literal['Buy', 'Sell']

@dataclass
class Trade:
    stock: str
    side: Side
    quantity: int
    price: Decimal

    def __post_init__(self):
        if isinstance(self.price, float):
            self.price = Decimal(str(self.price))

class PnLCalculator:
    def __init__(self):
        self.buy_queues: Dict[str, deque] = {}

    def _add_buy_to_queue(self, stock, trade):
        self.buy_queues[stock].append([trade.quantity, trade.price])
        return Decimal(0)

    def _fifo_sell_from_queue(self, stock, trade):
        pnl = Decimal(0)
        sell_qty = trade.quantity
        while sell_qty > 0 and self.buy_queues[stock]:
            logger.info(f'buy_queues: {self.buy_queues}')

            buy_qty, buy_price = self.buy_queues[stock][0]
            logger.info(f"buy_qty: {buy_qty}, buy_price: {buy_price}")

            matched_qty = min(sell_qty, buy_qty)
            pnl += matched_qty * (trade.price - buy_price)
            logger.info(f"pnl: {pnl} for matched_qty: {matched_qty}")

            sell_qty -= matched_qty
            buy_qty -= matched_qty
            logger.info(f"sell_qty: {sell_qty} buy_qty: {buy_qty}")

            if buy_qty == 0:
                self.buy_queues[stock].popleft()
            else:
                self.buy_queues[stock][0][0] = buy_qty
        return pnl


    def calc_pnl(self, trade: Trade) -> Decimal:
        stock = trade.stock

        if stock not in self.buy_queues:
            self.buy_queues[stock] = deque()

        if trade.side == 'Buy':
            return self._add_buy_to_queue(stock, trade)
        else:
            return self._fifo_sell_from_queue(stock, trade)




calc = PnLCalculator()
assert calc.calc_pnl(Trade("AAPL", "Buy", 100, 220.90))  == 0.0
assert calc.calc_pnl(Trade("AAPL", "Buy", 200, 221.05))  == 0.0
assert calc.calc_pnl(Trade("IBM", "Buy", 100, 203.50))   == 0.0
assert calc.calc_pnl(Trade("AAPL", "Sell", 50, 221.10))  == 10.0
assert calc.calc_pnl(Trade("AAPL", "Sell", 100, 221.00)) == 2.5
