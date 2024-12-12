import base64
import json
import time
import requests
import datetime
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
import statistics as s
import random
import tqdm
import math
import sympy as sp
import numpy as np

'''
app_key = 'NKZXXztAlpiGiyZc44errtsrsMInsF60'
sec_key = 'YUdGqUhkkz7r7gHt'


url = f'https://api.schwabapi.com/v1/oauth/authorize?client_id=NKZXXztAlpiGiyZc44errtsrsMInsF60&redirect_uri=https://127.0.0.1'
print(url)

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.tEe7I6jMs1HgsSi-TWOdIvKGOnWzCF3mzTh3oeNy8PU@',
}

params = {
    'symbols': 'NFLX, COST, TSLA, NVDA, HD, LLY',
    'fields': 'quote',
    'indicative': 'false',
}

response = requests.get('https://api.schwabapi.com/marketdata/v1/quotes', params=params, headers=headers)

print(response.json())
'''


# Account number = 69464639
# Hashed acc = 7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F


# decoded code = C0.b2F1dGgyLmZiZC5zY2h3YWIuY29t.SR_EhQPFLmE8YwBWEC04YBWClwpTDDKRxmGwEgc0yg8@


class SWclient:

    def __init__(self):

        # "accountNumber": "69464639",
        # "hashValue": "7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F"

        # 'F4CD9DB8470C0BB53D322E6157336D31D07D0D3549F8D85CFD6615E618806376' new hash value from new auth key, using own acc fx

        self.refresh_token = 'YcRlALIRUfRr2BJDV2TzPngd81eQ2XCVFOLA5B9wq5dHGiVb5UUO_L9st9D8JSoq58pzHK4ECAooMAlncIncwt1HO-VPyigtgk4m9xfKLRCj3jPILaGOD3OrNFI2-NY0kQUDlDuJqhQ@'
        self.authorization_token = 'Bearer I0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.ODFIPxGN5JChwQ1T1ddN_GAH7ev5WrvpT537qlTmDR4@'

        self.account_hash_num = 'F4CD9DB8470C0BB53D322E6157336D31D07D0D3549F8D85CFD6615E618806376'

    def quote_data(self, stocks):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token,
        }

        params = {
            'symbols': stocks,  # 'NFLX, COST, TSLA, NVDA, HD, LLY' comma separated string
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

        duration = 'DAY'
        if buysell == 'BUY':
            duration = 'DAY'

        json_data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': duration,  # FILL_OR_KILL DAY
            'price': price,  # string
            'orderStrategyType': 'SINGLE',
            # "destinationLinkName": "NASDAQ",
            # 'requestedDestination': "NSDQ",
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
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
            headers=headers,
            json=json_data,
        )
        print(response.content)

    def get_orders(self, type, from_time):  # FILLED or WORKING

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token
        }

        TO = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
        print(TO)
        params = {
            'maxResults': 100,
            'fromEnteredTime': from_time,
            # (datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(minutes=420)).isoformat(),
            'toEnteredTime': '2024-12-25T09:46:33.027Z',
            # (datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes=5)).isoformat(),
            'status': type,
        }

        try:

            response = requests.get(
                'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
                params=params,
                headers=headers,
                timeout=None
            )

            return response.json()

        except Exception as error:
            print(error)
            return None

    def del_order(self, order_id):  # string

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

        # print(response.content)

    def get_positions(self):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token
        }

        params = {
            'fields': 'positions',
        }

        response = requests.get('https://api.schwabapi.com/trader/v1/accounts', params=params, headers=headers)
        #print(response.content)
        return response.json()

    def original_auth(self):

        # get link buy putting URL into google and signing in

        # put link in here
        link = 'https://127.0.0.1/?code=C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.Qw4yTL4_Z3fJAI0fMgur_hIU3g_HquIgld8Re_a8TIY%40&session=5609f447-a6ce-4cf9-99e6-343d7ce80291'

        code = f'{link[link.index('code=') + 5:link.index('%40')]}@'

        byte_data = 'NKZXXztAlpiGiyZc44errtsrsMInsF60:YUdGqUhkkz7r7gHt'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Basic ' + str(base64.b64encode(bytes(byte_data, 'utf-8')).decode('utf-8'))
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
        print(at)  # I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.e_N-h8YbSPDlTO7XBupG-PjejThbZ8lnxoiA8Pm2eeA@
        print(rt)  # lSMTBnzHeK8Nfs0JTOVCNWnlc3Zuy3Y3hLO2nrOMiGNwCwr-TAsEXyl3nzm5GSshXRBR2oJC4kozJa5Y-6jRt3rRRQP419_g
        return response.json()

    def refresh_token_auth(self):
        # post

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
        self.authorization_token = 'Bearer ' + str(response_dictionary['access_token'])

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
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
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
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders/' + str(
                order_id_replacing),
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
            'duration': 'DAY',
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

            'childOrderStrategies': [

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


    def conditional_market_order(self, price, symbol, shares = 1):
        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': 'DAY',
            'price': price,  # string
            'orderStrategyType': 'TRIGGER',
            'orderLegCollection': [
                {
                    'instruction': 'BUY',  # string
                    'quantity': shares,  # int
                    'instrument': {
                        'symbol': symbol,  # string
                        'assetType': 'EQUITY',
                    },
                },
            ],

            'childOrderStrategies': [

                {
                    'orderType': 'MARKET',
                    'session': 'NORMAL',
                    'duration': 'DAY',
                    'orderStrategyType': 'SINGLE',
                    'orderLegCollection': [
                        {
                            'instruction': 'SELL',  # string
                            'quantity': shares,  # int
                            'instrument': {
                                'symbol': symbol,  # string
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
        print(response)

    def conditional_oco_order(self, price, buysell, amount, symbol, stop):

        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {

            'orderType': 'MARKET',
            'session': 'NORMAL',
            'duration': 'DAY',  # FILL_OR_KILL, DAY
            #'price': price[0],  # string
            'orderStrategyType': 'TRIGGER',
            'orderLegCollection': [
                {
                    'instruction': 'SELL',  # string
                    'quantity': amount[0],  # int
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
                            "price": price[0],
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
                            "orderType": "STOP",  # or stop_limit
                            "session": "NORMAL",
                            # "price": stop[1], # where limit order is placed || must be less than trigger
                            "stopPrice": stop[0],  # where trigger occurs
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

        # TO = str(datetime.datetime.now().isoformat())[0:-3] + 'Z'
        start = '2024-05-23T09:30:00.000Z'
        end = '2024-06-17T09:46:33.027Z'

        # https: // api.schwabapi.com / trader / v1 / accounts / accnum / transactions?startDate = 1 & endDate = 2 & symbol = NFLX & types = TRADE

        response = requests.get(
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num +
            '/transactions?startDate=' + start + '&endDate=' + end + '&symbol=' + symbol + '&types=TRADE',
            # params=params,
            headers=headers,
        )

        return response.json()

    def price_history(self, ticker, full_time=False):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token

        }

        end_time = str(int(time.time() * 1000))
        start_time = str(int((time.time() - 600) * 1000))

        if full_time:
            end_time = ''
            start_time = ''
        else:
            pass

        params = {
            'symbol': ticker,
            'periodType': 'day',  # day
            'period': '10',  # 10
            'frequencyType': 'minute',  # minute
            'frequency': '1',
            'startDate': start_time,  # start_time  #1717421400000
            'endDate': end_time,  # end_time,
            'needExtendedHoursData': 'false',
            'needPreviousClose': 'false',
        }
        try:

            response = requests.get('https://api.schwabapi.com/marketdata/v1/pricehistory', params=params,
                                    headers=headers)
            #print(response.json())

            return response.json()

        except Exception as error:
            print(error)
            return None

    def get_transaction_times(self, stocks):

        all_times = []

        for s in stocks:

            data = self.get_transaction_history(symbol=s)

            # print(len(data))
            old_time = None
            ids = {}
            for i in data:
                date_string = i['time']

                # Define the format string
                format_string = "%Y-%m-%dT%H:%M:%S%z"

                # Convert the string to a datetime object
                date_object = datetime.datetime.strptime(date_string, format_string)
                ids[i['orderId']] = date_object

            dates = []
            for i in sorted(ids):
                dates.append(ids[i])

            deltas = []
            for i in range(0, len(sorted(ids)), 2):

                if i + 1 < len(sorted(ids)):
                    deltas.append((dates[i + 1] - dates[i]).total_seconds())
                    all_times.append((dates[i + 1] - dates[i]).total_seconds())

                else:
                    break

            print(s + ' ' + str(deltas))
            time.sleep(1)

    def get_value_portfolio(self, str_stocks):

        data = self.quote_data(stocks=str_stocks)

        over_all_price = 0
        for symbol in data:
            inner_data = data[symbol]
            price = inner_data['quote']['bidPrice']
            over_all_price += price

        return over_all_price

    def conditional_market_order_short(self, price, symbol, shares = 1):
        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': 'DAY',
            'price': price,  # string
            'orderStrategyType': 'TRIGGER',
            'orderLegCollection': [
                {
                    'instruction': 'SELL',  # string
                    'quantity': shares,  # int
                    'instrument': {
                        'symbol': symbol,  # string
                        'assetType': 'EQUITY',
                    },
                },
            ],

            'childOrderStrategies': [

                {
                    'orderType': 'MARKET',
                    'session': 'NORMAL',
                    'duration': 'DAY',
                    'orderStrategyType': 'SINGLE',
                    'orderLegCollection': [
                        {
                            'instruction': 'BUY',  # string
                            'quantity': shares,  # int
                            'instrument': {
                                'symbol': symbol,  # string
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
        print(response)


    def trail_stop(self, symbol, offset, shares, buy_sell):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token

        }
        stop_price_basis = 'BID' if buy_sell == 'SELL' else 'ASK'

        json_data = {
            "complexOrderStrategyType": "NONE",
            "orderType": "TRAILING_STOP",
            "session": "NORMAL",
            "stopPriceLinkBasis": stop_price_basis,
            "stopPriceLinkType": "VALUE",
            "stopPriceOffset": offset,
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": buy_sell,
                    "quantity": shares,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }

        response = requests.post(
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
            headers=headers,
            json=json_data,
        )
        print(response.status_code)


    def option_chain(self, stock, itm=False):


        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token

        }

        if itm:
            r = 'ITM'
        else:
            r = 'ALL'
        params = {
                'symbol': stock,
                'contractType': 'ALL',
                'strikeCount': '8',
                'includeQuotes': 'FALSE',
                'strategy': 'SINGLE',
                'range': r
            }


        response = requests.get('https://api.schwabapi.com/marketdata/v1/chains', params=params,
                        headers=headers)

        return response.json()

    def option_order(self, price, symbol, instruction = 'BUY_TO_OPEN', otype='LIMIT'):

        # BUY_TO_OPEN  BUY_TO_CLOSE  SELL_TO_OPEN  SELL_TO_CLOSE
        # symbol is option/strike/date specific, get from data frame
        # Example : 'AOS   250417P00115000' 3 spaces
        # '2024-10-18:4': {'50.0': [{'putCall': 'CALL', 'symbol': 'AOS   241018C00050000'
        # year+month+day as ints all together
        # symbol string second part is 15 characters long
        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        if otype == 'LIMIT':

            json_data = {
                "complexOrderStrategyType": "NONE",
                "orderType": otype,
                "session": "NORMAL",
                "price": price,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": instruction,
                        "quantity": 1,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "OPTION"
                        }
                    }
                ]
            }

        else:

            json_data = {
                "complexOrderStrategyType": "NONE",
                "orderType": 'MARKET',
                "session": "NORMAL",
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": instruction,
                        "quantity": 1,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "OPTION"
                        }
                    }
                ]
            }


        response = requests.post(
            'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders',
            headers=headers,
            json=json_data,
        )




    def conditional_optionContract_marketShares_order(self, optionPrice, optionSymbol, stockShares, stockSymbol):
        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token,
            'Content-Type': 'application/json',
        }

        json_data = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": optionPrice,
            "duration": "DAY",
            "orderStrategyType": "TRIGGER",
            "orderLegCollection": [
                {
                    "instruction": 'BUY_TO_OPEN',
                    "quantity": 1,
                    "instrument": {
                        "symbol": optionSymbol,
                        "assetType": "OPTION"
                    }
                }
            ],

            'childOrderStrategies': [

                    {
                        "orderType": "LIMIT",
                        "session": "NORMAL",
                        "price": str(round((float(optionPrice)+0.02), 2)),
                        "duration": "DAY",
                        "orderStrategyType": "TRIGGER",
                        "orderLegCollection": [
                            {
                                "instruction": 'SELL_TO_CLOSE',
                                "quantity": 1,
                                "instrument": {
                                    "symbol": optionSymbol,
                                    "assetType": "OPTION"
                                }
                            }
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
        print(response)





'''
X = SWclient()


X.refresh_token_auth()


def get_values():

    data = X.option_chain(stock='M')['callExpDateMap']['2024-12-13:2']['15.5'][0]
    ask_price = data['bid']
    intrinsic_value = data['intrinsicValue']
    theory_value = data['theoreticalOptionValue']

    theory_premium = round(theory_value-intrinsic_value, 2)
    true_premium = round(ask_price - intrinsic_value, 2)

    return theory_premium, true_premium, ask_price


y1 = []
y2 = []
y3 = []
def update(f):
    thp, trp, op = get_values()

    if f%500 == 0:
        X.refresh_token_auth()


    if len(y1) > 500:
        y1.pop(0)
        y2.pop(0)
        y3.pop(0)

    y1.append(trp)
    y2.append(thp)
    y3.append(op)

    plt.clf()  # Clear the previous plot
    plt.subplot(1,2,1)
    plt.plot(y1,  color='g')
    plt.plot(y2,  color='r')
    plt.subplot(1,2,2)
    plt.plot(y3, color ='blue')
    plt.plot()



ani = FuncAnimation(plt.gcf(), update, frames=range(10000), interval=1000)
plt.show()
'''
