import json
import threading
import time
from abc import ABC,abstractmethod
from datetime import datetime
from decouple import config
from models.price import Price


class Strategy(ABC):
    price: Price

    def __init__(self, exchange, interval = 60, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.portfolio = {}
        self.exchange = exchange
        self.get_portfolio()

    def _run(self):
        self.is_running = False
        self.start()
        self.run()

    @abstractmethod
    def run(self):
        pass

    def start(self):
        if not self.is_running:
            print(datetime.now())
            if self._timer is None:
                self.next_call = time.time()
            else:
                self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def get_portfolio(self):
        self.portfolio = {'currency': self.exchange.get_asset_balance(self.exchange.currency),
                          'asset': self.exchange.get_asset_balance(self.exchange.asset)}

    def get_price(self):
        try:
            self.price = self.exchange.symbol_ticker()
        except Exception as e:
            pass
