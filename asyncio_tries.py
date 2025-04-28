import asyncio
import time

def blocking_function5():
    time.sleep(5)
    print("Finished blocking thread 5")

def blocking_function1():
    time.sleep(1)
    print("Finished blocking thread 1")


async def sleep5():
    await asyncio.sleep(5)
    print("Finished async sleeping 5")

async def sleep1():
    await asyncio.sleep(1)
    print("Finished async sleeping 1")


async def main():
    await asyncio.to_thread(blocking_function5)  # Event Loop ?
    await asyncio.to_thread(blocking_function1)  # Event Loop ?

    await sleep5()
    await sleep1()
    print("Finished main")


async def main_gather():
    await asyncio.gather(
        asyncio.to_thread(blocking_function5),
        asyncio.to_thread(blocking_function1),
        sleep5(),
        sleep1()
    )
    print("Finished main")


# asyncio.run(main())
asyncio.run(main_gather())