import time
import sys
import td_api as tdc
import asyncio


tdc = tdc.TDclient()


#Options_data = tdc.option_chain(details=['F', False])
#Options_data = tdc.sort_data_into_data_frames(Options_data)


# check spread, bid, ask
# track avg spread


# condition to remove order
# if ask is closer to our position than 50% of spread


# place bid order
# if not filled by the next loop cycle
# move it up.
# repeat

# place order at ask.
# if not filled by the next loop cycle
# move it down.
# repeat



# monitor spread process is started






class product:
    def __init__(self, shares, ticker):
        self.shares = shares
        self.ticker = ticker
        self.ask = 0
        self.bid = 0
        self.spreads = []

        self.open = False
        self.position = False
        self.to_open = False

        self.open_order_price = 0
        self.close_order_price = 0

        self.time_order_open = None
        self.order_ID = None

        self.selling_state = False

    def spread(self):
        return self.ask - self.bid

    def process_data(self, data):

        self.bid = data[self.ticker]['bidPrice']
        self.ask = data[self.ticker]['askPrice']
        self.spreads.append(self.ask - self.bid)
        #self._smart_price('SELL')

    def avg_spread(self):

        return sum(self.spreads) / len(self.spreads)

    def _smart_price(self, buy_sell):

        min_unit = 0.01

        spread_units = int((self.spread() / min_unit) / 2)

        if buy_sell == 'BUY':

            if spread_units > 5:
                higher_price = self.bid + min_unit
                return higher_price
            else:
                return self.bid
        else:

            selling_price_ladder = [self.ask]
            middle_market_price = self.ask - (spread_units * min_unit)

            new_price = self.close_order_price - min_unit

            if new_price > middle_market_price:
                new_lower_price = round(new_price, 2)
                return new_lower_price

            else:
                return self.close_order_price


            '''while True:
                price = round(selling_price_ladder[-1] - min_unit, 2)

                if price > middle_market_price and len(selling_price_ladder) < 10:
                    selling_price_ladder.append(price)
                else:
                    break'''




    def generate_order_ID(self):

        data = tdc.get_account_orders()
        for order in data:
            orderLegCollection = order['orderLegCollection'][0]
            symbol = orderLegCollection['instrument']['symbol']

            if symbol == self.ticker:
                self.order_ID = order['orderId']
            else:
                pass



    def close_position(self, paper=True):

        if paper:

            print('SELLING ORDER TO CLOSE AT --> ' + str(self.ask))
            self.open = True
            self.close_order_price = self.ask

        elif self.selling_state:

            new_price = self._smart_price(buy_sell='SELL')
            tdc.equity_order(price=new_price, stock=self.ticker, buysell='SELL', amount=self.shares)
            print('SELLING ORDER TO CLOSE AT --> ' + str(self.ask))
            self.open = True
            self.close_order_price = new_price
            self.time_order_open = time.time()
            self.generate_order_ID()
            return

        else:

            tdc.equity_order(price=self.ask, stock=self.ticker, buysell='SELL', amount=self.shares)
            print('SELLING ORDER TO CLOSE AT --> ' + str(self.ask))
            self.open = True
            self.close_order_price = self.ask
            self.time_order_open = time.time()
            self.generate_order_ID()
            return

    def open_position(self, paper=True):

        if paper:

            print('PURCHASE ORDER TO OPEN AT --> '+ str(self.bid))
            self.open = True
            self.open_order_price = self.bid

        else:

            tdc.equity_order(price=self.bid, stock=self.ticker, buysell='BUY', amount=self.shares)
            print('PURCHASE ORDER TO OPEN AT --> '+ str(self.bid))
            self.open = True
            self.open_order_price = self.bid
            self.time_order_open = time.time()
            self.generate_order_ID()
            return


    def maintain_buy_order(self):

        self.selling_state = False




        return

    def maintain_sell_order(self):
        self.selling_state = True
        # get order ID

        t_diff = time.time() - self.time_order_open # time diff in seconds since order is opened

        if t_diff > 5: # if order has been open for more than 3 seconds

            p = self._smart_price(buy_sell="SELL")

            if p == self.close_order_price: # we don't want to cancel the order if there is no better price
                pass
            else:

                tdc.cancel_option_order(OID=self.order_ID)
            # cancel order
            # test conditions will launch close position.
            # close position will read that selling state is true, it
            # will look at the previous order price and place a new order just below it from smart_order fx
        return



class portfolio:

    def __init__(self, products):
        self.products = products
        self.account_orders = {}
        self.object_product_mapping = {}
        for p in products:
            self.object_product_mapping[p.ticker] = p

        self.sold = 0


    def collect_data(self, testing=True):

        tickers = [obj.ticker for obj in self.products]
        data = tdc.get_quotes(details=[tickers, True])
        self._update(data)

    def _update(self, data):
        #print(data)
        for p in self.products:
            p.process_data(data)

    def test_conditions(self):
        #print('testing conditons')
        for p in self.products:
            if p.open and p.position: # Trying to close position
                print('maintain sell order')
                p.maintain_sell_order()

                return

            elif p.open and not p.position: # trying to buy position
                print('maintain buy order')

                p.maintain_buy_order()
                return

            elif not p.open and p.position: # we got filled
                print('starting close pos fx')
                self.sold = self.sold + 1
                p.close_position(paper=True)

                return

            else: # we don't have a position or an order (default case)
                print('starting open pos fx')
                if self.sold == 1:
                    p.open_position(paper=True)
                    sys.exit()
                else:
                    p.open_position(paper=True)
                return

    def poll_account_data(self):

        data = tdc.get_account_positions(details=None)
        subset_data = data['securitiesAccount']['positions']

        position_tickers = []
        for product_position_dict in subset_data:

            ticker = product_position_dict['instrument']['symbol']
            #stock_amount = product_position_dict['longQuantity']
            position_tickers.append(ticker)

        for ticker in self.object_product_mapping:
            if ticker in position_tickers:
                # position is true
                position_exists = True
            else:
                #position is false
                position_exists = False
                self.object_product_mapping[ticker].selling_state = False

            if self.object_product_mapping[ticker].position is not position_exists:  # old state is not new state

                self.object_product_mapping[ticker].open = False
                self.object_product_mapping[ticker].position = position_exists

            #print(self.object_product_mapping[ticker].open)
            #print(self.object_product_mapping[ticker].position)


products = [product(1,'NFLX')]

big_spread_trading_port = portfolio(products)


async def method_one():

    while True:
        big_spread_trading_port.collect_data()
        await asyncio.sleep(1)


async def method_two():

    while True:
        big_spread_trading_port.test_conditions()
        await asyncio.sleep(1)


async def method_three():

    while True:
        big_spread_trading_port.poll_account_data()
        await asyncio.sleep(1)


async def run_all():
    # Schedule both functions concurrently
    task1 = asyncio.create_task(method_one())
    task2 = asyncio.create_task(method_two())
    task3 = asyncio.create_task(method_three())

    await asyncio.gather(task1, task2, task3)

    # Continue with other tasks or operations without waiting for function_one() and function_two() to finish
    print("Continuing with other tasks or operations...")




asyncio.run(run_all())

# program does not work after full round trip


