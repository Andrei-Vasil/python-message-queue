from queueManager import QueueManager


class SubscriptionManager:
    def __init__(self, queueManager: QueueManager):
        self.__queueManager = queueManager

    def subscribe(self, topic: str) -> int:
        return self.__queueManager.createQueueChannel(topic)

    def unsubscribe(self, topic: str, client_id: int):
        self.__queueManager.removeQueueChannel(topic, client_id)
