from types import TracebackType
from quart import Quart, request
from subscriptionManager import SubscriptionManager
from topicManager import TopicManager
from queueManager import QueueManager

httpRequestHandler: Quart = Quart(__name__)
topicManager: TopicManager = TopicManager()
queueManager: QueueManager = QueueManager(topicManager)
subscriptionManager: SubscriptionManager = SubscriptionManager(queueManager)

@httpRequestHandler.route("/topic/<topic>", methods=['POST'])
async def new(topic):
    try:
        await topicManager.new(topic)
        await queueManager.topicAdded(topic)
        return f'Successfully created the new topic {topic}', 200
    except Exception as e:
        return str(e), 404

@httpRequestHandler.route("/topic/<topic>", methods=['DELETE'])
async def remove(topic):
    try:
        await topicManager.remove(topic)
        await queueManager.topicRemoved(topic)
        return f'Successfully deleted {topic} topic', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/subscription/<topic>", methods=['POST'])
async def subscribe(topic):
    try:
        id = await subscriptionManager.subscribe(topic)
        return f'{id}', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>", methods=['DELETE'])
async def unsubscribe(topic, id):
    try:
        await subscriptionManager.unsubscribe(topic, id)
        return f'Successfully unsubscribed id {id} from {topic} topic', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/publish/<topic>", methods=['POST'])
async def publish(topic):
    try:
        form = await request.json
        await queueManager.publishMessage(topic, str(form['item']))
        return f'Successfully published your message to {topic} topic', 200
    except Exception as e:
        return str(e), 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>", methods=['GET'])
async def retrieve(topic, id):
    try:
        message = await queueManager.retrieveMessage(topic, id)
        print(f'retrieve: {message}')
        return f'{message}', 200
    except Exception as e:
        return str(e), 404

httpRequestHandler.run()
