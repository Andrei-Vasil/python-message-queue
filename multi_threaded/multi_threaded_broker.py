from flask import Flask, request
from multi_threaded_queue import MultiThreadedQueue

httpRequestHandler: Flask = Flask(__name__)
queue: MultiThreadedQueue = None

@httpRequestHandler.route("/push", methods=['POST'])
def push():
    queue.push(request.json['item'])
    return ''

@httpRequestHandler.route("/pop", methods=['GET'])
def pop():
    return str(queue.pop())

with MultiThreadedQueue() as queue:
    httpRequestHandler.run()
