import asyncio
from typing import TypeVar, Generic
from collections import deque

import sys, os
sys.path.append(os.path.abspath(os.path.join('src')))
from benchmark.benchmark import count_consumer_throughput, count_producer_throughput, mark_end_of_push

T = TypeVar('T')

class AsyncQueue(Generic[T]):
    def __init__(self) -> None:
        self.__items: deque[T] = deque([])
        self.__condition = asyncio.Condition()
    
    async def push(self, item: T, benchmark_id: str, scenario_id: str) -> None:
        self.__items.append(item)
        async with self.__condition:
            self.__condition.notify()
        mark_end_of_push(benchmark_id, scenario_id)
        count_producer_throughput(scenario_id)

    async def pop(self, scenario_id: str) -> T:
        async with self.__condition:
            while len(self.__items) == 0:
                await self.__condition.wait()
        count_consumer_throughput(scenario_id)
        return self.__items.popleft()
