'''Log handler module'''
import logging
from datetime import datetime

from .io_element import IOElement
from messages import Log
from google.protobuf.timestamp_pb2 import Timestamp

class LogHandler(logging.Handler):
    '''
    LogHandler Class - Created so that log messages are recorded and
    can be seen in Foxglove Studio
    '''
    def __init__(self):
        super().__init__()
        self.timestamp = Timestamp()
        self.topic = 'logger'
        self.subscribers = []

    def emit(self, record: logging.LogRecord) -> None:
        message = self._compile_message(record)
        for subscriber in self.subscribers:
            subscriber.input_queue.put((self.topic, message))

    def add_subscriber(self, other_io_element: IOElement) -> None:
        '''
        Add subscriber to list.

        Parameters
        ----------
        - `other_io_element` (`IOElement`): IOElement to add as subscriber
        '''
        self.subscribers.append(other_io_element)

    def _compile_message(self, data: logging.LogRecord) -> Log:
        '''
        Compile log message to protobug message.

        Parameters
        ----------
        - `data` (`logging.LogRecord`): Log record (of a single logging message)

        Returns
        -------
        - `Log`: Log message in protobuf format (compatible with Foxglove)
        '''
        message = Log()
        self.timestamp.FromDatetime(datetime.fromtimestamp(data.created))
        message.timestamp.CopyFrom(self.timestamp)
        message.file = data.filename
        message.line = data.lineno
        message.message = data.getMessage()
        message.level = data.levelname
        message.name = data.processName

        return message
