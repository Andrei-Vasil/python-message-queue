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
        async with self.__ids_lock.acquire():
            self.__max_id_4_topic.pop(topic)
        async with self.__queue_channels_locks.get(topic, asyncio.Lock()).acquire():
            self.__queue_channels.pop(topic)
        self.__queue_channels_locks.pop(topic)

    async def createQueueChannel(self, topic: str) -> int:
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        id = None
        async with self.__ids_lock.acquire():
            self.__max_id_4_topic[topic] = self.__max_id_4_topic.get(topic, -1) + 1
            id = self.__max_id_4_topic[topic]
        async with self.__queue_channels_locks.get(topic, asyncio.Lock()).acquire():
            self.__queue_channels[topic][id] = AsyncQueue()
        return id

    async def removeQueueChannel(self, topic: str, id: int):
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        async with self.__queue_channels_locks.get(topic, asyncio.Lock()).acquire():
            self.__queue_channels[topic].pop(id)

    async def publishMessage(self, topic: str, message: str):
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        async with self.__queue_channels_locks.get(topic, asyncio.Lock()).acquire():
            for queue_channel in self.__queue_channels[topic].values():
                queue_channel.push(message)

    async def retrieveMessage(self, topic: str, queue_channel_id: int) -> str:
        if not await self.__topicManager.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        async with self.__queue_channels_locks.get(topic, asyncio.Lock()).acquire():
            return await self.__queue_channels[topic][queue_channel_id].pop()
