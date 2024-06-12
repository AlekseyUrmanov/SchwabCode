from testing import SWclient
import datetime
import time
import matplotlib.pyplot as plt
import asyncio
import concurrent.futures
import requests


X = SWclient()




def create_stock_list_str(stocks):
    final_str = ''
    for ticker in stocks:
        final_str += ticker + ', '

    return final_str.rstrip(', ')



X.refresh_token_auth()
ref_tt = time.time()

stocks_tech = ['GOOG']
               #'TSLA', 'MSFT', 'AAPL', 'AMZN', 'ORCL', 'META']

stocks_spread = ['LMT', 'NOC', 'ROP', 'BLK', 'MSI', 'POOL', 'AMP', 'INTU', 'HD', 'NFLX', 'LLY', 'GS', 'V', 'COST', 'AON', 'CAT']

low_vola = ['BAC','UBER', 'INTC', 'CSCO', 'SHOP', 'CVS','WMT', 'KO'] # KO WMT



stocks = ['NVDA']


stock_str = create_stock_list_str(stocks)
pst = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
start_time = time.time()

try:

    while True:


        def parameters(stocks_to_operate):
            quote_data = X.quote_data(stocks=stock_str)

            parameters = {}

            for symbol in stocks_to_operate:

                bid = quote_data[symbol]['quote']['bidPrice']
                ask = quote_data[symbol]['quote']['askPrice']
                ltp = quote_data[symbol]['quote']['lastPrice']

                spread = ask - bid

                '''if bid > max(stock_data[symbol]['bids'][
                             len(stock_data[symbol]['bids']) - 6:len(stock_data[symbol]['bids'])]):
                    #open_order_stocks.append(symbol)  # another way to ensure we don't quote
                    #print('not quoting local maxima')
                    pass
                elif spread > (sum(stock_data[symbol]['spreads']) / (len(stock_data[symbol]['spreads']) * 1.5)):
                    #open_order_stocks.append(symbol)  # another way to ensure we don't quote
                    #print('spread too large')
                    pass
                else:
                    pass'''

                mm = round((bid + ask) / 2, 2)
                mb = round((bid + (spread / 4)), 2)

                if bid == mb:
                    mb += 0.01
                    mb = round(mb, 2)
                elif mb >= bid + 0.03:
                    mb = round(bid + 0.02, 2)
                else:
                    pass

                print('Last Trade Price: ' + str(ltp) + ' Middle Market Price : '+ str(mm))
                if ltp < mm:
                    purchase = round(ltp,2)
                    sale = round(ltp+0.01, 2)

                    parameters[symbol] = {'price': [purchase, sale],
                                          'amount': [1, 1],
                                          'ticker': [symbol, symbol],
                                          'buysell': ['BUY', 'SELL'],
                                          'stop': [round(bid - (bid*(1/500)), 2)]}
                    print(symbol +' '+ str(parameters[symbol]))
                else:

                    pass



            return parameters

        def trade(trade_info_for_stocks):

            if trade_info_for_stocks is None:
                return

            stt = time.time()
            async def create_order(params, ticker):


                with concurrent.futures.ThreadPoolExecutor() as executor:
                    loop = asyncio.get_event_loop()
                    # Use loop.run_in_executor to run blocking call in separate thread pool
                    await loop.run_in_executor(executor, X.conditional_oco_order,
                                               params[ticker]['price'],
                                               params[ticker]['buysell'],
                                               params[ticker]['amount'],
                                               params[ticker]['ticker'],
                                               params[ticker]['stop'])

                await asyncio.sleep(1)


            async def main(para):
                # Create tasks

                tasks = []
                for tick in para.keys():
                    print(open_order_stocks)
                    if tick in open_order_stocks:
                        pass
                    else:
                        task = asyncio.create_task(create_order(para, tick))
                        tasks.append(task)

                await asyncio.gather(*tasks)

            if __name__ == "__main__":
                asyncio.run(main(trade_info_for_stocks))
            print(time.time() - stt)

            #print('Market Value Of Order Delivery: ' + str(market_value))


        order_data = X.get_orders(type='WORKING', from_time=pst)

        while order_data is None:
            order_data = X.get_orders(type='WORKING', from_time=pst)

        positions = X.get_positions()

        open_order_stocks = []

        try:
            pos_data = positions[0]['securitiesAccount']['positions']
        except KeyError:
            pos_data = []
            pass

        position_tickers = []
        for product_position_dict in pos_data:
            print(product_position_dict)
            ticker = product_position_dict['instrument']['symbol']
            amount = product_position_dict['longQuantity']
            position_tickers.append(ticker)

        #Checks open orders,if an order isopen for a stock we append it to an array and don't open another
        for order in order_data:
            try:
                print(order)
                if 'orderLegCollection' in order:

                    orderLegCollection = order['orderLegCollection'][0]
                    symbol = orderLegCollection['instrument']['symbol']

                    open_order_stocks.append(symbol)

                elif 'childOrderStrategies' in order:

                    orderLegCollection = order['childOrderStrategies'][0]['orderLegCollection'][0]
                    symbol = orderLegCollection['instrument']['symbol']

                    open_order_stocks.append(symbol)

                elif 'instrument' in order:
                    symbol = order['instrument']['symbol']
                    open_order_stocks.append(symbol)

            except KeyError:
                pass
        print('open order stocks after filtering')


        # we check our positions, if we have a position but not an order for it  we sell it bc an error must've occured
        for stock in position_tickers:
            if stock in open_order_stocks:
                pass
            else:
                X.market_order(symbol=stock, buysell='SELL', amount=1)

        # Two trial to collect data and place  orders for more accurate quote information

        print('Cycle 1')
        trade_info = parameters(stocks[0:4])
        if trade_info:
            trade(trade_info)
        '''print('Cycle 2')
        trade_info = parameters(stocks[4:8])
        trade(trade_info)
        print('Cycle 3')
        trade_info = parameters(stocks[8:12])
        trade(trade_info)
        print('Cycle 4')
        trade_info = parameters(stocks[12:16])
        trade(trade_info)
'''


        # new refresh token every 15 minutes
        if time.time() - ref_tt > 900:
            X.refresh_token_auth()
            ref_tt = time.time()

        # run the whole fx again every 10 seconds
        time.sleep(10)

except KeyboardInterrupt:
    print('done')





# parameters of variation
# stop loss
# spread capture
# time until check liquidation
# time until next trade
# spread size for trade to start
# upward drift before cancel

# big loss on tsla bc spread was 8 cents


# limit order works on fill or kill