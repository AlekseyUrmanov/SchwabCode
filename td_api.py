import json
import requests
import pandas as pd


class TDclient:

    def __init__(self):

        self.ck = "Y1KS0BMRKRBSI6CVNYIHHN1NVF3VUI2J"
        self.at = 'Bearer lN2BQGWgWWkPq3iMSKsv4UNX8ayjoKPhLHsRegMVcnm0qNsH0RMKPpvnmtaUsI8EndGe0aNgYVFbsrOueoMTZtG+pEu5s8J7zeyXIeQUoJ8gCYMsZXC2t1p5zg82EQwYWnK/UWgdF281IjU5ae0VHjjWe5WjhZnrKV2F6l3ue0WqktUK4Pv204+PGwVw2iz2sdSCrZSnQaQ3z6INca0GPA08l3tnBWou3BD2eapvWZsnKtFZIFT5CoLARtaT667aSKr6BSk53D8e3pz0QkdayJUdaJVQiky2Tdf1L4HxebgbpBs1nIQld3vijuiKzUlEuf9aNkUHWzRVenULeW6yVr9O+ry5iZGmXoj461XgO+NvU9sodVEEZfx8IyQkq3aIMelt7zaP17hDywnB1jOYIDu9HUrtF3S3L180uM3tzd6GTUknvEPdwbeWQZThmJyRsATPhNzGaDO5SHdBwRX5lWeac+0qFhIN3uLIbkwvlcNxgtueAXr98t3uMvGb+q+VfIwf3KvXQN/OFMoyLkI49/XKt7ZSlDfIbmRoxsXwBWfBu962s88s6D6OsZJ100MQuG4LYrgoVi/JHHvlxi2HSGbsfBq+kRfbmFqDiQRCnoz3omvnQIVwRGIb6TQA/i+2V17Hz1crVJK94A/a8hguko+JPFfhR/GSrPU8sb/dZa68PZrOA993AdycpUgqqJfSk4Jws45B5HvKAiCA7WUydCgdGcuychye0IP7nOoiaSVDHEIfOpRH34KABEAVj4aR3J0HgdVe8S4hy07nU8VfEHEYY+Sn4Oyd8hBur+sQRxPizMV22yLCkcWMpRPEIFklawASSqVPEtpQ/o84v3G4etT7gUz44k41AWAotwkrlAMsZy+ugf3HkiPP1xyCJzTIo1T6fxib3h0FuiPLGghv6anR3WA05Fi1I6KYvdrimonpYf/+f8fN2CShbJmb38jrKKEzZ+9pEkR7e8MHhBLtXDr1AobO94q5QtxoDlv3QE7/leATykgU4FBQJQqZ3PjqX+An1txROiPMlX7Yj4WDC74vmmOok1RGrERvK6gN6qQsSthJW6ydY2GO9d+Wmfr4QspaGA2ocho4LatAviRQu0DGhJPszdsHduaIY4eBo1B/8gE7i2rqW9PhdFTb7Gq5l0HifCxzUBE=212FD3x19z9sWBHDJACbC00B75E'
        self.rt = "cHOlhGwTwx8Da1E2cu1oWY8mJ5Pqp8k5LA2hJ1st3EyiqVYpkfxihHyYlKwCTuN66TldGvnfh0Rz7yjiCAsrw3OFNJXH226zMmv2dWkuqLXj/eayeo/tag2DcNQc0/VDolIapfWOwhk7ARUlnAZSv++k0PgtFhEWJeGrGeW3Vdjly0iWlig1rK/GGD5XbkXpFDOtyfYgZIrK//L80H8ocUMOK4Tt+HcTnAtDdKmHYFlvqFLfrqHvjEuxZoSCwnDTAvhSeMH8j5EtReVTnRRv1i11Z1OZDNYzuHq6cHC5g3R3MBjbOKMp0XMPLz3/n/NuqhRvzqbCk2lsfR8YyPEXpzxwoNIo0zkbhUbuJ+9eKZypLoET0ztpnHMoF9OHrbLF9jo523qJlYaauk36peLZQMMXytp5Ynu8tXoxLugDfOCCjfYQCSLIYi0T9Wj100MQuG4LYrgoVi/JHHvlU/7OXTXEASEHjNIzW4h5khZcDFuo909n/QyF88qLbXyOpylC6/cpwrcpKASzEorCOacw6P6iKV3dAJpwzG39bI4VFh6L/JWZL3wJHeun9xENb1NEEPEyOw/pmchMnbCRAHjW/XMWIFSCOG9HSM7RJFB3l1x7Am3az0WFHCYGQ5XFZh30CoujFku6j29PvYzfAeu/BrPK1Iryxs9RYGyTmjLTYAmlJpryXyc50Nxsjn+dRjybITqpCDL5ACZmj4A+gc8wzVBw2idDussdPnENdM7ct+itl1zhH5M1cbUFQcdZytO5+r4PTqoikStDy1IGVKZosfOX/Cs/ZywRROQC2aDGsDBXulyZlsOxQx6Qvh6AIQjvb6RS06Qy+3yu5VFp+oOwBgnRMLiAb3LrDtaReYoJ96fYgDHBGKCHT2UFSQOoVnQGsUezQPTLGaE=212FD3x19z9sWBHDJACbC00B75E"
        # https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=https://localhost/mytest&client_id=Y1KS0BMRKRBSI6CVNYIHHN1NVF3VUI2J%40AMER.OAUTHAP
        # goes to 404 page take part after code = , put into url dcoder simple UTF-8 decode
        # use auth grant type, slap in url, api key, and that code and offline and boom
        # self.new_access_token()

    def get_fundamentals(self, symbol):

        # url for specific call of data
        url = 'https://api.tdameritrade.com/v1/instruments'
        # format tickr inserts the stock ticker variable, r is raw string.

        payload = {'apikey': self.ck,  # Simple payload structuring
                   'symbol': symbol,
                   'projection': 'fundamental'
                   }

        response = requests.get(url=url, params=payload)
        content = self.response_processing(response, self.get_fundamentals, symbol)
        fund_data = (content[symbol])['fundamental']
        return fund_data

    def get_account_orders(self, details='orders'):
        # orders or positiions
        # url for specific call of data
        url = 'https://api.tdameritrade.com/v1/accounts/236642469/orders'
        # format tickr inserts the stock ticker variable, r is raw string.
        headers = {
            'Authorization': self.at
        }

        params = {
            'status': 'WORKING',  # WORKING, PENDING_ACTIVATION (after hours), CANCELLED.
            # 'fields': details
        }

        response = requests.get(url, params=params, headers=headers)
        content = self.response_processing(response, self.get_account_orders, details)
        return content

    def get_account_positions(self, details):


        url = 'https://api.tdameritrade.com/v1/accounts/236642469'
        # format tickr inserts the stock ticker variable, r is raw string.
        headers = {
            'Authorization': self.at
        }

        params = {
            'fields': 'positions'
        }

        response = requests.get(url, params=params, headers=headers)
        content = self.response_processing(response, self.get_account_positions, details)
        return content

    def get_quote(self, details=[]):

        symbol = details[0]
        real_time = details[1]

        # with authentication there will be real_time_data entitled : true
        url = 'https://api.tdameritrade.com/v1/marketdata/{}/quotes'.format(symbol)

        if real_time:
            params = {
                'apikey': self.ck,
            }
            header = {
                'Authorization': self.at,
                'Content-Type': 'application/json'
            }
            print('tried real time')
        else:
            params = {
                'apikey': self.ck,

            }
            header = {}

        response = requests.get(url=url, params=params, headers=header)
        content = self.response_processing(response, self.get_quote, symbol)
        return content

    def get_quotes(self, details=[]):

        symbols = details[0]
        real_time = details[1]

        # with authentication there will be real_time_data entitled : true
        url = 'https://api.tdameritrade.com/v1/marketdata/quotes'

        if real_time:
            params = {
                'apikey': self.ck,
                'symbol': symbols
            }
            header = {
                'Authorization': self.at,
                'Content-Type': 'application/json'
            }
            #print('tried real time')
        else:
            params = {
                'apikey': self.ck,
                'symbol': symbols

            }
            header = {}

        response = requests.get(url=url, params=params, headers=header)
        content = self.response_processing(response, self.get_quote, symbols)
        return content

    def get_limit_order_book(self, ticker):
        endpoint = format("https://api.tdameritrade.com/v1/marketdata/{}/orderbook", ticker)

        headers = {
            'apikey': self.ck,
            'Authorization': self.at
        }

        response = requests.get(url=endpoint, headers=headers)
        print(response)
        print(response.status_code)
        # content = self.response_processing(response, self.get_limit_order_book, ticker)
        print(json.loads(response.content))
        z = json.loads(response.content)
        print(z)

        content = response.json()
        return content

    def option_chain(self, details=[]):

        ticker = details[0]
        real_time = details[1]
        if real_time:

            params = {
                'apikey': self.ck,
                'symbol': ticker,
                'contractType': 'ALL',
                'strikeCount': '14',
                'includeQuotes': 'FALSE',
                'strategy': 'SINGLE',
            }
            header = {
                'Authorization': self.at,
                'Content-Type': 'application/json'
            }
            print('tried real time')

        else:

            params = {
                'apikey': self.ck,
                'symbol': ticker,
                'contractType': 'ALL',
                'strikeCount': '14',
                'includeQuotes': 'FALSE',
                'strategy': 'SINGLE',
                'range': 'ITM'
            }

            header = {}

        response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params=params, headers=header)
        content = self.response_processing(response, self.option_chain, details)
        return content

    def specific_option_chain_quote(self, symbol, real_time=False):

        ticker = symbol.split('_')[0]
        date_string = symbol.split('_')[1]

        day = date_string[2:4]
        mon = date_string[0:2]
        year = date_string[4:6]

        full_date = '20' + year + '-' + mon + '-' + day

        if "P" in symbol:
            strike = symbol.split('P')[1]
            contract_type = 'PUT'
            pc_query = 'putExpDateMap'
        else:
            strike = symbol.split('C')[1]
            contract_type = 'CALL'
            pc_query = 'callExpDateMap'

        if real_time:

            params = {
                'apikey': self.ck,
                'symbol': ticker,
                'contractType': contract_type,
                'includeQuotes': 'TRUE',
                'strike': strike,
                'toDate': full_date,
            }

            header = {
                'Authorization': self.at,
                'Content-Type': 'application/json'
            }

            response = requests.get('https://api.tdameritrade.com/v1/marketdata/chains', params=params, headers=header)
            content = self.response_processing(response, self.option_chain, symbol)

            contract_data = content[pc_query]
            contract_data = contract_data[list(contract_data.keys())[0]]
            contract_data = contract_data[list(contract_data.keys())[0]]
            contract_data = contract_data[0]

            underlying = content['underlying']

            return {'asset': underlying, 'option': contract_data}

        else:
            pass

    @staticmethod
    def sort_data_into_data_frames(raw_json):

        all_frames = []

        for key in ['callExpDateMap', 'putExpDateMap']:
            call_or_put_data = raw_json[key]
            expiration_date_list = list(call_or_put_data.keys())

            framed_option_chain = {}
            for date in expiration_date_list:

                strikes = list((call_or_put_data[date]).keys())
                expire_data_relative_data = []

                for strike in strikes:
                    strike_data_dict = (call_or_put_data[date][strike])[0]
                    expire_data_relative_data.append(strike_data_dict)

                frame = pd.DataFrame.from_records(expire_data_relative_data, index=strikes)
                index_date = (date.split(':'))[0]
                # date string from TD comes as date:value, we just grab the date
                framed_option_chain[index_date] = frame

            all_frames.append(framed_option_chain)

        return all_frames
        # frames is a list, 2 entries of dictionaries, first is a dictionary of call data frames, where the keys are
        # the dates, second entry is the put dictionary of data frames.

    def cancel_option_order(self, OID):

        url = 'https://api.tdameritrade.com/v1/accounts/236642469/orders/{}'.format(OID)

        headers = {
            'Authorization': self.at,
            # 'Content-Type': 'application/json',
        }

        '''parameters = {



            'orderId': OID
        }'''

        response = requests.delete(url=url, headers=headers)
        print(response)

        content = self.response_processing(response, self.cancel_option_order, parameters=OID)

        return (content)

    def option_order(self, **kwargs):

        details = kwargs

        url = 'https://api.tdameritrade.com/v1/accounts/236642469/orders'

        headers = {
            'Authorization': self.at,
            'Content-Type': 'application/json',
        }

        # BUY_TO_OPEN  BUY_TO_CLOSE  SELL_TO_OPEN  SELL_TO_CLOSE
        # symbol is option/strike/date specific, get from data frame
        data = {
            "complexOrderStrategyType": "NONE",
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": details['price'],
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": details['instruction'],
                    "quantity": details['quantity'],
                    "instrument": {
                        "symbol": details['symbol'],
                        "assetType": "OPTION"
                    }
                }
            ]
        }

        response = requests.post(url=url, headers=headers,
                                 data=json.dumps(data))
        self.response_processing(response, self.option_order, details)


    def equity_order(self, price, stock, buysell, amount):


        url = 'https://api.tdameritrade.com/v1/accounts/236642469/orders'

        headers = {
            'Authorization': self.at,
            'Content-Type': 'application/json',
        }

        data = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "price": price,
            "orderLegCollection":
                [
                {
                    "instruction": buysell, # Buy Sell
                    "quantity": amount,
                    "instrument": {
                        "symbol": stock,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }

        response = requests.post(url=url, headers=headers,
                                 data=json.dumps(data))
        details = [price, buysell, stock, amount]
        self.response_processing(response, self.equity_order, details)

    def new_access_token(self):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.rt,
            'access_type': '',
            'code': '',
            'client_id': self.ck,
            'redirect_uri': ''
        }

        response = requests.post('https://api.tdameritrade.com/v1/oauth2/token', data=data)
        content = self.response_processing(response, self.new_access_token, None)
        new_access_token = content['access_token']
        full_code = 'Bearer ' + new_access_token
        print(full_code)
        self.at = full_code

    def response_processing(self, response, func_call, parameters):
        # show sresponses that came, update tokens and variables, recall operations, keep operation log
        #print(func_call.__name__.upper())
        response_code = response.status_code
        #print(response)
        #print(response_code)

        if response_code == 401:
            self.new_access_token()
            print('Created New Access Token')
            print('Updated Token')
            print('Running Correction Instance')
            if type(parameters) == dict:
                data = func_call(**parameters)
            else:
                data = func_call(details=parameters)
            print('Instance Complete')
            return data

            # run process again

        elif response_code == 200 or response_code == 201:
            try:
                #print(parameters)
                content = response.json()
                #print('Returning Data')
                #print('Call Complete')
                return content
            except Exception:
                print('No data to return')
                print('Call Complete')
                return

        elif response_code == 400:  # should not occur from internal method// instance calls
            print('Improper Call Structure')
            print(parameters)
            pass


#tdc = TDclient()
#tdc.new_access_token()
#tdc.equity_order(price=7, stock='WBD', buysell='BUY', amount=1)

#data = tdc.get_account_orders()
#print(data)
#13783484498
#[{'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'LIMIT', 'complexOrderStrategyType': 'NONE', 'quantity': 1.0, 'filledQuantity': 0.0, 'remainingQuantity': 1.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'CDRG', 'price': 7.0, 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '934423104', 'symbol': 'WBD'}, 'instruction': 'BUY', 'positionEffect': 'OPENING', 'quantity': 1.0}], 'orderStrategyType': 'SINGLE', 'orderId': 13783484498, 'cancelable': True, 'editable': True, 'status': 'WORKING', 'enteredTime': '2024-04-10T19:21:37+0000', 'tag': 'AA_Alekseevich', 'accountId': 236642469}]



'''
data = tdc.get_account_positions(details=None)
print(data['securitiesAccount']['positions'])
'''

