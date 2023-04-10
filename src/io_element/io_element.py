'''IOElement class module'''
import logging
from typing import Dict, Union
import threading
from queue import Queue

# pylint: disable=no-name-in-module
from google.protobuf.message import Message
from google.protobuf.timestamp_pb2 import Timestamp

class IOElement:
    '''
    IOElement class to receive data from another IOElement,
    process the incoming data and publish the processed data
    to any subscriber elements.
    '''
    def __init__(self, name: str, topic: str, async_loop: bool = False) -> None:
        self.name = name
        self.topic = topic
        self.async_loop = async_loop
        self.input_queue = Queue()
        self.stop_flag = False
        self.streaming_thread = None
        self.timestamp = Timestamp()
        self.subscribers = []

    def start_stream(self) -> None:
        '''Method to start data stream.'''
        logging.debug(f'{self.name}: Starting data stream...')
        if self.async_loop:
            self.streaming_thread = threading.Thread(target=self._a_streaming_loop)
        else:
            self.streaming_thread = threading.Thread(target=self._streaming_loop)

        self.streaming_thread.start()
        logging.info(f'{self.name}: Data stream started.')

    def stop_stream(self) -> None:
        '''Method to stop data stream.'''
        logging.debug(f'{self.name}: Stopping data stream.')
        self.stop_flag = True
        self.streaming_thread.join()
        logging.info(f'{self.name}: Data stream stopped.')

    def _streaming_loop(self) -> None:
        '''Method to perform while loop calling _stream_task() method'''
        while not self.stop_flag:
            message = self._stream_task()
            if message is not None:
                if isinstance(message, dict):
                    for key, msg in message.items():
                        self._publish_to_subscribers(msg, topic=f'{self.topic}/{key}')
                elif isinstance(message, Message):
                    self._publish_to_subscribers(message)

    async def _a_streaming_loop(self) -> None:
        '''Method to perform while loop calling _stream_task() method'''
        while not self.stop_flag:
            message = self._stream_task()
            if message is not None:
                self._publish_to_subscribers(message)

    def _stream_task(self) -> Message|None:
        '''Method of the task to perform during the datastream process.'''
        raise NotImplementedError('Please add this function to your child class.')

    def add_subscriber(self, other_io_element) -> None:
        '''Add another IOElement instance as a subscriber.'''
        self.subscribers.append(other_io_element)

    def _publish_to_subscribers(self, message: Message, topic: str = None) -> None:
        '''Publish messages to subscribers.'''
        # Define topic
        if topic is None:
            topic = self.topic

        # Publish message to all subscribers
        for subscriber in self.subscribers:
            subscriber.input_queue.put((topic, message))
