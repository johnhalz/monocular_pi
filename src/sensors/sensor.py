import queue
import logging
import threading
from google.protobuf.timestamp_pb2 import Timestamp

class Sensor:
    def __init__(self, name: str, sensor_type: str) -> None:
        self.name = name
        self.sensor_type = sensor_type
        self.connection = None
        self.read_source = None
        self.connected = False
        self.data_queue = queue.Queue()
        self.stop_flag = False
        self.streaming_thread = None
        self.timestamp = Timestamp()

    def connect(self) -> None:
        '''
        Method to connect to sensor
        '''
        if self.connected:
            logging.debug(f'{self.name}: Already connected.')
            return

        logging.debug(f'{self.name}: Connecting to sensor...')

    def disconnect(self) -> None:
        '''
        Method to disconnect to sensor
        '''
        if not self.connected:
            logging.debug(f'{self.name}: Already disconnected.')
            return

        logging.debug(f'{self.name}: Disonnecting from sensor...')
        try:
            if hasattr(self.connection, 'close'):
                self.connection.close()
            elif hasattr(self.connection, 'release'):
                self.connection.release()
            else:
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
        self.data_queue.put(None)
        self.streaming_thread.join()
        logging.info(f'{self.name}: Stream stopped.')

    def __streaming_loop(self) -> None:
        '''
        Method to perform while loop calling __read_data
        '''
        while not self.stop_flag:
            timestamp, data = self._read_data()
            self.data_queue.put((timestamp, data))

    def _read_data(self):
        logging.warning(f'{self.name}: Not receiving any data')
        self.timestamp.GetCurrentTime()
        return self.timestamp, None
