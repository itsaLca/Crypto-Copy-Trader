from abc import ABC, abstractmethod


class Exchange(ABC):
    balance = None
    exchange_name = None
    master_balance = None
    isMargin = None
    expected_orders = list()

    def __init__(self, apiKey, apiSecret, pairs, name="Unnamed"):
        self.api = {'key': apiKey,
                    'secret': apiSecret}
        # delete '\n' from symbols'
        self.pairs = list(map(lambda pair: pair.replace('\n', ''), pairs))
        self.name = name

    def get_balance(self):
        return self.balance

    def get_trading_symbols(self):
        symbols = set()
        for pair in self.pairs:
            pair = str(pair)
            symbols.add(pair[:3])
            symbols.add(pair[3:])
        return symbols

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self, caller_callback):
        pass

    @abstractmethod
    def process_event(self, event):
        pass

    @abstractmethod
    def on_order_handler(self, event):
        pass

    @abstractmethod
    def get_open_orders(self):
        pass

    @abstractmethod
    async def on_cancel_handler(self, event):
        pass

    @abstractmethod
    def create_order(self, order):
        pass

    async def async_create_order(self, order):
        self.create_order(order)

    @abstractmethod
    def get_part(self, symbol, quantity, price):
        pass

    @abstractmethod
    def calc_quantity_from_part(self, symbol, quantityPart, price, side):
        pass

    def add_expected_order_id(self, id, callback):
        self.expected_orders.append({'id': id,
                                     'callback': callback})

    def check_expected_order(self, order):
        for expected_order in self.expected_orders:
            if order.id == expected_order['id']:
                expected_order['callback'](order)

    async def close_position(self, symbol):
        print(f" exchange {self.exchange_name} do not support event \' close_position \' ")