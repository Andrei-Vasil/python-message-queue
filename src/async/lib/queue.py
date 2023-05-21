import asyncio
from typing import TypeVar, Generic
from collections import deque

from benchmark.benchmark import mark_end_of_push

T = TypeVar('T')

class AsyncQueue(Generic[T]):
    def __init__(self) -> None:
        self.__items: deque[T] = deque([])
        self.__condition = asyncio.Condition()
    
    async def push(self, item: T, benchmark_id: str) -> None:
        self.__items.append(item)
        async with self.__condition:
            self.__condition.notify()
        mark_end_of_push(benchmark_id)

    async def pop(self) -> T:
        async with self.__condition:
            while len(self.__items) == 0:
                await self.__condition.wait()
        return self.__items.popleft()
