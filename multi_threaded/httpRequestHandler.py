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
        return f'Successfully created the new topic {topic}', 200
    except Exception as e:
        return str(e), 404

@httpRequestHandler.route("/topic/<topic>", methods=['DELETE'])
def remove(topic):
    try:
        topicManager.remove(topic)
        queueManager.topicRemoved(topic)
        return f'Successfully deleted {topic} topic', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/subscription/<topic>", methods=['POST'])
def subscribe(topic):
    try:
        id = subscriptionManager.subscribe(topic)
        return f'{id}', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>", methods=['DELETE'])
def unsubscribe(topic, id):
    try:
        subscriptionManager.unsubscribe(topic, id)
        return f'Successfully unsubscribed id {id} from {topic} topic', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/publish/<topic>", methods=['POST'])
def publish(topic):
    try:
        form = request.json
        queueManager.publishMessage(topic, str(form['item']))
        return f'Successfully published your message to {topic} topic', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>", methods=['GET'])
def retrieve(topic, id):
    try:
        message = queueManager.retrieveMessage(topic, id)
        return f'{message}', 200
    except Exception as e:
        return str(e), 404

with MultiThreadedQueue() as queue:
    httpRequestHandler.run()
