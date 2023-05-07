from queueManager import QueueManager


class SubscriptionManager:
    def __init__(self, queueManager: QueueManager):
        self.__queueManager = queueManager

    async def subscribe(self, topic: str) -> int:
        return await self.__queueManager.createQueueChannel(topic)

    async def unsubscribe(self, topic: str, client_id: int):
        await self.__queueManager.removeQueueChannel(topic, client_id)
