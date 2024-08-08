from testing import SWclient
import time
import datetime

X = SWclient()


while True:

    X.refresh_token_auth()

    token = X.authorization_token

    with open('rftoken.txt', 'w') as file:
        file.write(token)

    time.sleep(900)

