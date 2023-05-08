from topicManager import TopicManager
from lib.queue import AsyncQueue
import asyncio

class QueueManager:
    def __init__(self, topicManager: TopicManager):
        self.__topicManager = topicManager
        self.__queue_channels: dict[str, dict[int, AsyncQueue]] = dict()
        self.__queue_channels_locks: dict[str, asyncio.Lock] = dict()
        self.__max_id_4_topic: dict[str, int] = dict()
        self.__ids_lock = asyncio.Lock()

    async def topicRemoved(self, topic: str):
        async with self.__ids_lock:
            self.__max_id_4_topic.pop(topic)
        async with self.__queue_channels_locks[topic]:
            self.__queue_channels.pop(topic)
        self.__queue_channels_locks.pop(topic)

    async def topicAdded(self, topic: str):
        async with self.__ids_lock:
            self.__max_id_4_topic[topic] = 0
        self.__queue_channels_locks[topic] = asyncio.Lock()
        async with self.__queue_channels_locks[topic]:
            self.__queue_channels[topic] = dict()

    async def createQueueChannel(self, topic: str) -> int:
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        id = None
        async with self.__ids_lock:
            id = self.__max_id_4_topic[topic]
            self.__max_id_4_topic[topic] += 1
        async with self.__queue_channels_locks[topic]:
            self.__queue_channels[topic][id] = AsyncQueue()
        return id

    async def removeQueueChannel(self, topic: str, id: int):
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        async with self.__queue_channels_locks[topic]:
            self.__queue_channels[topic].pop(id)

    async def publishMessage(self, topic: str, message: str):
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        async with self.__queue_channels_locks[topic]:
            for queue_channel in self.__queue_channels[topic].values():
                await queue_channel.push(message)

    async def retrieveMessage(self, topic: str, queue_channel_id: int) -> str:
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        async with self.__queue_channels_locks[topic]:
            return await self.__queue_channels[topic][int(queue_channel_id)].pop()
