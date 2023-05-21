from typing import TypeVar, Generic
from collections import deque
import queue
import threading

import sys, os
sys.path.append(os.path.abspath(os.path.join('src')))
from benchmark.benchmark import mark_end_of_push

T = TypeVar('T')

class MultiThreadedQueue(Generic[T]):
    def __init__(self) -> None:
        self.__consumer_queue = queue.Queue()
        self.__items: deque[T] = deque([])
        self.__lock = threading.Lock()
        self.__condition = threading.Condition()
        self.__threads = []
        self.__daemon_queue = queue.Queue()
        self.__daemon_thread = threading.Thread(target=self.__daemon)
        self.__daemon_thread.start()
    
    def __daemon(self) -> None:
        while True:
            try:
                self.__daemon_queue.get_nowait()
                return
            except Exception:
                for (thread, q) in self.__threads:
                    try:
                        q.get_nowait()
                        thread.join()
                    except Exception:
                        pass

    def __push(self, item: T, q: queue.Queue, benchmark_id: str) -> None:
        with self.__lock:
            self.__items.append(item)
        with self.__condition:
            self.__condition.notify()
        mark_end_of_push(benchmark_id)
        q.put(True)
    
    def push(self, item: T, benchmark_id: str) -> None:
        q = queue.Queue()
        thread = threading.Thread(target=self.__push, args=(item, q, benchmark_id,))
        self.__threads.append((thread, q))
        thread.start()
        
    def __pop(self, q: queue.Queue) -> T:
        with self.__condition:
            while len(self.__items) == 0:
                self.__condition.wait()
            with self.__lock:
                self.__consumer_queue.put(self.__items.popleft())
        q.put(True)

    def pop(self) -> T:
        q = queue.Queue()
        thread = threading.Thread(target=self.__pop, args=(q,))
        self.__threads.append((thread, q))
        thread.start()
        return self.__consumer_queue.get()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.__daemon_queue.put(True)
        self.__daemon_thread.join()
