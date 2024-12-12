import requests
from testing import SWclient
from datetime import datetime
import tqdm



def sp500():

    headers = {
        'Accept-Language': 'en-US,en;q=0.5',

        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.slickcharts.com/sp500', headers=headers).json()

    return response

def snc(date):

    # year-mon-day
    url = 'https://api.nasdaq.com/api/calendar/dividends?date={}'.format(date)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        # Add more headers if required
    }
    response = (requests.get(url, headers=headers)).json()
    data = response["data"]['calendar']['rows']
    return data


def sort_data(data):
    sorted_data = {}
    for entry in data:
        symbol = str(entry['symbol'])
        cash_div_payment = str(entry['dividend_Rate'])
        annual_cash_div_payment = str(entry['indicated_Annual_Dividend'])
        pay_date = str(entry['payment_Date'])
        ex_date = str(entry['dividend_Ex_Date'])

        sorted_data[symbol] = {'cash': cash_div_payment, 'yearly_cash': annual_cash_div_payment, 'pay_date': pay_date,
                               'ex_date': ex_date}

    return sorted_data


def print_at_strike_data(put_data, call_data):

    print('[ '+str(call_data['bid']) + ' | ' + str(call_data['ask']) +
          '    |    ' + str(put_data['bid']) + ' | ' + str(put_data['ask']) + ' ]')


#'2024-10-16'

def dividend_mis_pricing(schwab_client, date):

    doc_data = []
    #schwab_client.refresh_token_auth()

    div_ex_date = date

    today = datetime.today().date()
    target_date = datetime(int(div_ex_date.split('-')[0]), int(div_ex_date.split('-')[1]),
                           int(div_ex_date.split('-')[2])).date()
    days_until_target = (target_date - today).days

    l = snc(div_ex_date)

    sd = sort_data(l)

    full_div_port_value = {'cost': 0, 'earnings': 0}
    #tqdm.tqdm(top_sp500_tickers, desc='processing'):
    for key in sd.keys():
        full_div_port_value['earnings'] += float(sd[key]['cash'])
        #print(key+' '+sd[key]['cash'])
        u = 0
        try:
            data = schwab_client.option_chain(stock=key, itm=True)
            if data['putExpDateMap']:

                div_amount = sd[key]['cash']

                yearly_div = sd[key]['yearly_cash']

                if int(float(yearly_div) / float(div_amount)) == 4:
                    # quarterly dividend no option adjustments
                    # print(data['putExpDateMap'])
                    for date in data['putExpDateMap']:

                        if (int(date.split(':')[1])+1) >= days_until_target:
                            option_data_for_date = data['putExpDateMap'][date]

                            for strike in option_data_for_date:

                                strike_date_option_data = option_data_for_date[strike][0]

                                if strike_date_option_data['inTheMoney']:
                                    ask_price = strike_date_option_data['ask']
                                    bid_price = strike_date_option_data['bid']
                                    # v = strike_date_option_data['volume']

                                    extra = float(strike_date_option_data['extrinsicValue'])
                                    intra = float(strike_date_option_data['intrinsicValue'])
                                    extra = round(float(ask_price) - float(intra), 2)

                                    call_premium = data['callExpDateMap'][date][strike][0]['bid']

                                    div_amount = float(div_amount)
                                    profit = round(div_amount - extra, 2)
                                    mark_price = round(float(data['underlyingPrice']), 2)
                                    if u == 0:
                                        full_div_port_value['cost'] += mark_price
                                        u = mark_price
                                    else:
                                        pass

                                    extra_bid = round(float(bid_price) - float(intra), 2)
                                    profit_at_bid = round(div_amount - extra_bid, 2)


                                    rate_of_return = (365/(int(date.split(':')[1]))) * (profit/mark_price)
                                    if profit > 0 and float(ask_price) > 0:

                                        data_base_entry = {'stock': key, 'strike': strike, 'expiration': date,
                                                           'contract_ask': str(ask_price), 'contract_bid': str(bid_price),
                                                           'intrinsic': str(intra), 'profit': str(profit),
                                                           'spread': str(round(ask_price - bid_price, 2)),
                                                           'fees': str(0.0132), 'underlyingMarketPrice': str(mark_price),
                                                           'cash_dividend': str(div_amount), 'ex_date': div_ex_date}

                                        doc_data.append(data_base_entry)

                                        print('Option ' + key + ' ' + date + ' Strike: ' + strike + ' Price : ' + str(
                                            ask_price) + ' MarketPrice: ' + str(mark_price))
                                        print('Cash Div: ' + str(div_amount) + ' Extrinsic Paid: ' + str(
                                            extra) + ' Intrinsic: ' + str(intra))
                                        print('Profit: ' + str(profit) + ' Option Spread ' + str(
                                            round(ask_price - bid_price, 2)) + ' Call Premium: '+str(call_premium)+' Rate of Return: '+str(rate_of_return))
                                        print()
                                    else:
                                        if profit >= -0.01:
                                            # print(key+ ' Profit: ' + str(profit) + ' '+ str(profit_at_bid))
                                            pass
                        else:
                            # Option chain expires too early
                            pass

                else:
                    # one time or special dividend
                    pass

            else:
                # dividend paying stock with no options chain
                pass

        except Exception as e:


            print(e)
            pass

    print(full_div_port_value)
    y = round((full_div_port_value['earnings'] / full_div_port_value['cost']) * 100, 2)
    print('yield: ' + str(y) + '%')

    return doc_data


def synthetic_div_arbitrage(schwab_client, date):
    doc_data = []
    # schwab_client.refresh_token_auth()

    div_ex_date = date

    today = datetime.today().date()
    target_date = datetime(int(div_ex_date.split('-')[0]), int(div_ex_date.split('-')[1]),
                           int(div_ex_date.split('-')[2])).date()
    days_until_target = (target_date - today).days

    l = snc(div_ex_date)

    sd = sort_data(l)


    full_div_port_value = {'cost': 0, 'earnings': 0}

    for key in sd.keys():
        full_div_port_value['earnings'] += float(sd[key]['cash'])

        try:
            data = schwab_client.option_chain(stock=key, itm=True)
            if data['putExpDateMap']:

                div_amount = sd[key]['cash']

                yearly_div = sd[key]['yearly_cash']

                if int(float(yearly_div) / float(div_amount)) == 4:

                    for date in data['putExpDateMap']:

                        if (int(date.split(':')[1]) + 1) >= days_until_target and (int(date.split(':')[1]) + 1)  <= 32:
                            put_data = data['putExpDateMap'][date]
                            call_data = data['callExpDateMap'][date]

                            for strike in put_data:

                                put_at_strike = put_data[strike][0]
                                call_at_strike = call_data[strike][0]

                                put_ask_price = put_at_strike['ask']
                                call_bid_price = call_at_strike['bid']

                                call_sym = call_at_strike['symbol']
                                put_sym = put_at_strike['symbol']

                                div_amount = float(div_amount)

                                mark_price = round(float(data['underlyingPrice']), 2)
                                strike = float(strike)

                                intrinsic_call = 0 if (mark_price - strike) <= 0 else (mark_price - strike)
                                intrinsic_put = 0 if (strike- mark_price) <= 0 else (strike - mark_price)



                                if intrinsic_call > 0:
                                    #print(call_at_strike['intrinsicValue'])
                                    profit = call_bid_price - put_ask_price - intrinsic_call + div_amount

                                    premium = round(call_bid_price - intrinsic_call, 2)

                                else:

                                    profit = call_bid_price - put_ask_price + intrinsic_put + div_amount

                                    premium = 0

                                profit -= 0.013
                                if profit >0:

                                    rr = str(round((260/(int(date.split(':')[1])+1)) * (profit/mark_price) * 100, 2))

                                    '''print('Stock: '+ str(key) + '\nProfit: '+str(round(profit, 2))+' Mark Price: ' +str(mark_price)+
                                          ' ARR: '+rr+'\nOption--> Strike: '+ str(strike) + ' DTE: '+str(int(date.split(':')[1]))+
                                          ' Div: '+str(div_amount) + ' ('+ str(div_ex_date)+')')'''

                                    #print_at_strike_data(put_at_strike, call_at_strike)

                                    row = (str(key), str(round(profit, 2)), str(mark_price),
                                          float(rr), str(strike),  str(int(date.split(':')[1])),
                                          str(div_amount), str(div_ex_date), put_at_strike, call_at_strike, premium)

                                    doc_data.append(row)
                                    #print()

        except Exception as e:
            print(e)
            pass

    return doc_data


X = SWclient()
X.refresh_token_auth()

all_data = []



for i in range(12, 32):

    j = '2024-12-'+str(i)
    try:

        sorted_doc_data= synthetic_div_arbitrage(X, date=j)
        for j in sorted_doc_data:

            all_data.append(j)

    except Exception as e:
        pass

#print(all_data)
final = sorted(all_data, key=lambda x: x[3], reverse=False)
for i in final:
    new_tuple = i
    #print(new_tuple)

    if new_tuple[10] < float(new_tuple[6]) :
        pass
    else:
        print()
        print('Stock: '+new_tuple[0]+ ' Profit: '+new_tuple[1]+' Stock Price: '+new_tuple[2]+
              ' ARR: '+str(new_tuple[3])+'%' + ' Selling Premium: ' +str(new_tuple[10])+'\n'+
              'Strike: '+new_tuple[4]+' DTE: '+new_tuple[5]+ ' Dividend/Share: '+new_tuple[6]+ ' ExDate: '+new_tuple[7]+
              ' CallCode: '+i[9]['symbol'])

        print_at_strike_data(i[8], i[9])




