import testing
import time
wab_api = testing.SWclient()
import random
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import threading
import datetime




pst =  str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
#wab_api.refresh_token_auth()
class DataCollector:
    def __init__(self, stocks):
        self.data = {}
        self.stocks = stocks
        self.trade_booleans = {}
        self.secondary_trade_booleans = {}
        self.open_order_stocks = []
        self.orders_by_symbol = {}
        self.st = time.time()

    def collect_data(self):
        while True:
                # Simulate data collection and update the dictionary
                quote_data = wab_api.quote_data(self.stocks)
                t = time.time()
                for symbol in quote_data.keys():

                    symbol_data = quote_data[symbol]
                    ltp = symbol_data['quote']['lastPrice']
                    bid = symbol_data['quote']['bidPrice']
                    ask = symbol_data['quote']['askPrice']
                    bid_size = symbol_data['quote']['bidSize']
                    ask_size = symbol_data['quote']['askSize']
                    spread = round(ask - bid, 2)

                    weight = (ltp-bid)/ spread

                    if symbol not in self.data:
                        self.trade_booleans[symbol] = False
                        self.secondary_trade_booleans[symbol] = False
                        self.data[symbol]= {'bids':[bid],
                                                   'asks':[ask],
                                                   'ltps':[ltp],
                                                   'spreads':[spread],
                                                   'bid_size':[bid_size],
                                                   'ask_size':[ask_size],
                                                    'ltp_weight':[weight],
                                            'bid_delta':[0],
                                            'bid':0,
                                            'ask':0,
                                            'trade_condition':[0],
                                            'reduction':0}

                    else:
                        self.data[symbol]['bids'].append(bid)
                        self.data[symbol]['asks'].append(ask)
                        self.data[symbol]['ltps'].append(ltp)
                        self.data[symbol]['spreads'].append(spread)
                        self.data[symbol]['bid_size'].append(bid_size)
                        self.data[symbol]['ask_size'].append(ask_size)
                        self.data[symbol]['ltp_weight'].append(weight)

                        self.data[symbol]['bid'] = bid
                        self.data[symbol]['ask'] = ask



                        previous_bid = self.data[symbol]['bids'][-2]
                        bid_delta = bid - previous_bid
                        self.data[symbol]['bid_delta'].append(bid_delta)


                    n = len(self.data[symbol]['bids'])

                    if n < 32:
                        self.data[symbol]['bid_delta_smooth'] = []

                    elif n < 60:
                        l = len(self.data[symbol]['bid_delta'])
                        bd = self.data[symbol]['bid_delta']
                        self.data[symbol]['bid_delta_smooth'].append(sum(bd[l-31:l-1]) / 30)

                        pass
                    else:
                        # add data to smoothed bid delta
                        l = len(self.data[symbol]['bid_delta'])
                        bd = self.data[symbol]['bid_delta']
                        new_smooth_delta_point = sum(bd[l - 31:l - 1]) / 30
                        self.data[symbol]['bid_delta_smooth'].append(new_smooth_delta_point)

                        # compute stats
                        spread_mean = sum(self.data[symbol]['spreads'])/len(self.data[symbol]['spreads'])
                        smooth_bid_delta_sd = statistics.stdev(self.data[symbol]['bid_delta_smooth'])

                        smooth_bid_delta_mean = (sum(self.data[symbol]['bid_delta_smooth']) /
                                                 len(self.data[symbol]['bid_delta_smooth']))



                        previous_bid = self.data[symbol]['bids'][-2]
                        delta = 0
                        z_score = (new_smooth_delta_point - smooth_bid_delta_mean) / smooth_bid_delta_sd
                        #print(z_score)
                        '''
                        print('Bid price: '+ str(bid)+ ' Smoothed Bid Delta: '+ str(new_smooth_delta_point))
                        print('Mean Smoothed Bid Delta: '+ str(smooth_bid_delta_mean))
                        print('Time to process data: '+ str(time.time()- t))
                        print()'''




                        self.data[symbol]['reduction'] = new_smooth_delta_point
                        self.trade_booleans[symbol] = True
                        self.data[symbol]['trade_condition'].append(1)


                        self.trade_booleans[symbol] = True
                        self.data[symbol]['trade_condition'].append(0)


                if t - self.st > (60*15):
                    wab_api.refresh_token_auth()
                    self.st = time.time()
                else:
                    pass


                time.sleep(1)


    def account_orders(self):


        while True:
            time.sleep(1)

            order_data = wab_api.get_orders(type='WORKING', from_time=pst)

            while order_data is None:
                order_data = wab_api.get_orders(type='WORKING', from_time=pst)

            self.open_order_stocks = []
            self.orders_by_symbol = {}
            for order in order_data:
                try:
                    #print(order)
                    if 'orderLegCollection' in order:

                        orderLegCollection = order['orderLegCollection'][0]
                        symbol = orderLegCollection['instrument']['symbol']
                        buysell = orderLegCollection['instruction']
                        self.orders_by_symbol[symbol] = {}

                        self.open_order_stocks.append(symbol)

                        price = order['price']
                        oid = order['orderId']
                        self.orders_by_symbol[symbol]['instruction']= buysell
                        self.orders_by_symbol[symbol]['price']= price
                        self.orders_by_symbol[symbol]['orderId']= oid


                    elif 'childOrderStrategies' in order:

                        orderLegCollection = order['childOrderStrategies'][0]['orderLegCollection'][0]
                        symbol = orderLegCollection['instrument']['symbol']

                        self.open_order_stocks.append(symbol)

                    elif 'instrument' in order:
                        symbol = order['instrument']['symbol']
                        self.open_order_stocks.append(symbol)

                except Exception as error:

                    print('error')
                    print(error)
                    print(order)
                    pass





    def trade(self):

        while True:
            time.sleep(5)


            print('running trade')
            stocks_list = [stock.strip() for stock in self.stocks.split(',')]
            for symbol in stocks_list:

                if self.orders_by_symbol:

                    if self.data[symbol]['bid'] > (self.orders_by_symbol[symbol]['price'] + 0.2):
                        wab_api.del_order(order_id=self.orders_by_symbol[symbol]['orderId'])
                    else:
                        pass

                if self.trade_booleans[symbol] and (symbol not in self.open_order_stocks):

                    if symbol in self.orders_by_symbol:
                        pass
                    else:


                        bid = self.data[symbol]['bid']
                        ask = self.data[symbol]['ask']

                        bid_size = self.data[symbol]['quote']['bidSize']
                        ask_size = self.data[symbol]['quote']['askSize']

                        def get_purchase_and_sale():

                            weight = bid_size / (bid_size + ask_size)


                            mm = bid + ((ask - bid) * weight)



                            purchase = round(mm - 0.02, 2)

                            sale = round(mm + 0.02, 2)

                            return purchase, sale

                        purchase, sale = get_purchase_and_sale()




'''
if __name__ == '__main__':

    # Create an instance of DataCollector

    try:
    
        wab_api.refresh_token_auth()
        data_collector = DataCollector(stocks='AMD')
        
        thread1 = threading.Thread(target=data_collector.collect_data)
        thread2 = threading.Thread(target=data_collector.trade)
        thread3 = threading.Thread(target=data_collector.account_orders)

        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()
        
        # Wait for both threads to complete
        thread1.join()
        thread2.join()
        thread3.join()


    except KeyboardInterrupt:
        print(data_collector.data)

        plt.plot(data_collector.data['AMD']['bid_delta_smooth'])
        plt.show()
        print('ran')

'''


wab_api.refresh_token_auth()
start = True
stocks = ['AVGO', 'INTU', 'KLAC','NVDA', 'TMO', 'CMG', 'NFLX', 'GWW', 'NOC', 'DE', 'BLK',
          'AMP', 'LIN', 'HD', 'MSI', 'CAT', 'LLY', 'LMT', 'COST', 'ULTA', 'URI', 'ORLY']

random.shuffle(stocks)
#NOW

for stock in stocks:

    cycle_start_time = time.time()

    while True:
        symbol = stock
        positions = wab_api.get_positions()

        try:
            pos_data = positions[0]['securitiesAccount']['positions']
        except KeyError:
            pos_data = []
            pass

        position_tickers = []
        for product_position_dict in pos_data:
            ticker = product_position_dict['instrument']['symbol']
            amount = product_position_dict['longQuantity']
            position_tickers.append(ticker)

        order_data = wab_api.get_orders(from_time=pst, type='WORKING')

        while order_data is None:
            order_data = wab_api.get_orders(type='WORKING', from_time=pst)

        order_by_symbol = {}
        for order in order_data:
            try:
                olc = order['orderLegCollection']
                symbol = olc[0]['instrument']['symbol']
                order_id = order['orderId']
                instruction = olc[0]['instruction']

                order_by_symbol[symbol] = {}
                order_by_symbol[symbol]['OID'] = order_id
                order_by_symbol[symbol]['INSTRUC'] = instruction

            except Exception as error:
                print(error)

        quote = wab_api.quote_data(stocks=symbol)

        while quote is None:
            quote = wab_api.quote_data(stocks=symbol)

        bid = quote[symbol]['quote']['bidPrice']
        ask = quote[symbol]['quote']['askPrice']

        bid_size = quote[symbol]['quote']['bidSize']
        ask_size = quote[symbol]['quote']['askSize']

        def get_purchase_and_sale():

            if bid < 600:
                fee_adjustment = 2

            elif bid < 1000:
                fee_adjustment = 3
            elif bid < 2000:
                fee_adjustment = 4

            elif bid < 5000:
                fee_adjustment = 5
            else:
                fee_adjustment = 1

            weight = bid_size / (bid_size+ask_size)

            mm = bid + ((ask- bid)* weight)

            print(weight)

            print(mm)

            purchase = round(mm- (0.01*fee_adjustment), 2)

            sale = round(mm  + (0.01 * fee_adjustment), 2)

            return purchase, sale

        if start:
            sent_order = False
            start = False

        if symbol not in position_tickers and sent_order is False:
            purchase, sale = get_purchase_and_sale()
            wab_api.limit_order(symbol=symbol, price=purchase, amount=1, buysell='BUY')
            sent_order = True
            print('order purchase price')
            print(purchase)
            print('order sale price')
            print(sale)

        elif symbol in position_tickers and sent_order is True:

            print('plalce sell order sale price')
            print(sale)
            wab_api.limit_order(symbol=symbol, price=sale, amount=1, buysell='SELL')
            sent_order = False
            break

        else:
            if time.time() - cycle_start_time > 60:

                current_buying_order_id = order_by_symbol[symbol]['OID']
                if order_by_symbol[symbol]['INSTRUC'] == 'BUY':

                    wab_api.del_order(order_id=current_buying_order_id)
                else:
                    pass

                sent_order = False
                break
            else:

                pass

        time.sleep(1)

    time.sleep(30)



