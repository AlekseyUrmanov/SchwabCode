from testing import SWclient

import time
import datetime

import asyncio


swb = SWclient()
program_start_time = str( datetime.datetime.now().isoformat())[0:-3] + 'Z'
print(program_start_time)
class product:

    def __init__(self, shares, ticker):
        self.shares = shares
        self.ticker = ticker
        self.ask = 0
        self.bid = 0
        self.spreads = []
        self.bids = []


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

    def get_down_impulse(self):

        differences = []
        for i in range(len(self.bids)-1):
            if self.bids[i+1] < self.bids[i]:
                differences.append(self.bids[i] - self.bids[i+1])

        return (sum(differences) / len(differences))

    def process_data(self, data):

        self.bid = data[self.ticker]['quote']['bidPrice']
        self.ask = data[self.ticker]['quote']['askPrice']
        self.spreads.append(self.ask - self.bid)
        self.bids.append(self.bid)

        if len(self.bids) > 120:
            self.bids.pop(0)

        #print('Data for ' + self.ticker + ' updated. ASK:'+str(self.ask) + ' BID:'+str(self.bid) )

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
                return self.open_order_price
            else:

                return middle_market_price


    def generate_order_ID(self):

        data = swb.get_orders(type='WORKING', from_time=program_start_time)
        #print(data)
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
            swb.limit_order(price=price, symbol=self.ticker, buysell='SELL', amount=self.shares)
            self.open = True
            self.close_order_price = self.ask

            self.time_order_open = datetime.datetime.now()
            self.generate_order_ID()
            print('SELLING ORDER TO CLOSE AT --> ' + str(self.ask) +' '+ str(self.ticker) + ' ' + str(self.order_ID))

            return

    def open_position(self, paper=True):

        if paper:

            print('PURCHASE ORDER TO OPEN AT --> '+ str(self.bid))
            self.open = True
            self.open_order_price = self.bid

        else:
            price = self._smart_price(buy_sell='BUY')
            swb.limit_order(price=price, symbol=self.ticker, buysell='BUY', amount=self.shares)
            self.open = True
            self.open_order_price = self.bid
            self.time_order_open = datetime.datetime.now().isoformat()

            self.generate_order_ID()
            print('BUYING ORDER TO OPEN AT --> ' + str(self.bid) +' '+ str(self.ticker) + ' ' + str(self.order_ID))

            return


    def maintain_buy_order(self):

        target_buying_price = float(self.bid) - self.get_down_impulse()
        target_buying_price = round(target_buying_price, 2)
        if round(float(self.open_order_price), 2) != target_buying_price:

            swb.put_replace(order_id_replacing=self.order_ID,
                            symbol=self.ticker,
                            amount=self.shares,
                            price=target_buying_price,
                            buysell="BUY")

            self.generate_order_ID()

        else:

            pass



    def maintain_sell_order(self):
        #self.selling_state = True
        # get order ID


        if float(self.ask) < (float(self.close_order_price)- (self.spread()*4)): #liquidating at a loss
            #print('Forced Position Sale @ ' + str(self.bid) + '$ on ' + str(self.ticker))

            print('cancelling order because price drop')
            swb.del_order(order_id=self.order_ID)
            self.open = False


            #self.position = False

            #swb.market_order(symbol=self.ticker, amount=self.shares, buysell='SELL')

            #self.order_ID = 0
            #self.close_order_price = 0
            #self.open_order_price = 0
            return


        '''if float(self.ask) < float(self.close_order_price):

            if float(self.ask) > float(self.open_order_price):


                swb.del_order(order_id=self.order_ID)
                self.open = False
            else:
                pass
        else:
            pass'''

        # t_diff = time.time() - self.time_order_open # time diff in seconds since order is opened

        # swb.del_order(order_id=self.order_ID)

        # smart price
        pass



class portfolio:

    def __init__(self, products, stocks):
        self.products = products
        self.stocks = stocks

        self.account_orders = {}

        self.object_product_mapping = {}

        for p in products:
            self.object_product_mapping[p.ticker] = p

        self.sold = 0
        self.pst = time.time()


    def collect_data(self):
        #print('collecting data')
        data = swb.quote_data(stocks=self.stocks)

        self._update(data)








        if( time.time() - self.pst) > (60*20):
            swb.refresh_token_auth()
            self.pst = time.time()
        else:
            pass

    def _update(self, data):
        #print(data)
        for p in self.products:
            p.process_data(data)

    def test_conditions(self):
        #print('testing conditons')
        for p in self.products:

            if (p.open is True) and (p.position is True): # I have an order to sell
                #print('maintain sell order')
                p.maintain_sell_order()
                pass

            elif p.open and not p.position: # Open order
                #print('maintain buy order')

                p.maintain_buy_order()
                pass

            elif not p.open and p.position: # we got filled
                #print('starting close pos fx')
                self.sold = self.sold + 1
                p.close_position(paper=False)

                pass

            else: # we don't have a position or an order (default case)
                #print('starting open pos fx')

                p.open_position(paper=False)
                pass

    def poll_account_data(self):

        data = swb.get_positions()
        try:
            subset_data = data[0]['securitiesAccount']['positions']
        except KeyError:
            subset_data = []
            pass


        position_tickers = []
        for product_position_dict in subset_data:
            ticker = product_position_dict['instrument']['symbol']
            # stock_amount = product_position_dict['longQuantity']
            position_tickers.append(ticker)

        for ticker in self.object_product_mapping:
            if ticker in position_tickers:
                # position is true
                position_exists = True
            else:
                # position is false
                position_exists = False
                #self.object_product_mapping[ticker].selling_state = False

            if self.object_product_mapping[ticker].position is not position_exists:  # old state is not new state

                self.object_product_mapping[ticker].open = False
                self.object_product_mapping[ticker].position = position_exists

            #print(self.object_product_mapping[ticker].open)
            #print(self.object_product_mapping[ticker].position)






products = [product(1,'NVDA')]

big_spread_trading_port = portfolio(products,'NVDA')


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
    time.sleep(130)
    task2 = asyncio.create_task(method_two())
    task3 = asyncio.create_task(method_three())

    await asyncio.gather(task1, task2, task3)

    # Continue with other tasks or operations without waiting for function_one() and function_two() to finish
    print("Continuing with other tasks or operations...")




asyncio.run(run_all())



