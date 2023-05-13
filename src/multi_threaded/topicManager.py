from threading import Lock

class TopicManager:
    def __init__(self):
        self.__topics = set()
        self.__topics_lock = Lock()

    def new(self, topic: str):
        if self.exists(topic):
            raise Exception(f"Topic named {topic} already exists")
        with self.__topics_lock:
            self.__topics.add(topic)

    def remove(self, topic: str):
        if not self.exists(topic):
            raise Exception(f"There is no topic named: {topic}")
        with self.__topics_lock:
            self.__topics.remove(topic)

    def exists(self, topic: str):
        with self.__topics_lock:
            return topic in self.__topics
