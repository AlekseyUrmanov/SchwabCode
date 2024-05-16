import json
import requests
import pandas as pd

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


def schwab_market_order(symbol, buysell, amount):
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.mpNzVyYl3_ahFXScoUQn0IbhepS7S8rlZh-zO_zYKNU@',
        'Content-Type': 'application/json',
    }

    json_data = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': buysell, #string
                'quantity': amount, #int
                'instrument': {
                    'symbol': symbol, #string
                    'assetType': 'EQUITY',
                },
            },
        ],
    }

    response = requests.post(
        'https://api.schwabapi.com/trader/v1/accounts/7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F/orders',
        headers=headers,
        json=json_data,
    )

    return




def schwab_limit_order(symbol, price, buysell, amount):
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.mpNzVyYl3_ahFXScoUQn0IbhepS7S8rlZh-zO_zYKNU@',
        'Content-Type': 'application/json',
    }

    json_data = {
        'orderType': 'LIMIT',
        'session': 'NORMAL',
        'duration': 'DAY',
        'price': price,
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': buysell, #string
                'quantity': amount, #int
                'instrument': {
                    'symbol': symbol, #string
                    'assetType': 'EQUITY',
                },
            },
        ],
    }

    response = requests.post(
        'https://api.schwabapi.com/trader/v1/accounts/7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F/orders',
        headers=headers,
        json=json_data,
    )

    return





class SWclient:

    def __init__(self):

        self.authorization_token_md = 'Bearer I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.YjZBLYEgjEBWw5PaEyqYrbyAVrmQoeZuyOezPOP9rW0@'
        self.authorization_token_ad = 'Bearer I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.-jXsdyMXAQUQfem1cdSg7K3cDyxoLVJ7dxTYztULcIQ@'

        self.account_hash_num = '7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F'

    def quote_data(self, stocks):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token_md,
        }

        params = {
            'symbols': stocks, # 'NFLX, COST, TSLA, NVDA, HD, LLY' comma separated string
            'fields': 'quote',
            'indicative': 'false',
        }

        response = requests.get('https://api.schwabapi.com/marketdata/v1/quotes', params=params, headers=headers)

        return response.json()

    def limit_order(self, symbol, price, amount, buysell):

        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token_ad,
            'Content-Type': 'application/json',
        }

        json_data = {
            'orderType': 'LIMIT',
            'session': 'NORMAL',
            'duration': 'DAY',
            'price': price, #string
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
            'https://api.schwabapi.com/trader/v1/accounts/7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F/orders',
            headers=headers,
            json=json_data,
        )

    def get_orders(self):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token_ad
        }

        params = {
            'fromEnteredTime': '2024-03-29T00:00:00.000Z',
            'toEnteredTime': '2024-06-29T00:00:00.000Z',
            'status': 'WORKING',
        }

        response = requests.get(
            'https://api.schwabapi.com/trader/v1/accounts/7AB7448405301904073BD521EEC25E1E727C5EC5C5959501EE8732497E91BE4F/orders',
            params=params,
            headers=headers,
        )

        return response.json()


    def del_order(self, order_id): # oid is int by  default needs converted to string

        url = 'https://api.schwabapi.com/trader/v1/accounts/' + self.account_hash_num + '/orders/' + str(order_id)

        headers = {
            'accept': '*/*',
            'Authorization': self.authorization_token_ad
        }

        response = requests.delete(
            url=url,
            headers=headers,
        )


    def get_positions(self):

        headers = {
            'accept': 'application/json',
            'Authorization': self.authorization_token_ad
        }

        params = {
            'fields': 'positions',
        }

        response = requests.get('https://api.schwabapi.com/trader/v1/accounts', params=params, headers=headers)

        return response.json()



#  quote data {'ORCL': {'assetMainType': 'EQUITY', 'assetSubType': 'COE', 'quoteType': 'NBBO', 'realtime': True, 'ssid': 635772468, 'symbol': 'ORCL', 'quote': {'52WeekHigh': 132.7737, '52WeekLow': 96.92, 'askMICId': 'EDGX', 'askPrice': 119.17, 'askSize': 1, 'askTime': 1715706906963, 'bidMICId': 'MIAX', 'bidPrice': 119.12, 'bidSize': 1, 'bidTime': 1715706907064, 'closePrice': 116.37, 'highPrice': 122.55, 'lastMICId': 'XADF', 'lastPrice': 119.15, 'lastSize': 100, 'lowPrice': 116.13, 'mark': 119.15, 'markChange': 2.78, 'markPercentChange': 2.38893186, 'netChange': 2.78, 'netPercentChange': 2.38893186, 'openPrice': 116.5, 'postMarketChange': 0.0, 'postMarketPercentChange': 0.0, 'quoteTime': 1715706907064, 'securityStatus': 'Normal', 'totalVolume': 12115354, 'tradeTime': 1715706906971}}, 'NFLX': {'assetMainType': 'EQUITY', 'assetSubType': 'COE', 'quoteType': 'NBBO', 'realtime': True, 'ssid': 231673095, 'symbol': 'NFLX', 'quote': {'52WeekHigh': 639.0, '52WeekLow': 329.615, 'askMICId': 'ARCX', 'askPrice': 610.57, 'askSize': 1, 'askTime': 1715706900956, 'bidMICId': 'XCHI', 'bidPrice': 610.1, 'bidSize': 4, 'bidTime': 1715706886512, 'closePrice': 616.59, 'highPrice': 621.48, 'lastMICId': 'XADF', 'lastPrice': 610.335, 'lastSize': 100, 'lowPrice': 609.73, 'mark': 610.335, 'markChange': -6.255, 'markPercentChange': -1.01445045, 'netChange': -6.255, 'netPercentChange': -1.01445045, 'openPrice': 615.17, 'postMarketChange': 0.0, 'postMarketPercentChange': 0.0, 'quoteTime': 1715706900956, 'securityStatus': 'Normal', 'totalVolume': 1196059, 'tradeTime': 1715706903736}}, 'COST': {'assetMainType': 'EQUITY', 'assetSubType': 'COE', 'quoteType': 'NBBO', 'realtime': True, 'ssid': 92819298, 'symbol': 'COST', 'quote': {'52WeekHigh': 789.4814, '52WeekLow': 476.75, 'askMICId': 'ARCX', 'askPrice': 774.68, 'askSize': 1, 'askTime': 1715706896575, 'bidMICId': 'XCHI', 'bidPrice': 774.32, 'bidSize': 4, 'bidTime': 1715706896592, 'closePrice': 775.15, 'highPrice': 780.812, 'lastMICId': 'XADF', 'lastPrice': 774.53, 'lastSize': 100, 'lowPrice': 771.4301, 'mark': 774.53, 'markChange': -0.62, 'markPercentChange': -0.07998452, 'netChange': -0.62, 'netPercentChange': -0.07998452, 'openPrice': 774.93, 'postMarketChange': 0.0, 'postMarketPercentChange': 0.0, 'quoteTime': 1715706896592, 'securityStatus': 'Normal', 'totalVolume': 572552, 'tradeTime': 1715706906435}}}
# get orders [{'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'LIMIT', 'complexOrderStrategyType': 'NONE', 'quantity': 1.0, 'filledQuantity': 0.0, 'remainingQuantity': 1.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'JNST', 'price': 7.0, 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '83406F102', 'symbol': 'SOFI', 'instrumentId': 150758952}, 'instruction': 'BUY', 'positionEffect': 'OPENING', 'quantity': 1.0}], 'orderStrategyType': 'SINGLE', 'orderId': 1000485911320, 'cancelable': True, 'editable': True, 'status': 'WORKING', 'enteredTime': '2024-05-14T17:20:26+0000', 'tag': 'API_TOS:CHART', 'accountNumber': 69464639}]

# get psitions [{'securitiesAccount': {'type': 'MARGIN', 'accountNumber': '69464639', 'roundTrips': 0, 'isDayTrader': False, 'isClosingOnlyRestricted': False, 'pfcbFlag': False, 'positions': [{'shortQuantity': 0.0, 'averagePrice': 0.3166, 'currentDayProfitLoss': -0.27, 'currentDayProfitLossPercentage': -6.32, 'longQuantity': 1.0, 'settledLongQuantity': 1.0, 'settledShortQuantity': 0.0, 'instrument': {'assetType': 'OPTION', 'cusip': '0WBD..QV40007500', 'symbol': 'WBD   240531P00007500', 'description': 'Warner Brothers Discovery Inc 05/31/2024 $7.5 Put', 'netChange': -0.0027, 'type': 'VANILLA', 'putCall': 'PUT', 'underlyingSymbol': 'WBD'}, 'marketValue': 4.0, 'maintenanceRequirement': 0.0, 'averageLongPrice': 0.31, 'taxLotAverageLongPrice': 0.3166, 'longOpenProfitLoss': -27.66, 'previousSessionLongQuantity': 1.0, 'currentDayCost': 0.0}, {'shortQuantity': 0.0, 'averagePrice': 12.5026, 'currentDayProfitLoss': -0.0992, 'currentDayProfitLossPercentage': -0.79, 'longQuantity': 1.0, 'settledLongQuantity': 0.0, 'settledShortQuantity': 0.0, 'instrument': {'assetType': 'EQUITY', 'cusip': '345370860', 'symbol': 'F', 'netChange': 0.0708}, 'marketValue': 12.4, 'maintenanceRequirement': 3.72, 'averageLongPrice': 12.5026, 'taxLotAverageLongPrice': 12.5026, 'longOpenProfitLoss': -0.1018, 'previousSessionLongQuantity': 0.0, 'currentDayCost': 12.5}, {'shortQuantity': 0.0, 'averagePrice': 339.34, 'currentDayProfitLoss': -1.935, 'currentDayProfitLossPercentage': -0.57, 'longQuantity': 1.0, 'settledLongQuantity': 1.0, 'settledShortQuantity': 0.0, 'instrument': {'assetType': 'EQUITY', 'cusip': '437076102', 'symbol': 'HD', 'netChange': -1.935}, 'marketValue': 339.03, 'maintenanceRequirement': 101.71, 'averageLongPrice': 339.335, 'taxLotAverageLongPrice': 339.34, 'longOpenProfitLoss': -0.315, 'previousSessionLongQuantity': 1.0, 'currentDayCost': 0.0}, {'shortQuantity': 0.0, 'averagePrice': 8.3233, 'currentDayProfitLoss': 9.87, 'currentDayProfitLossPercentage': 1.18, 'longQuantity': 100.0, 'settledLongQuantity': 100.0, 'settledShortQuantity': 0.0, 'instrument': {'assetType': 'EQUITY', 'cusip': '934423104', 'symbol': 'WBD', 'netChange': 0.0987}, 'marketValue': 847.87, 'maintenanceRequirement': 172.87, 'averageLongPrice': 8.305725, 'taxLotAverageLongPrice': 8.3233, 'longOpenProfitLoss': 15.54, 'previousSessionLongQuantity': 100.0, 'currentDayCost': 0.0}, {'shortQuantity': 0.0, 'averagePrice': 7.51, 'currentDayProfitLoss': -0.035, 'currentDayProfitLossPercentage': -0.47, 'longQuantity': 1.0, 'settledLongQuantity': 0.0, 'settledShortQuantity': 0.0, 'instrument': {'assetType': 'EQUITY', 'cusip': '83406F102', 'symbol': 'SOFI', 'netChange': 0.365}, 'marketValue': 7.48, 'maintenanceRequirement': 2.99, 'averageLongPrice': 7.51, 'taxLotAverageLongPrice': 7.51, 'longOpenProfitLoss': -0.035, 'previousSessionLongQuantity': 0.0, 'currentDayCost': 7.51}], 'initialBalances': {'accruedInterest': 0.0, 'availableFundsNonMarginableTrade': 2811.91, 'bondValue': 14902.32, 'buyingPower': 10080.0, 'cashBalance': 2811.91, 'cashAvailableForTrading': 0.0, 'cashReceipts': 0.0, 'dayTradingBuyingPower': 14971.0, 'dayTradingBuyingPowerCall': 0.0, 'dayTradingEquityCall': 0.0, 'equity': 3995.14, 'equityPercentage': 100.0, 'liquidationValue': 3995.14, 'longMarginValue': 1178.96, 'longOptionMarketValue': 4.27, 'longStockValue': 1178.96, 'maintenanceCall': 0.0, 'maintenanceRequirement': 265.0, 'margin': 2811.91, 'marginEquity': 3990.87, 'moneyMarketFund': 0.0, 'mutualFundValue': 2811.91, 'regTCall': 0.0, 'shortMarginValue': 0.0, 'shortOptionMarketValue': 0.0, 'shortStockValue': 0.0, 'totalCash': 0.0, 'isInCall': False, 'pendingDeposits': 0.0, 'marginBalance': 0.0, 'shortBalance': 0.0, 'accountValue': 3995.14}, 'currentBalances': {'accruedInterest': 0.0, 'cashBalance': 2791.9, 'cashReceipts': 0.0, 'longOptionMarketValue': 4.0, 'liquidationValue': 4002.68, 'longMarketValue': 1206.78, 'moneyMarketFund': 0.0, 'savings': 0.0, 'shortMarketValue': 0.0, 'pendingDeposits': 0.0, 'mutualFundValue': 0.0, 'bondValue': 0.0, 'shortOptionMarketValue': 0.0, 'availableFunds': 3717.39, 'availableFundsNonMarginableTrade': 1188.97, 'buyingPower': 10059.98, 'buyingPowerNonMarginableTrade': 3717.39, 'dayTradingBuyingPower': 14971.0, 'equity': 3998.68, 'equityPercentage': 100.0, 'longMarginValue': 1206.78, 'maintenanceCall': 0.0, 'maintenanceRequirement': 281.29, 'marginBalance': 0.0, 'regTCall': 0.0, 'shortBalance': 0.0, 'shortMarginValue': 0.0, 'sma': 5029.99}, 'projectedBalances': {'availableFunds': 3717.39, 'availableFundsNonMarginableTrade': 3717.39, 'buyingPower': 10059.98, 'dayTradingBuyingPower': 14971.0, 'dayTradingBuyingPowerCall': 0.0, 'maintenanceCall': 0.0, 'regTCall': 0.0, 'isInCall': False, 'stockBuyingPower': 10059.98}}}]


#X = SWclient()

