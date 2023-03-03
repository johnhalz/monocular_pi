import logging

class Subscriber:
    def __init__(self, name: str, require_pb_message: bool = False) -> None:
        self.name = name
        self.require_pb_message = require_pb_message

    async def receive_data(self, data):
        '''Receive data from publishers.'''
        raise NotImplementedError
