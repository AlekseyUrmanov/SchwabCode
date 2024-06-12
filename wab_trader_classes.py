import time
import datetime


class product:

    def __init__(self, shares, ticker, api_client):

        self.shares = shares
        self.ticker = ticker
        self.ask = 0
        self.bid = 0
        self.spreads = []
        self.bids = []
        self.trading_weights = []

        self.open = False
        self.position = False

        self.open_order_price = 0
        self.close_order_price = 0

        self.time_order_open = None
        self.order_ID = None

        self.api_client_object = api_client
        self.pst = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'

    def spread(self):
        return self.ask - self.bid

    def get_down_impulse(self):

        differences = []
        for i in range(len(self.bids) - 1):
            if self.bids[i + 1] < self.bids[i]:
                differences.append(self.bids[i] - self.bids[i + 1])

        # apply weights
        weighted_diff = []
        len_diff = len(differences)

        return (sum(differences) / len(differences))

    def process_data(self, data):

        self.bid = data[self.ticker]['quote']['bidPrice']
        self.ask = data[self.ticker]['quote']['askPrice']
        weight = (float(data[self.ticker]['quote']['lastPrice']) - float(self.bid) )/ (self.spread())

        self.trading_weights.append(weight)
        self.spreads.append(self.ask - self.bid)
        self.bids.append(self.bid)

        if len(self.bids) > 240:
            self.bids.pop(0)

        print('Data for ' + self.ticker + ' updated --> BID:'+str(self.bid) + ' ASK:'+str(self.ask))

    def avg_spread(self):

        return sum(self.spreads) / len(self.spreads)

    def _smart_price(self, buy_sell):

        min_unit = 0.01

        spread_units = int((self.spread() / min_unit) / 2)

        middle_market_price = (float(self.ask) + float(self.bid)) / 2
        middle_buy_price = (middle_market_price + float(self.bid)) / 2

        if buy_sell == 'BUY':

            distance_down = self.get_down_impulse()

            price = float(self.bid) - distance_down
            price = round(price, 2)
            return price

        else:

            middle_market_price = round((float(self.bid) + float(self.ask)) / 2, 2)

            if middle_market_price < float(self.open_order_price):
                print('market price lower than open')
                return self.open_order_price
            else:

                return middle_market_price

    def generate_order_ID(self):

        data = self.api_client_object.get_orders(type='WORKING', from_time=self.pst)
        # print(data)
        for order in data:
            orderLegCollection = order['orderLegCollection'][0]
            symbol = orderLegCollection['instrument']['symbol']

            if symbol == self.ticker:
                self.order_ID = order['orderId']
                break
            else:
                pass

    def close_position(self, paper=True):

        if self.position is not True:
            pass
        else:

            price = self._smart_price(buy_sell='SELL')
            self.api_client_object.limit_order(price=price, symbol=self.ticker, buysell='SELL', amount=self.shares)
            self.open = True
            self.close_order_price = price

            self.time_order_open = datetime.datetime.now()
            self.generate_order_ID()
            print('SELLING ORDER TO CLOSE AT --> ' + str(price) + ' ' + str(self.ticker) + ' ' + str(self.order_ID))

            return

    def open_position(self, paper=True):

        if len(self.bids) < 100: # not enough data gathered to Trade
          pass

        else:
            price = self._smart_price(buy_sell='BUY')
            self.api_client_object.limit_order(price=price, symbol=self.ticker, buysell='BUY', amount=self.shares)
            self.open = True
            self.open_order_price = self.bid
            self.time_order_open = datetime.datetime.now().isoformat()

            self.generate_order_ID()
            print('BUYING ORDER TO OPEN AT --> ' + str(self.bid) + ' ' + str(self.ticker) + ' ' + str(self.order_ID))

            return

    def maintain_buy_order(self):

        target_buying_price = float(self.bid) - self.get_down_impulse()
        print('downward impulse: ' + str(self.get_down_impulse()))
        target_buying_price = round(target_buying_price, 2)
        if round(float(self.open_order_price), 2) != target_buying_price:
            print('target purchase price: '+ str(target_buying_price))
            print('actual order price: ' + str(self.open_order_price))

            self.api_client_object.put_replace(order_id_replacing=self.order_ID,
                                               symbol=self.ticker,
                                               amount=self.shares,
                                               price=target_buying_price,
                                               buysell="BUY")

            self.generate_order_ID()
            self.open_order_price = target_buying_price
            self.time_order_open = datetime.datetime.now().isoformat()

        else:

            pass

    def maintain_sell_order(self):
        # self.selling_state = True
        # get order ID

        if float(self.ask) < (float(self.close_order_price) - (self.spread() * 4)):  # liquidating at a loss

            return




class portfolio:

    def __init__(self, products, stocks, api_client):

        self.api_client_object = api_client

        self.products = products
        self.stocks = stocks

        self.account_orders = {}

        self.object_product_mapping = {}

        for p in products:
            self.object_product_mapping[p.ticker] = p

        self.sold = 0
        self.pst = time.time()

    def collect_data(self):

        data = self.api_client_object.quote_data(stocks=self.stocks)

        self._update(data)

        if (time.time() - self.pst) > (60 * 20):
            self.api_client_object.refresh_token_auth()
            self.pst = time.time()
        else:
            pass

    def _update(self, data):
        for p in self.products:
            p.process_data(data)

    def test_conditions(self):
        for p in self.products:

            if (p.open is True) and (p.position is True):  # We are checking our open order to sell
                p.maintain_sell_order()

            elif p.open and not p.position:  # We are checking our open order to buy
                p.maintain_buy_order()

            elif not p.open and p.position:  # We need to open an order to sell
                self.sold = self.sold + 1
                p.close_position(paper=False)

            else:  # We need to open an order to buy
                p.open_position(paper=False)

    def poll_account_data(self):

        data = self.api_client_object.get_positions()
        try:
            subset_data = data[0]['securitiesAccount']['positions']
        except KeyError:
            subset_data = []
            pass

        position_tickers = []
        for product_position_dict in subset_data:
            ticker = product_position_dict['instrument']['symbol']
            position_tickers.append(ticker)

        for ticker in self.object_product_mapping:
            if ticker in position_tickers:
                position_exists = True
            else:
                position_exists = False

            if self.object_product_mapping[ticker].position is not position_exists:  # old state is not new state

                self.object_product_mapping[ticker].open = False
                self.object_product_mapping[ticker].position = position_exists

            # print(self.object_product_mapping[ticker].open)
            # print(self.object_product_mapping[ticker].position)




