import base64
import json
import time
import numpy as np
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import math as m
from scipy.signal import argrelextrema


class SWclient:

    def __init__(self):

        self.refresh_token = ''
        self.authorization_token = ''
        self.account_hash_num = ''
        
    def quote_data(self, stocks):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token,
        }

        params = {
            'symbols': stocks, # 'NFLX, COST, TSLA, NVDA, HD, LLY' comma separated string
            'fields': 'quote',
            'indicative': 'false',
        }

        try:

            response = requests.get('https://api.schwabapi.com/marketdata/v1/quotes', params=params, headers=headers)

            return response.json()

        except Exception as error:
            print(error)
            return None


    def limit_order(self, symbol, price, amount, buysell):

        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': 'DAY',
            'price': price, #string
            'orderStrategyType': 'SINGLE',
            #"destinationLinkName": "NASDAQ",
            #'requestedDestination': "NSDQ",
            'orderLegCollection': [
                {
                    'instruction': buysell,  # string
                    'quantity': amount,  # int
                    'instrument': {
                        'symbol': symbol,  # string
                        'assetType': 'EQUITY',
                    },
                },
            ],
        }

        response = requests.post(
            'https://api.schwabapi.com/trader/v1/accounts/'+self.account_hash_num+'/orders',
            headers=headers,
            json=json_data,
        )
        print(response.content)

    def get_orders(self, type, from_time): # FILLED or WORKING

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token
        }


        TO = str( datetime.datetime.now().isoformat())[0:-3] + 'Z'

        params = {
            'fromEnteredTime': from_time, #(datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(minutes=420)).isoformat(),
            'toEnteredTime': '2024-06-20T09:46:33.027Z', #(datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes=5)).isoformat(),
            'status': type,
        }

        try:

            response = requests.get(
                'https://api.schwabapi.com/trader/v1/accounts/'+self.account_hash_num+'/orders',
                params=params,
                headers=headers,
                timeout=None
            )

            return response.json()

        except Exception as error:
            print(error)
            return None




    def del_order(self, order_id): # string

        order_id = str(order_id)

        url = 'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders/' + order_id

        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token
        }

        response = requests.delete(
            url=url,
            headers=headers,
        )

        #print(response.content)


    def get_positions(self):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token
        }

        params = {
            'fields': 'positions',
        }

        response = requests.get('https://api.schwabapi.com/trader/v1/accounts', params=params, headers=headers)

        return response.json()

    def original_auth(self):

        # get link buy putting URL into google and signing in


        #put link in here
        link = 'https://127.0.0.1/?code=C0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.w_ree_ul9mugGImJluDudebO00LvWQe2LQalmwcYmt0%40&session=7ebb222a-6bb2-4ead-82e5-2133296c0682'


        code = f'{link[link.index('code=')+5:link.index('%40')]}@'


        byte_data = 'NKZXXztAlpiGiyZc44errtsrsMInsF60:YUdGqUhkkz7r7gHt'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Basic '+ str(base64.b64encode(bytes(byte_data, 'utf-8')).decode('utf-8'))
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://127.0.0.1'
        }

        response = requests.post('https://api.schwabapi.com/v1/oauth/token', data=data, headers=headers)
        dd = response.json()
        print(dd)
        at = dd['access_token']
        rt = dd['refresh_token']
        print(at) # I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.e_N-h8YbSPDlTO7XBupG-PjejThbZ8lnxoiA8Pm2eeA@
        print(rt) # lSMTBnzHeK8Nfs0JTOVCNWnlc3Zuy3Y3hLO2nrOMiGNwCwr-TAsEXyl3nzm5GSshXRBR2oJC4kozJa5Y-6jRt3rRRQP419_g
        return response.json()

    def refresh_token_auth(self):
        #post

        byte_data = 'NKZXXztAlpiGiyZc44errtsrsMInsF60:YUdGqUhkkz7r7gHt'
        headers = {
            'accept': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + str(base64.b64encode(bytes(byte_data, 'utf-8')).decode('utf-8'))
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'redirect_uri': 'https://127.0.0.1'
        }

        response = requests.post('https://api.schwabapi.com/v1/oauth/token', data=data, headers=headers)
        response_dictionary = response.json()
        print(response_dictionary)
        self.authorization_token = 'Bearer '+ str(response_dictionary['access_token'])

    def acc_nums(self):
        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token
        }

        response = requests.get('https://api.schwabapi.com/trader/v1/accounts/accountNumbers', headers=headers)
        dd = response.json()
        print(dd)

    def market_order(self, symbol, buysell, amount):
        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {
            'orderType': 'MARKET',
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': buysell,  # string
                    'quantity': amount,  # int
                    'instrument': {
                        'symbol': symbol,  # string
                        'assetType': 'EQUITY',
                    },
                },
            ],
        }

        response = requests.post(
            'https://api.schwabapi.com/trader/v1/accounts/'+ self.account_hash_num+ '/orders',
            headers=headers,
            json=json_data,
        )


    def put_replace(self, order_id_replacing, price, buysell, amount, symbol, market=False):

        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        if market:
            json_data = {
                'orderType': 'MARKET',
                'session': 'NORMAL',
                'duration': 'DAY',
                'orderStrategyType': 'SINGLE',
                'orderLegCollection': [
                    {
                        'instruction': buysell,  # string
                        'quantity': amount,  # int
                        'instrument': {
                            'symbol': symbol,  # string
                            'assetType': 'EQUITY',
                        },
                    },
                ],
            }

        else:

            json_data = {
                'orderType': 'LIMIT',
                'session': 'NORMAL',
                'duration': 'DAY',
                'price': price,  # string
                'orderStrategyType': 'SINGLE',
                'orderLegCollection': [
                    {
                        'instruction': buysell,  # string
                        'quantity': amount,  # int
                        'instrument': {
                            'symbol': symbol,  # string
                            'assetType': 'EQUITY',
                        },
                    },
                ],
            }

        response = requests.put(
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders/' + str(order_id_replacing),
            headers=headers,
            json=json_data,
        )
        print(response.content)


    def conditional_order(self, price, buysell, amount, symbol):
        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': 'FILL_OR_KILL',
            'price': price[0],  # string
            'orderStrategyType': 'TRIGGER',
            'orderLegCollection': [
                {
                    'instruction': buysell[0],  # string
                    'quantity': amount[0],  # int
                    'instrument': {
                        'symbol': symbol[0],  # string
                        'assetType': 'EQUITY',
                    },
                },
            ],

            'childOrderStrategies':[

                {
                    'orderType': 'LIMIT',
                    'session': 'NORMAL',
                    'duration': 'DAY',
                    'price': price[1],  # string
                    'orderStrategyType': 'SINGLE',
                    'orderLegCollection': [
                        {
                            'instruction': buysell[1],  # string
                            'quantity': amount[1],  # int
                            'instrument': {
                                'symbol': symbol[1],  # string
                                'assetType': 'EQUITY',
                            },
                        },
                    ],

                }
            ]

        }

        response = requests.post(
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
            headers=headers,
            json=json_data,
        )
        print(response.status_code)



    def conditional_oco_order(self, price, buysell, amount, symbol, stop):

            headers = {
                'accept': '*/*',
                'Authorization': self.authorization_token,
                'Content-Type': 'application/json',
            }

            json_data = {

                'orderType': 'LIMIT',
                'session': 'NORMAL',
                'duration': 'DAY', # FILL_OR_KILL, DAY
                'price': price[0],  # string
                'orderStrategyType': 'TRIGGER',
                'orderLegCollection': [
                    {
                        'instruction': buysell[0],  # string
                        'quantity':amount[0],  # int
                        'instrument': {
                            'symbol': symbol[0],  # string
                            'assetType': 'EQUITY',
                        },
                    },
                ],

                'childOrderStrategies': [

                        {
                            "orderStrategyType": "OCO",
                            "childOrderStrategies": [
                                {
                                    "orderType": "LIMIT",
                                    "session": "NORMAL",
                                    "price": price[1],
                                    "duration": "DAY",
                                    "orderStrategyType": "SINGLE",
                                    "orderLegCollection": [
                                        {
                                            "instruction": buysell[1],
                                            "quantity": amount[1],
                                            "instrument": {
                                                "symbol": symbol[1],
                                                "assetType": "EQUITY"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "orderType": "STOP", # or stop_limit
                                    "session": "NORMAL",
                                    #"price": stop[1], # where limit order is placed || must be less than trigger
                                    "stopPrice": stop[0], # where trigger occurs
                                    "duration": "DAY",
                                    "orderStrategyType": "SINGLE",
                                    "orderLegCollection": [
                                        {
                                            "instruction": buysell[1],
                                            "quantity": amount[1],
                                            "instrument": {
                                                "symbol": symbol[1],
                                                "assetType": "EQUITY"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }

                ]

            }


            response = requests.post(
                'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
                headers=headers,
                json=json_data,
            )
            print(response.status_code)


    def get_transaction_history(self, symbol):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token
        }

        #TO = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
        start = '2024-05-23T09:30:00.000Z'
        end = '2024-06-17T09:46:33.027Z'


        #https: // api.schwabapi.com / trader / v1 / accounts / accnum / transactions?startDate = 1 & endDate = 2 & symbol = NFLX & types = TRADE

        response = requests.get(
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num +
            '/transactions?startDate='+ start+'&endDate='+end+'&symbol='+symbol+'&types=TRADE',
            #params=params,
            headers=headers,
        )

        return response.json()


    def price_history(self, ticker):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token

        }

        end_time = str(int(time.time() * 1000))
        start_time = str(int((time.time() - 600) * 1000))


        params = {
            'symbol': ticker,
            'periodType': 'day',
            'period': '10',
            'frequencyType': 'minute',
            'frequency': '1',
            'startDate': '',#start_time  #1717421400000
            'endDate': '',#end_time,
            'needExtendedHoursData': 'false',
            'needPreviousClose': 'false',
        }

        response = requests.get('https://api.schwabapi.com/marketdata/v1/pricehistory', params=params, headers=headers)
        #print(response.json())

        return response.json()



X = SWclient()
X.refresh_token_auth()
#X.original_auth()


stocks = ['INTU', 'KLAC', 'TMO', 'NFLX', 'GWW', 'NOC', 'DE', 'BLK',
          'AMP', 'LIN', 'HD', 'MSI', 'CAT', 'LLY', 'LMT', 'COST', 'ULTA', 'URI',
          'MDB', 'CRWD', 'CTAS', 'NOW', 'MCK', 'ROP', 'UNH', 'MSCI', 'VRTX', 'GS',
          'ADBE','POOL', 'AON', 'CB']

recovery_times = []


tech_stocks = ['ORCL', 'MSFT', 'AAPL', 'AMD', 'IBM', 'META', 'UBER', 'TSLA', 'AMZN', 'GOOG', 'SPOT', 'NVDA']

for stock in stocks:

    data = X.price_history(ticker=stock)['candles']

    red = 0
    green = 0

    rg_cand = []

    rg_deltas = {'r':[], 'g':[]}

    close_array = []

    for candle in data:
        if candle['close'] > candle['open']:

            green += 1
            rg_cand.append('g')
            rg_deltas['g'].append(candle['close']-candle['open'])

        elif candle['close'] < candle['open']:

            red+= 1
            rg_cand.append('r')
            rg_deltas['r'].append(candle['open']-candle['close'])

        else:
            rg_cand.append('o')
            pass

        close_array.append(candle['close'])



    mu_g = sum(rg_deltas['g']) / len(rg_deltas['g'])
    mu_r = sum(rg_deltas['r']) / len(rg_deltas['r'])

    sigma_g = (mu_g) **0.5
    sigma_r = ((mu_r) ** 0.5)/2

    rinarow = 0
    index= 0

    recovery_quantity = 0
    instances = 0

    red_candles_not_big_enough = 0
    for i in rg_cand:
        if i=='r':
            rinarow +=1
            if rinarow == 2:
                instances += 1
                price_at_index = close_array[index]
                try:

                    mx_price = max(close_array[index + 1: len(close_array)])
                except Exception:
                    break

                three_candle_data = data[index-2:index+1]

                sizes = [c['open'] - c['close'] for c in three_candle_data]
                sizes = [True if c > (sigma_r+mu_r) else False for c in sizes]

                if True in sizes:

                    if mx_price > price_at_index:

                        '''print(stock)
                        print('True')
                        print('Price went above 5 consecutive red candles')
                        print('Price choosen: ' + str(price_at_index))
                        print('Highest price after crash : ' + str(mx_price))
                        print('('+ str(index)+ '/'+ str(len(rg_cand))+ ') min')'''

                        recovery_quantity += 1
                        inner_index = 0
                        for price in close_array[index + 1: len(close_array)]:
                            if price > price_at_index:
                                # print('Time to next highest price: '+ str(inner_index)+ ' min @ ' + str(price))

                                recovery_times.append(inner_index)
                                break
                            else:
                                pass
                            inner_index += 1
                        # print()
                    else:
                        '''print(stock)
                        print('Price never above after 5 consecutive red candles')
                        print('Price choosen: '+ str(price_at_index))
                        print('Highest price after crash : '+ str(mx_price))
                        print()'''

                else:
                    red_candles_not_big_enough += 1
                    instances -=1

        else:

            rinarow =0

        index += 1
    print(stock)
    try:
        print(str(recovery_quantity) +' Recovered trades out of: '+ str(instances) +' which is '+  str(round((recovery_quantity/instances)*100, 2))+ '%')
    except Exception:
        print('0')
    print('Instances when red candles not big enough: '+ str(red_candles_not_big_enough))

    time.sleep(0.6)

plt.hist(recovery_times, bins = 25)
plt.show()
