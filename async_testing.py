import asyncio
import time

async def main():

    while True:
        print('gathering data')
        await asyncio.sleep(1)

async def not_main():

    while True:
        print('testing trading conditions')
        await asyncio.sleep(2)


async def run_all():
    # Schedule both functions concurrently
    task1 = asyncio.create_task(main())
    task2 = asyncio.create_task(not_main())

    await asyncio.wait([task1, task2])

    # Continue with other tasks or operations without waiting for function_one() and function_two() to finish
    print("Continuing with other tasks or operations...")

#asyncio.run(run_all())



