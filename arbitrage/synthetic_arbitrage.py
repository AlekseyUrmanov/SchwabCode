from testing import SWclient
import time
import tqdm

X = SWclient()
X.refresh_token_auth()

winners = {}




top_sp500_tickers = [
  "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM", "V",
  "JNJ", "UNH", "PG", "HD", "DIS", "PYPL", "VZ", "NFLX", "INTC", "CMCSA",
  "PEP", "NKE", "T", "MRK", "CSCO", "PFE", "ADBE", "XOM", "TMO", "IBM",
  "AVGO", "WMT", "QCOM", "CRM", "LLY", "TXN", "MDT", "HON", "AMGN",
  "COST", "AMAT", "NOW", "LMT", "INTU", "ISRG", "SBUX", "CAT", "NKE", "TGT"]

top_sp500_tickers = ['MSFT', 'AMZN', 'AAPL', 'TSLA',
                     'SPY', 'JNJ', 'INTC',
                     'NVDA', 'GOOGL', 'GOOG', 'AMD',
                     'MU', 'KO', 'PEP', 'BAC',
                     'JPM', 'NFLX', 'XOM', 'CVX', 'UBER', 'PYPL', 'CBOE', 'DOW', 'UBER']
api_call_data = {}

#X.market_order(symbol='GOOGL', buysell='BUY', amount=100)
#X.option_order(price=None, symbol='GOOGL 241206C00170000', otype='MARKET', instruction='SELL_TO_OPEN')
#X.option_order(price=None, symbol='GOOGL 241206P00170000', otype='MARKET', instruction='BUY_TO_OPEN')

while True:



    for stock in tqdm.tqdm(top_sp500_tickers, desc = 'processing'):

        try:
            winners[stock] = []

            analysis_start_time = time.time()
            chain = X.option_chain(stock=stock)

            api_call_data[stock] = chain

            call_map = chain['callExpDateMap']

            put_map = chain['putExpDateMap']

            dates = list(put_map.keys())

            #dates = ['2024-11-15:4']
            for date in dates:
                #print(date)

                strikes_put = list(put_map[date].keys())
                strikes_call = list(call_map[date].keys())

                strikes = list(set(strikes_call) & set(strikes_put))

                #strikes = ['591.0']
                for strike in strikes:

                    call_sell_price = call_map[date][strike][0]['bid']

                    call_intrinsic = call_map[date][strike][0]['intrinsicValue']

                    put_intrinsic = put_map[date][strike][0]['intrinsicValue']

                    put_buy_price = put_map[date][strike][0]['ask']
                    itm = call_map[date][strike][0]['inTheMoney']

                    spread_adj = round((call_map[date][strike][0]['ask'] - call_map[date][strike][0]['bid']) / 2, 2)

                    if itm:
                        market_price = float(call_intrinsic) + float(strike)
                        profit = round(call_sell_price - put_buy_price - call_intrinsic, 2)
                        fee = 0.013 + (0.000027 * float(market_price))
                        # profit += spread_adj
                        profit = round(profit - fee, 2)

                    else:
                        market_price = float(strike) - float(put_intrinsic)
                        profit = call_sell_price - put_buy_price + put_intrinsic
                        fee = 0.013 + (0.000027*float(market_price))
                        #profit += spread_adj
                        profit = round(profit - fee, 2)


                    if (profit > 0) and (put_buy_price > 0) and (call_sell_price > 0):
                        days_until_expire = int(date.split(':')[1]) + 1
                        annual_yield = round(((365/days_until_expire) * (profit/market_price)) * 100, 2)
                        if annual_yield < 4.5:
                            pass
                        else:

                            winners[stock].append({'date': date, 'strike_price': strike, 'profit': profit, 'yield': annual_yield,
                                                   'mp': round(float(market_price)*100, 2),
                                                   'actual_yield': round((profit/float(market_price)) * 100, 2),
                                                   'spread_adjustment': spread_adj})


        except Exception as e:
            print(e)
            pass

        #X.market_order(symbol='PYPL', buysell='BUY', amount=100)
        #X.option_order(price=None, symbol='PYPL  241108C00077000', otype='MARKET', instruction='SELL_TO_OPEN')
        #X.option_order(price=None, symbol='PYPL  241108P00077000', otype='MARKET', instruction='BUY_TO_OPEN')

        # 'KO    2411015P00073000'

        #time.sleep(0.5)

    yield_sort = []

    for stock in winners:

        data = winners[stock]

        max_per_stock = []
        for entry in data:
            y = entry['yield']
            row = (y, entry['date'], entry['strike_price'], stock, entry['profit'], entry['mp'], entry['actual_yield'],
                   entry['spread_adjustment'])
            max_per_stock.append(row)

        sorted_max_per_stock = sorted(max_per_stock, key=lambda x: x[0], reverse=True)
        top_three = sorted_max_per_stock[0:3]

        for i in top_three:
            yield_sort.append(i)

    synthetic_shorts = sorted(yield_sort, key=lambda x: x[0], reverse=False)

    density = []
    for i in synthetic_shorts:

        density.append(i[0])
        print(i)

    time.sleep(1)




# [0.05, 0.05, 0.07, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.06, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.06, 0.05, 0.05, 0.06, 0.06, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.05, 0.06, 0.06, 0.06, 0.05, 0.05, 0.06, 0.05, 0.05, 0.05, 0.07, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.06, 0.05]

# [0.04, 0.04, 0.04, 0.06, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.04, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.07, 0.07, 0.07, 0.07, 0.07, 0.08, 0.06, 0.06, 0.06, 0.07, 0.04, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.06, 0.06, 0.05, 0.06, 0.06, 0.05, 0.05, 0.05, 0.06, 0.03, 0.04, 0.05, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.04, 0.05, 0.05, 0.05, 0.06, 0.03, 0.04, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.04, 0.04, 0.03, 0.04, 0.04, 0.04, 0.04, 0.04, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.06, 0.06, 0.07, 0.07, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.03, 0.04, 0.06, 0.05, 0.05, 0.06, 0.06, 0.05, 0.05, 0.05, 0.04, 0.05, 0.05, 0.04, 0.04, 0.04, 0.05, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.05, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.03, 0.04, 0.04, 0.05, 0.05, 0.06, 0.05, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.06, 0.07, 0.07, 0.07, 0.06, 0.06, 0.05, 0.06]

