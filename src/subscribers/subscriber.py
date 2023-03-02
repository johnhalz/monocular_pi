import asyncio
import logging
import queue
from google.protobuf.timestamp_pb2 import Timestamp

class Subscriber:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_receiving = False
        self.data_queue = queue.Queue()

    def receive_data(self):
        pass

    async def start(self):
        '''Start receiving data from source(s).'''
        pass

    def stop(self):
        '''Stop receiving data from source(s).'''
        self.is_receiving = False
