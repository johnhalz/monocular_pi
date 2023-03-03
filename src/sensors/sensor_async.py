import logging
from google.protobuf.timestamp_pb2 import Timestamp

class ASensor:
    def __init__(self, name: str, sensor_type: str) -> None:
        self.name = name
        self.sensor_type = sensor_type
        self.connection = None
        self.read_source = None
        self.is_reading = False
        self.connected = False
        self.timestamp = Timestamp()
        self.subscribers = []

    async def connect(self) -> None:
        '''Connect to sensor'''
        if self.connected:
            logging.warning(f'{self.name}: Already connected.')
            return

        logging.info(f'{self.name}: Connecting to sensor...')

    async def disconnect(self) -> None:
        '''Disconnect from sensor'''
        if not self.connected:
            logging.warning(f'{self.name}: Already disconnected.')
            return

        logging.info(f'{self.name}: Disonnecting from sensor...')
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

    async def _read_data(self):
        logging.warning(f'{self.name}: Not receiving any data')
        self.timestamp.GetCurrentTime()
        return self.timestamp, None

    async def start_stream(self) -> None:
        '''Start reading data from sensor.'''
        if not self.connected:
            logging.error(f'{self.name}: Unable to start streaming data - Sensor not connected.')
            return

        logging.info(f'{self.name}: Starting stream...')
        self.is_reading = True
        logging.info(f'{self.name}: Stream started.')
        while self.is_reading:
            result = await self._read_data()

            for subscriber in self.subscribers:
                subscriber.receive_data(result)

    def stop_stream(self) -> None:
        '''Stop reading data from sensor'''
        logging.info(f'{self.name}: Stopping stream...')
        self.is_reading = False
        logging.info(f'{self.name}: Streaming stopped.')

    def add_subscriber(self, subscriber):
        '''Add new subscriber to '''
        self.subscribers.append(subscriber)
