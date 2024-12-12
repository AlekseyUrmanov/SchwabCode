from testing import SWclient
import datetime
import time


X = SWclient()
X.refresh_token_auth()


start_time = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'


# stock, expire_date, strike, sell_call

def order_iteration(stock_ticker, expire_date, direction, option_code, call_or_put, strike):


    data = X.option_chain(stock=stock_ticker)

    if call_or_put == 'call':

        q_bid = data['callExpDateMap'][expire_date][strike][0]['bid']
        q_ask = data['callExpDateMap'][expire_date][strike][0]['ask']

        target_price = q_bid + 0.01
        order_price = q_ask - 0.01
    else:

        q_bid = data['putExpDateMap'][expire_date][strike][0]['bid']
        q_ask = data['putExpDateMap'][expire_date][strike][0]['ask']

        target_price = q_ask + 0.01
        order_price = q_bid - 0.01


    interval = 0.01
    code = option_code

    sell_or_buy = 'SELL'
    sell_or_buy = direction


    while True:
        if sell_or_buy == 'BUY':

            if order_price > target_price:
                break
        else:
            if order_price < target_price:
                print('price diff')
                break

        i = 'BUY_TO_OPEN' if sell_or_buy == 'BUY' else 'SELL_TO_OPEN' #TODO CHNAGE THIS TO SELL_TO_CLOSE WHEN DONE
        X.option_order(price=str(round(order_price, 2)), symbol=code, instruction=i)
        time.sleep(2)

        order_Data = X.get_orders(type='WORKING', from_time=start_time)
        if len(order_Data) == 0:
            print('no order data')
            break

        oid = None
        for order in order_Data:

            try:

                if order['orderLegCollection'][0]['instrument']['symbol'] == code:
                    oid = order['orderId']
                    # if order exist we did not get a fill
                    X.del_order(order_id=oid)
                    if sell_or_buy == 'BUY':

                        order_price = round(float(order_price + interval),2)
                    else:
                        order_price = round(float(order_price - interval),2)

                else:
                    pass

            except Exception as error:
                pass

        if oid is None:
            print('no order id')
            break

        time.sleep(0.5)

    print('process complete')







X.market_order(symbol='NVDA',amount=100, buysell='BUY')

order_iteration(stock_ticker='NVDA', expire_date='2024-12-13:4', direction='SELL', option_code='NVDA  241213C00138000',
                call_or_put='call', strike='138.0')

order_iteration(stock_ticker='NVDA', expire_date='2024-12-13:4', direction='BUY', option_code='NVDA  241213P00138000',
                call_or_put='put', strike='138.0')
