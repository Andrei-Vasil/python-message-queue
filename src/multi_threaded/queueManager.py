from topicManager import TopicManager
from lib.queue import MultiThreadedQueue
from threading import Lock

class QueueManager:
    def __init__(self, topicManager: TopicManager):
        self.__topicManager = topicManager
        self.__queue_channels: dict[str, dict[int, MultiThreadedQueue]] = dict()
        self.__queue_channels_locks: dict[str, Lock] = dict()
        self.__max_id_4_topic: dict[str, int] = dict()
        self.__ids_lock = Lock()

    def topicRemoved(self, topic: str):
        with self.__ids_lock:
            self.__max_id_4_topic.pop(topic)
        with self.__queue_channels_locks[topic]:
            self.__queue_channels.pop(topic)
        self.__queue_channels_locks.pop(topic)

    def topicAdded(self, topic: str):
        with self.__ids_lock:
            self.__max_id_4_topic[topic] = 0
        self.__queue_channels_locks[topic] = Lock()
        with self.__queue_channels_locks[topic]:
            self.__queue_channels[topic] = dict()

    def createQueueChannel(self, topic: str) -> int:
        if not self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        id = None
        with self.__ids_lock:
            id = self.__max_id_4_topic[topic]
            self.__max_id_4_topic[topic] += 1
        with self.__queue_channels_locks[topic]:
            self.__queue_channels[topic][id] = MultiThreadedQueue()
        return id

    def removeQueueChannel(self, topic: str, id: int):
        if not self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        with self.__queue_channels_locks[topic]:
            self.__queue_channels[topic].pop(id)

    def publishMessage(self, topic: str, message: str, benchmark_id: str):
        if not self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        with self.__queue_channels_locks[topic]:
            for queue_channel in self.__queue_channels[topic].values():
                queue_channel.push(message, benchmark_id)

    def retrieveMessage(self, topic: str, queue_channel_id: int) -> str:
        if not self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        with self.__queue_channels_locks[topic]:
            return self.__queue_channels[topic][int(queue_channel_id)].pop()
