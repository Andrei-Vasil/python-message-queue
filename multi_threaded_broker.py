from flask import Flask, request
from queue_lib.multi_threaded_queue import MultiThreadedQueue

app: Flask = Flask(__name__)
queue: MultiThreadedQueue = MultiThreadedQueue()

@app.route("/push", methods=['POST'])
def push():
    queue.push(request.form['item'])
    return ''

@app.route("/pop", methods=['GET'])
def pop():
    return queue.pop()

app.run()
