import asyncio
from typing import Awaitable, Callable

import aio_pika


class RabbitMQConsumer:
    def __init__(
        self,
        connection: aio_pika.Connection,
        queue_name: str,
        callback: Callable[[aio_pika.IncomingMessage], Awaitable[None]],
    ):
        self.connection = connection
        self.queue_name = queue_name
        self.callback = callback

        self.task = None

    async def consume(self):
        await self.connection.connect()
        async with self.connection.channel() as channel:
            queue = await channel.declare_queue(
                self.queue_name,
                durable=True,
            )
            await queue.consume(self.callback)
            await asyncio.Future()

    async def start(self) -> None:
        self.task = asyncio.create_task(self.consume())

    async def stop(self) -> None:
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
