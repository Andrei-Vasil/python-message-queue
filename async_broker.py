from quart import Quart, request
from queue_lib.async_queue import AsyncQueue

app: Quart = Quart(__name__)
queue: AsyncQueue = AsyncQueue()

@app.route("/push", methods=['POST'])
async def push():
    form = await request.form
    await queue.push(form['item'])
    return ''

@app.route("/pop", methods=['GET'])
async def pop():
    return await queue.pop()

app.run()
