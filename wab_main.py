from testing import SWclient
import time
import datetime
import asyncio
import wab_trader_classes


Schwab_Api_Client = SWclient()
print(datetime.datetime.now())


products_to_trade = [wab_trader_classes.product(100,'F', Schwab_Api_Client)]

active_trading_portfolio = wab_trader_classes.portfolio(products_to_trade,'F', Schwab_Api_Client)


async def method_one():


    while True:
        active_trading_portfolio.collect_data()

        await asyncio.sleep(1)


async def method_two():


    while True:
        active_trading_portfolio.test_conditions()
        await asyncio.sleep(1)


async def method_three():


    while True:
        active_trading_portfolio.poll_account_data()
        await asyncio.sleep(1)


async def run_all():

    task1 = asyncio.create_task(method_one())
    task2 = asyncio.create_task(method_two())
    task3 = asyncio.create_task(method_three())

    await asyncio.gather(task1, task2, task3)

    # Continue with other tasks or operations without waiting for function_one() and function_two() to finish
    print("Continuing with other tasks or operations...")




asyncio.run(run_all())

