import queue
import time
import threading
from typing import Any

class Sensor:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connection = None
        self.read_source = None
        self.connected = False
        self.data_queue = queue.Queue()
        self.stop_flag = False
        self.streaming_thread = None

    def connect(self) -> None:
        '''
        Method to connect to sensor
        '''
        pass

    def disconnect(self) -> None:
        '''
        Method to disconnect to sensor
        '''
        try:
            self.connection.close()
            self.connected = False
        except Exception as exc:
            raise ConnectionError('Unable to close connection.') from exc

    def start_stream(self) -> None:
        '''
        Method to start data stream
        '''
        self.streaming_thread = threading.Thread(target=self.__streaming_loop)
        self.streaming_thread.start()

    def stop_stream(self) -> None:
        '''
        Method to stop stream
        '''
        self.stop_flag = True
        self.streaming_thread.join()

    def __streaming_loop(self):
        '''
        Method to perform while loop calling __read_data
        '''
        while not self.stop_flag:
            timestamp, data = self.__read_data()
            self.data_queue.put((timestamp, data))

    def __read_data(self) -> tuple[int, Any]:
        data = None
        timestamp = time.perf_counter_ns()
        return timestamp, data

    def __process_data(self) -> None:
        pass
