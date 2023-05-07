from quart import Quart, request
from lib.queue import AsyncQueue
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

# TODO: map each request url

httpRequestHandler.run()


# @httpRequestHandler.route("/push", methods=['POST'])
# async def push():
#     form = await request.json
#     await queue.push(form['item'])
#     return ''

# @httpRequestHandler.route("/pop", methods=['GET'])
# async def pop():
#     return str(await queue.pop())