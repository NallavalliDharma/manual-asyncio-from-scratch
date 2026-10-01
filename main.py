from EventLoop import EventLoop
from future import Future
from yield_control import yield_control

###Demo 1 test
async def hello():
    return 42


loop = EventLoop()

task = loop.create_task(
    hello()
)

result = loop.run_until_complete(
    task
)

print(result)

### Demo2 test:
async def worker(name):

    print(name, "start")

    await yield_control()

    print(name, "end")


loop = EventLoop()

loop.create_task(
    worker("A")
)

loop.create_task(
    worker("B")
)

loop.run_forever()

### Demo3 test:
async def worker(name):

    print(name, 1)

    await yield_control()

    print(name, 2)

    await yield_control()

    print(name, 3)


loop = EventLoop()

loop.create_task(worker("A"))
loop.create_task(worker("B"))

loop.run_forever()

### Demo4 test:
async def waiter():

    print("waiting")

    result = await future

    print(result)


loop = EventLoop()

future = Future()

loop.create_task(
    waiter()
)

loop.call_soon(
    future.set_result,
    "done"
)

loop.run_forever()

###Demo5 test:

async def calculate():

    await yield_control()

    return 100


async def main():

    task = loop.create_task(
        calculate()
    )

    result = await task

    return result


loop = EventLoop()

task = loop.create_task(
    main()
)

result = loop.run_until_complete(
    task
)

print(result)