import asyncio
from typing import TypeVar, Generic, List
from collections import deque

T = TypeVar('T')

class AsyncQueue(Generic[T]):
    def __init__(self) -> None:
        self.__items: deque[T] = deque([])
        self.__condition = asyncio.Condition()
    
    async def push(self, item: T) -> None:
        self.__items.append(item)
        async with self.__condition:
            self.__condition.notify()

    async def pop(self) -> T:
        async with self.__condition:
            while len(self.__items) == 0:
                await self.__condition.wait()
        return self.__items.popleft()
