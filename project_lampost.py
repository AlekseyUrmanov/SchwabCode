import testing as charles_schwab_api_wrapper
import time
import random
import datetime
import threading


wab_api = charles_schwab_api_wrapper.SWclient()
wab_api.refresh_token_auth()

pst = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
program_start_time = time.time()

stock_shares = 1

start = True
stocks = ['KLAC', 'TMO', 'NFLX', 'DE', 'BLK',
          'AMP', 'LIN', 'HD', 'MSI', 'CAT', 'LLY', 'LMT', 'COST', 'ULTA', 'URI',
          'CRWD', 'CTAS', 'NOW', 'MCK', 'ROP', 'UNH', 'VRTX', 'GS',
          'ADBE','POOL', 'AON', 'CB', 'NOC', 'GWW', 'MSCI']
# INTU GWW MDB MSCI

over_1k_stocks = ['LRCX', 'ASML', 'ORLY', 'REGN', 'DECK', 'FICO', 'AVGO', 'TDG', 'MTD', 'MSTR', 'MELI']

more_stocks = ['CSL', 'IT', 'DPZ', 'WSO', 'MLM', 'SAIA',
               'PH', 'ELV', 'SPGI', 'WING', 'SNPS', 'HUBS', 'MCO']
# 32 + 13 + 12 = 45 w/o 1k stocks

tech = ['ORCL', 'MSFT', 'AAPL', 'AMD', 'IBM', 'META', 'UBER', 'TSLA', 'AMZN', 'GOOG', 'SPOT', 'NVDA']


def main_trading_fx():

    program_start_time = time.time()
    start = True

    while True:
        run = 0

        for stock in stocks:
            sleep_time = 10  # sec

            cycle_start_time = time.time()

            # Checking refresh token life

            if cycle_start_time - program_start_time > (60*15):
                wab_api.refresh_token_auth()
                program_start_time = time.time()
            else:
                pass

            # --------------------------------------------------------------------------------
            loop_counter = 0
            while True:
                symbol = stock

                # Grabbing Position Data

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

                # ----------------------------------------------------------------------------

                # Get Order Data

                order_data = wab_api.get_orders(from_time=pst, type='WORKING')

                while order_data is None:
                    order_data = wab_api.get_orders(type='WORKING', from_time=pst)

                order_by_symbol = {}
                for order in order_data:
                    try:
                        olc = order['orderLegCollection']
                        ticker = olc[0]['instrument']['symbol']
                        order_id = order['orderId']
                        instruction = olc[0]['instruction']

                        order_by_symbol[ticker] = {}
                        order_by_symbol[ticker]['OID'] = order_id
                        order_by_symbol[ticker]['INSTRUC'] = instruction

                    except Exception as error:
                        print(error)

                # ----------------------------------------------------------------------------

                # Get Historical Pricing
                if loop_counter >0:
                    # we only check for a local max once, right before we place a buy order
                    pass
                else:

                    data = (wab_api.price_history(ticker=symbol))['candles'][-6:-1]
                    price_array = []
                    current_candle = (wab_api.price_history(ticker=symbol))['candles'][-1]
                    max_array = []

                    for candle in data:

                        close = candle['close']
                        open = candle['open']
                        max_array.append(close)
                        price_array.append('r' if close < open else 'g')


                    if current_candle['close'] > max(max_array):
                        break
                        sleep_time = 1
                    else:

                        if price_array.count('r') > 3:

                            pass
                        else:
                            break
                            sleep_time = 1

                # ----------------------------------------------------------------------------------

                # Get quote Data

                quote = wab_api.quote_data(stocks=symbol)

                while quote is None:
                    quote = wab_api.quote_data(stocks=symbol)

                bid = quote[symbol]['quote']['bidPrice']
                ask = quote[symbol]['quote']['askPrice']

                bid_size = quote[symbol]['quote']['bidSize']
                ask_size = quote[symbol]['quote']['askSize']



                # ---------------------------------------------------------------------------------------

                # Pricing And Trading Logic

                def get_purchase_and_sale():

                    if bid < 300:
                        fee_adjustment = 2

                    elif bid < 600:
                        fee_adjustment = 3

                    elif bid < 1000:
                        fee_adjustment = 4

                    elif bid < 2000:
                        fee_adjustment = 5

                    elif bid < 5000:
                        fee_adjustment = 10
                    else:
                        fee_adjustment = 1

                    weight = bid_size / (bid_size+ask_size)

                    print('weight')
                    print(weight)
                    if weight > 0.5:
                        weight = 1 - weight

                    mm = bid + ((ask- bid)* weight)

                    reference_bid = bid

                    purchase = round(mm - (0.01*fee_adjustment), 2)

                    sale = round(mm + (0.01 * fee_adjustment), 2)

                    return purchase, sale, reference_bid

                if start:
                    sent_order = False
                    start = False

                # TODO should be == 0 bc the loop counter is default to 0

                '''if loop_counter == 1: # If we cancel buy order but it gets executed
                    if symbol in position_tickers:
                        # Will cause to place a sell order
                        sent_order = True'''

                if (symbol not in position_tickers) and sent_order is False:
                    purchase, sale, reference_bid = get_purchase_and_sale()
                    wab_api.limit_order(symbol=symbol, price=purchase, amount=stock_shares, buysell='BUY')
                    sent_order = True
                    print('buying ' + str(purchase))

                elif (symbol in position_tickers) and sent_order is True:

                    print('selling '+ str(sale))
                    wab_api.limit_order(symbol=symbol, price=sale, amount=stock_shares, buysell='SELL')
                    sent_order = False
                    break

                else:
                    try:

                        if time.time() - cycle_start_time > 3:

                            try:

                                current_buying_order_id = order_by_symbol[symbol]['OID']

                            except Exception:
                                sent_order = True
                                pass




                            if order_by_symbol[symbol]['INSTRUC'] == 'BUY':

                                if purchase - bid > purchase - reference_bid or purchase - bid  < 0:
                                    # if bid-order diatsnace inc = price is going down
                                    # else bid-order distance converges to current bid, (price going up)
                                    # until the bid-order-ref distance is negative
                                    # then 'm falling behind best bid and I can cancel order
                                    print('canceling order')
                                    wab_api.del_order(order_id=current_buying_order_id)

                                    sent_order = False
                                    sleep_time = 1
                                    break

                            else:
                                if order_by_symbol[symbol]['INSTRUC'] == 'SELL':
                                    sent_order = False

                                    break
                                else:

                                    pass

                        else:
                            pass
                    except Exception as error:
                        # most likely key error because we try to cancel an order that no longer exists
                        # we got a position fill even though we read it as position false due to time of api call


                        print('del order broken')
                        print(error)

                        pass

                loop_counter += 1

                time.sleep(1)
            run += 1
            print('run '+ str(run))
            time.sleep(sleep_time)



def get_orders_by_symbol():

    order_data = wab_api.get_orders(from_time=pst, type='WORKING')

    while order_data is None:
        order_data = wab_api.get_orders(type='WORKING', from_time=pst)

    order_by_symbol = {}
    for order in order_data:
        try:
            olc = order['orderLegCollection']
            ticker = olc[0]['instrument']['symbol']
            order_id = order['orderId']
            time_in = order['enteredTime']
            instruction = olc[0]['instruction']
            price = order['price']

            dt = datetime.datetime.strptime(time_in, '%Y-%m-%dT%H:%M:%S%z')

            # Convert the datetime object to a Unix timestamp
            unix_timestamp = int(dt.timestamp())

            order_by_symbol[ticker] = {}
            order_by_symbol[ticker]['OID'] = order_id
            order_by_symbol[ticker]['INSTRUC'] = instruction
            order_by_symbol[ticker]['PRICE'] = price
            order_by_symbol[ticker]['TIMEOPEN'] = unix_timestamp

        except Exception as error:
            print('get orders breaking')
            print(order_data)
            print(error)

    return order_by_symbol



def expired_positions():

    while True:

        order_by_symbol = get_orders_by_symbol()
        sell_symbols = []

        for symbol in order_by_symbol:

            if order_by_symbol[symbol]['INSTRUC'] == 'SELL':

                time_check = ((order_by_symbol[symbol]['PRICE'] * 0.001)**2) * 1200
                #print(time_check/60)

                if time.time() - order_by_symbol[symbol]['TIMEOPEN'] > 10:
                    sell_symbols.append(symbol)

        for symbol in sell_symbols:

            order_replace_counter = 0
            while True:

                obs = get_orders_by_symbol()

                if symbol in obs:

                    old_price = obs[symbol]['PRICE']
                    new_price = round(old_price - 0.01, 2)

                    if new_price < 300:
                        fee_adjustment = 2

                    elif new_price < 500:
                        fee_adjustment = 3

                    elif new_price < 1000:
                        fee_adjustment = 4

                    elif new_price < 2000:
                        fee_adjustment = 5

                    elif new_price < 5000:
                        fee_adjustment = 10
                    else:
                        fee_adjustment = 1


                    if int(fee_adjustment/2) == order_replace_counter:
                        # has 10 seconds to fill  at profit price
                        # sale prices decreases to break even price (-0.01) fee loss
                        # and another 10 seconds at fill there, then it continues down

                        pass
                    else:
                        pass

                    old_order_id = obs[symbol]['OID']
                    #print(obs)
                    try:

                        wab_api.put_replace(order_id_replacing=old_order_id,
                                            price=new_price,
                                            symbol=symbol,
                                            buysell='SELL',
                                            amount=stock_shares)
                        print('Replaced order ' + str(old_price)+ ' --> '+ str(new_price))
                        order_replace_counter += 1
                    except Exception as error:
                        print(error)
                        print('Order got filled right before cancellation')
                        break
                else:
                    break

        time.sleep(1)


if __name__ == '__main__':

    thread1 = threading.Thread(target=main_trading_fx)
    thread2 = threading.Thread(target=expired_positions)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()

#TODO loop counter adjusted to 0 again
#TODO test the quick selling down method
#TODO test the 3 red candles
#TODO test the quoteing while order open to see what is changing

