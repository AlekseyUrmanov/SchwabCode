
def can_quote(stock, api_client):

    data = api_client.price_history(ticker=stock)['candles']

    red = 0
    green = 0

    rg_cand = []

    rg_deltas = {'r': [], 'g': []}

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

    sigma_g = (mu_g ** 0.5)/2
    sigma_r = (mu_r ** 0.5)/2

    three_candle_data = data[len(data)-3:len(data)-1]

    if rg_cand[-3:-1] == ['r', 'r']:
        pass
    else:
        return False

    sizes = [c['open'] - c['close'] for c in three_candle_data]
    sizes = [True if c > (sigma_r + mu_r) else False for c in sizes]

    if True in sizes:
        return True
    else:
        return False


