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
        return f'Successfully created the new topic {topic}\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404

@httpRequestHandler.route("/topic/<topic>", methods=['DELETE'])
async def remove(topic):
    try:
        await topicManager.remove(topic)
        await queueManager.topicRemoved(topic)
        return f'Successfully deleted {topic} topic\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/subscription/<topic>", methods=['POST'])
async def subscribe(topic):
    try:
        id = await subscriptionManager.subscribe(topic)
        return f'{id}\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>", methods=['DELETE'])
async def unsubscribe(topic, id):
    try:
        await subscriptionManager.unsubscribe(topic, int(id))
        return f'Successfully unsubscribed id {id} from {topic} topic\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/publish/<topic>/<scenario_id>", methods=['POST'])
async def publish(topic, scenario_id):
    try:
        form = await request.json
        await queueManager.publishMessage(topic, str(form['item']), str(form['benchmark_id']), scenario_id)
        return f'Successfully published your message to {topic} topic\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404
    
@httpRequestHandler.route("/subscription/<topic>/<id>/<scenario_id>", methods=['GET'])
async def retrieve(topic, id, scenario_id):
    try:
        message = await queueManager.retrieveMessage(topic, id, scenario_id)
        return f'{message}\r\n', 200
    except Exception as e:
        return f'{str(e)}\r\n', 404

httpRequestHandler.run()
