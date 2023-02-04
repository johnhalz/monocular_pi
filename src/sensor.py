import queue
import logging
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
            logging.debug(f'{self.name}: Already connected.')
        logging.debug(f'{self.name}: Connecting to sensor...')
        pass

    def disconnect(self) -> None:
        '''
        Method to disconnect to sensor
        '''
            logging.debug(f'{self.name}: Already disconnected.')
        logging.debug(f'{self.name}: Disonnecting from sensor...')
        try:
                raise AttributeError(f'{self.name}: Aborting - Unknown method to close connection.')
            self.connected = False
            logging.info(f'{self.name}: Successfully disconnected.')
        except Exception as exc:
            raise ConnectionError(f'{self.name}: Unable to close connection.') from exc

    def start_stream(self) -> None:
        '''
        Method to start data stream
        '''
        logging.debug(f'{self.name}: Starting stream...')
        self.streaming_thread = threading.Thread(target=self.__streaming_loop)
        self.streaming_thread.start()
        logging.info(f'{self.name}: Stream started.')

    def stop_stream(self) -> None:
        '''
        Method to stop stream
        '''
        logging.debug(f'{self.name}: Stopping stream...')
        self.stop_flag = True
        self.streaming_thread.join()
        logging.info(f'{self.name}: Stream stopped.')

    def __streaming_loop(self):
        '''
        Method to perform while loop calling __read_data
        '''
        while not self.stop_flag:
            timestamp, data = self.__read_data()
            self.data_queue.put((timestamp, data))

    def __read_data(self) -> tuple[int, Any]:
        pass

    def __process_data(self) -> None:
        pass
