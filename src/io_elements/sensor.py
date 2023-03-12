'''Module for sensor class'''
import logging

from google.protobuf.timestamp_pb2 import Timestamp

from .io_element import IOElement, IOElementType

class Sensor(IOElement):
    '''Sensor class'''
    def __init__(self, name: str, group: str) -> None:
        super().__init__(IOElementType.PIPELINE_INPUT)

        self.name = name
        self.group = group
        self.connection = None
        self.read_source = None
        self.timestamp = Timestamp()
        self.add_run_requirement('connected')

    async def connect(self) -> None:
        '''Open connection with sensor'''
        if self.run_requirements['connected']:
            logging.warning(f'{self.name}: Already connected.')
            return

        logging.info(f'{self.name}: Connecting to sensor...')

    async def disconnect(self) -> None:
        '''Close connection with sensor'''
        if not self.run_requirements['connected']:
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
            self.run_requirements['connected'] = False
            logging.info(f'{self.name}: Successfully disconnected.')
        except Exception as exc:
            raise ConnectionError(f'{self.name}: Unable to close connection.') from exc

    async def process_data(self, *args, **kwargs):
        '''
        Process data. This function is meant to be overwritten by the
        child class's implementation.
        '''
        raise NotImplementedError("This function hasn't been implemented.")
