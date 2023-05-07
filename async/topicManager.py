
class TopicManager:
    def __init__(self):
        self.__topics = set()

    async def new(self, topic: str):
        if self.exists(topic):
            raise Exception(f"Topic named {topic} already exists")
        self.__topics.add(topic)

    async def remove(self, topic: str):
        if not self.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        self.__topics.remove(topic)

    async def exists(self, topic: str):
        return topic in self.__topics
