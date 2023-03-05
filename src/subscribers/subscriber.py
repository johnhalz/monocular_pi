import logging
import asyncio

class Subscriber:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def process_data(self, data):
        # do something with data, e.g. make a network request or write to a file
        await asyncio.sleep(1)
        logging.info(f"Processed data: {data}")

    async def get_data(self):
        data = await self.queue.get()
        await self.process_data(data)
