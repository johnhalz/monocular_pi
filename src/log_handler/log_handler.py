import logging
from queue import Queue
from google.protobuf.timestamp_pb2 import Timestamp

class LogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.data_queue = Queue()
        self.timestamp = Timestamp()

    def emit(self, record: logging.LogRecord):
        self.timestamp.GetCurrentTime()
        self.data_queue.put((self.timestamp, record))
