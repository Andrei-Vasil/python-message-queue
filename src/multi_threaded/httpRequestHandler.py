from flask import Flask, request
from lib.queue import MultiThreadedQueue
from subscriptionManager import SubscriptionManager
from topicManager import TopicManager
from queueManager import QueueManager

httpRequestHandler: Flask = Flask(__name__)
topicManager: TopicManager = TopicManager()
queueManager: QueueManager = QueueManager(topicManager)
subscriptionManager: SubscriptionManager = SubscriptionManager(queueManager)

@httpRequestHandler.route("/topic/<topic>", methods=['POST'])
def new(topic):
    try:
        topicManager.new(topic)
        queueManager.topicAdded(topic)
        return f'Successfully created the new topic {topic}\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404

@httpRequestHandler.route("/topic/<topic>", methods=['DELETE'])
def remove(topic):
    try:
        topicManager.remove(topic)
        queueManager.topicRemoved(topic)
        return f'Successfully deleted {topic} topic\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/subscription/<topic>", methods=['POST'])
def subscribe(topic):
    try:
        id = subscriptionManager.subscribe(topic)
        return f'{id}\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>", methods=['DELETE'])
def unsubscribe(topic, id):
    try:
        subscriptionManager.unsubscribe(topic, int(id))
        return f'Successfully unsubscribed id {id} from {topic} topic\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/publish/<topic>/<scenario_id>", methods=['POST'])
def publish(topic, scenario_id):
    try:
        form = request.json
        queueManager.publishMessage(topic, str(form['item']), str(form['benchmark_id']), scenario_id)
        return f'Successfully published your message to {topic} topic\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>/<scenario_id>", methods=['GET'])
def retrieve(topic, id, scenario_id):
    try:
        message = queueManager.retrieveMessage(topic, id, scenario_id)
        return f'{message}\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404

with MultiThreadedQueue() as queue:
    httpRequestHandler.run(port=5003)
