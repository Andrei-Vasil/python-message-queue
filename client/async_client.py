import asyncio, random, requests, time

async def pusher():
    x = random.randint(1, 10)
    headers = {
      'Content-Type': 'application/json; charset=utf-8', 
      'Accept': 'text/plain'
    }
    body = { 
        "item": x
    }
    requests.post('http://localhost:5000/push', headers=headers, json=body, stream=True)

async def popper():
    requests.get('http://localhost:5000/pop')

async def main_wrapper():
    tasks = []
    for _ in range(500):
        tasks.append(asyncio.create_task(pusher()))
    for _ in range(500):
        tasks.append(asyncio.create_task(popper()))
    # tasks.append(asyncio.create_task(pusher()))
    await asyncio.wait(tasks)

def main():
    start = time.time()
    asyncio.run(main_wrapper())
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
