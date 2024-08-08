from testing import SWclient
import time
import datetime

X = SWclient()

with open('rftoken.txt', 'r') as file:
    content = file.read()

X.authorization_token = content


## PARAMETERS ##
stock_to_trade = 'NVDA'
shares_to_trade = 1
trade_time_interval = 5
trade_cycles = 400
counter = 0
value_add = 0.02

program_start = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
refresh_counter = time.time()


while True:

    if time.localtime().tm_sec == 55:
        break

init_inv = 0
trial = 0
old_ap = None
while True:

    id_inv = False
    try:
        pd = X.get_positions()[0]['securitiesAccount']['positions']
    except Exception:
        print('New auth token')

        with open('rftoken.txt', 'r') as file:
            content = file.read()

        X.authorization_token = content
        pd = X.get_positions()[0]['securitiesAccount']['positions']
        pass

    print('getting positions ' + str(trial))

    for product_position_dict in pd:

        if product_position_dict['instrument']['symbol'] == stock_to_trade:
            id_inv = True
            l = product_position_dict['longQuantity']

            print('Initial inv: '+ str(init_inv)+ ' Current Inv : '+ str(l))
            if init_inv != l:
                ap = product_position_dict['averagePrice']
                value = ap

                if old_ap is None:
                    pass
                else:

                    value = ((ap*l) - (old_ap*init_inv)) / (l - init_inv)
                    print(value)
                    value = ap

                price = round(value + value_add, 2)
                X.limit_order(symbol=stock_to_trade, buysell='SELL', amount=l, price=price)
                print('sent order')

            init_inv = l
            old_ap= ap

    trial += 1
    if id_inv:
        pass
    else:
        init_inv = 0



