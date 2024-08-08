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
trade_cycles = 1600
counter = 0

program_start = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
while True:

    if time.localtime().tm_sec == 59:
        break


print('started')

#d= X.get_orders(from_time=program_start, type='FILLED')
#print(d)

ref_pl = 0
twy_condition = False
old_inv = 0
for i in range(trade_cycles):

    process_start_time = time.time()

    pd = X.get_positions()[0]['securitiesAccount']['positions']
    l = 0
    new_pl = 0
    for product_position_dict in pd:

        if product_position_dict['instrument']['symbol'] == stock_to_trade:
            l = product_position_dict['longQuantity']
            old_ap = product_position_dict['averagePrice']
            s = product_position_dict['shortQuantity']
            new_pl = product_position_dict['currentDayProfitLoss']

        else:
            pass

    if l > 0 and l <14:
        # (ref_pl - new_pl) > (0.02*l)
        twy_condition = False
        loss = (ref_pl - new_pl)


        print('ref pl: '+ str(ref_pl)+ ' loss: '+ str(loss))

        if loss <= 0.02:

            pass
        elif loss <= 0.05:
            earn_back = 3

            X.market_order(symbol=stock_to_trade, buysell='BUY', amount=earn_back)
            print(time.time())

        elif loss >= 0.20:

            earn_back = 10

            X.market_order(symbol=stock_to_trade, buysell='BUY', amount=earn_back)
            print(time.time())
        else:
            pass


        old_inv = l

    elif l ==0:
        X.market_order(symbol=stock_to_trade, buysell='BUY', amount=shares_to_trade)
        twy_condition = False
        print(time.time())

        pd = X.get_positions()[0]['securitiesAccount']['positions']

        for product_position_dict in pd:

            if product_position_dict['instrument']['symbol'] == stock_to_trade:
                pl = product_position_dict['currentDayProfitLoss']

        ref_pl = pl

        old_inv = 0

    else:

        if twy_condition:
            #X.market_order(symbol=stock_to_trade, buysell='SELL', amount=l)
            twy_condition = False
        else:
            #time.sleep(60)
            twy_condition = True

        pass



    if i%(int(900/trade_time_interval)) == 0:
        with open('rftoken.txt', 'r') as file:
            content = file.read()

        X.authorization_token = content


    time_took = time.time() - process_start_time
    #print(time_took)

    try:
        time.sleep(trade_time_interval - time_took)
    except Exception:
        pass
    counter += 1

