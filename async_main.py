import asyncio, random
from queue_lib.async_queue import AsyncQueue

async def pusher(queue: AsyncQueue):
    x = random.randint(1, 10)
    print(f'pushin {x}')
    await queue.push(x)

async def popper(queue: AsyncQueue):
    print(f'poppin {await queue.pop()}')

async def main_wrapper():
    queue: AsyncQueue = AsyncQueue()
    tasks = []
    for _ in range(3):
        tasks.append(asyncio.create_task(pusher(queue)))
    for _ in range(4):
        tasks.append(asyncio.create_task(popper(queue)))
    tasks.append(asyncio.create_task(pusher(queue)))
    await asyncio.wait(tasks)

def main():
    asyncio.run(main_wrapper())
