from testing import SWclient
import testing
import datetime
import time
import matplotlib.pyplot as plt
import asyncio
import concurrent.futures

X = SWclient()

def run_strt():

    pst = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'


    def test_functions(stock_list, stock_str):

        data = X.quote_data(stocks=stock_str)
        sum_price = 0
        param_bundles = {}

        positions = X.get_positions()
        try:
            subset_data = positions[0]['securitiesAccount']['positions']
        except KeyError:
            subset_data = []
            pass

        position_tickers = []
        for product_position_dict in subset_data:
            ticker = product_position_dict['instrument']['symbol']
            position_tickers.append(ticker)


        for ticker in stock_list:
            if (ticker in position_tickers) or (open_order_dict[ticker] is True):
                pass
            else:



                bid = data[ticker]['quote']['bidPrice']
                ask= data[ticker]['quote']['askPrice']
                weight = (float(data[ticker]['quote']['lastPrice']) - float(bid)) / (float(ask) - float(bid))

                mid_price= (float(bid) + float(ask))/2

                mid_buy = round(float(bid) + ((mid_price - float(bid))/2), 2)
                mid_sell = round((float(ask) - ((float(ask) - mid_price))/2), 2)

                sum_price += mid_buy

                #round(mid_buy + 0.01, 2)
                mod_bid = round(float(bid) - 0.02, 2)
                mod_ask = round(float(ask) + 0.01, 2)


                '''print(ask)
                print('-----')
                print(mid_sell)
                print(mid_buy)
                print('-----')
                print(bid)
                print('weight = ' + str(weight))'''

                #X.conditional_order(price=[mod_bid, mid_sell], buysell=['BUY', 'SELL'], amount=[1, 1], symbol=[ticker, ticker])
                '''if (float(ask)- float(bid)) >= 0.03:


                    param_bundles[ticker] = {}
                    param_bundles[ticker]['price'] = [mid_buy, mid_sell]
                    param_bundles[ticker]['buysell'] = ['BUY', 'SELL']
                    param_bundles[ticker]['amount'] = [1, 1]
                    param_bundles[ticker]['symbol'] = [ticker, ticker]
                    param_bundles[ticker]['stop'] = [round(float(bid) - 0.01, 2)]
                else:
                    print('spread too small')
                    pass'''

                param_bundles[ticker] = {}
                param_bundles[ticker]['price'] = [mid_buy, mid_sell]
                param_bundles[ticker]['buysell'] = ['BUY', 'SELL']
                param_bundles[ticker]['amount'] = [1, 1]
                param_bundles[ticker]['symbol'] = [ticker, ticker]
                param_bundles[ticker]['stop'] = [round(float(bid) - 0.03, 2)]


        print('Market ordering value : ' + str(sum_price) + '$')

        return param_bundles


    def c_data():

        weights = []
        bids = []
        asks = []
        for i in range(0,1600):


            data = X.quote_data(stocks='NFLX')
            ticker = 'NFLX'

            bid = data[ticker]['quote']['bidPrice']
            ask = data[ticker]['quote']['askPrice']
            weight = (float(data[ticker]['quote']['lastPrice']) - float(bid)) / (float(ask) - float(bid))
            if (weight < 0) or (weight > 1):
                pass
            else:

                weights.append(weight)
            bids.append(bid)
            asks.append(ask)

            time.sleep(1)

        print(weights)
        print(bids)
        print(asks)

        return weights


    def create_stock_list_str(stocks):
        final_str = ''
        for ticker in stocks:
            final_str += ticker + ', '

        return final_str.rstrip(', ')


    pst = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'

    def liquidate(stocks, stock_str):


        sum_non_transacted = 0 # canceleed orders or market sold orders
        quote_data = X.quote_data(stocks=stock_str)


        data = X.get_orders(type='WORKING', from_time=pst)
        print(data)
        order_IDs = []

        if not data:
            for symbol in stocks:
                open_order_dict[symbol] = False
        else:

            for order in data:
                try:
                    orderLegCollection = order['orderLegCollection'][0]
                    symbol = orderLegCollection['instrument']['symbol']
                    strat = order['orderStrategyType']
                    #print(symbol)


                    if symbol in stocks:

                        #float(quote_data[symbol]['quote']['bidPrice']) <
                        if strat == 'OCO':
                            open_order_dict[symbol] = True
                            pass
                        else:
                            if float(quote_data[symbol]['quote']['bidPrice']) > (float(order['price']) + 0.05):
                                order_IDs.append(order['orderId'])
                                sum_non_transacted +=1
                                open_order_dict[symbol] = False
                            else:
                                open_order_dict[symbol] = True
                                pass

                        pass
                    else:
                        pass
                except KeyError:
                    pass

            async def func_cancel_order(OID):

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    loop = asyncio.get_event_loop()
                    # Use loop.run_in_executor to run blocking call in separate thread pool
                    await loop.run_in_executor(executor, X.del_order,
                                               OID)
                await asyncio.sleep(1)

            async def main_cancel_order():
                # Create tasks

                tasks = []
                for OID in order_IDs:

                    task = asyncio.create_task(func_cancel_order(OID))
                    tasks.append(task)
                # Wait for all tasks to complete
                await asyncio.gather(*tasks)

            if __name__ == "__main__":
                asyncio.run(main_cancel_order())

            print('Total Unfinished Orders : '+ str(sum_non_transacted))




    stocks = ['TSLA']
    open_order_dict = {}

    ss = create_stock_list_str(stocks)


    t = time.time()
    liquidate(stocks=stocks, stock_str=ss)
    params = test_functions(stock_list=stocks, stock_str=ss)
    if not params:
        print('No Params')
        pass
    else:

        print(params)


        async def func_s(p, ticker):
            data = p[ticker]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                loop = asyncio.get_event_loop()
                # Use loop.run_in_executor to run blocking call in separate thread pool
                await loop.run_in_executor(executor, X.conditional_oco_order,
                                           data['price'], data['buysell'], data['amount'],
                                           [ticker, ticker],
                                           data['stop'])
            await asyncio.sleep(1)


        async def main():
            # Create tasks

            tasks = []
            for tick in stocks:

                task = asyncio.create_task(func_s(params, tick))
                tasks.append(task)
            # Wait for all tasks to complete
            await asyncio.gather(*tasks)


        if __name__ == "__main__":
            asyncio.run(main())


        print(time.time() - t)
        time.sleep(1)

        t = time.time()

        liquidate(stocks=stocks, stock_str=ss)
        print('Post Liquidation Fx')
        print(time.time() - t)


ref_tt = time.time()
#X.refresh_token_auth()
'''while True:

    run_strt()
    time.sleep(30)

    if time.time() - ref_tt > 900:
        #X.refresh_token_auth()
        ref_tt = time.time()'''

pst = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'

X.refresh_token_auth()
while True:

    stocks = ['AMD', 'TSLA', 'MSFT', 'AAPL', 'AMZN', 'ORCL', 'META']
    ticker = 'NFLX'

    data = X.get_orders(type='WORKING', from_time=pst)
    order_IDs = []

    def trade():

        quote_data = X.quote_data(stocks=ticker)
        print(quote_data)
        bid = quote_data[ticker]['quote']['bidPrice']
        ask = quote_data[ticker]['quote']['askPrice']
        spread = ask - bid
        mm = round((bid + ask) / 2, 2)

        mb = round((bid + (spread / 4)), 2)

        #if (ask - bid) >= 0.03:

        '''X.conditional_order(price=[mb, mm],
                            amount=[1, 1],
                            buysell=['BUY', 'SELL'],
                            symbol=[ticker, ticker])  '''


    if not data:

        trade()

    else:
        pass



    #else:
    #print(str(round(ask - bid, 2)) + str(' Spread Too Small'))

    time.sleep(3)



# parameters of variation
# stop loss
# spread capture
# time until check liquidation
# time until next trade
# spread size for trade to start
# upward drift before cancel



# limit order works on fill or kill