'''Sensor class module'''
import logging
from typing import Union, Dict

from .io_element import IOElement, Message

class Sensor(IOElement):
    '''
    Sensor class (child class of IOElement)
    '''
    def __init__(self, name: str, topic: str) -> None:
        super().__init__(name, topic)
        self.connection = None
        self.read_source = None
        self.connected: bool = False

    def connect(self) -> None:
        '''Method to connect to sensor.'''
        if self.connected:
            logging.debug(f'{self.name}: Already connected.')
            return

        logging.debug(f'{self.name}: Connecting to sensor...')

    def disconnect(self) -> None:
        '''Method to disconnect from sensor.'''
        if not self.connected:
            logging.debug(f'{self.name}: Already disconnected.')
            return

        logging.debug(f'{self.name}: Disconnecting from sensor...')
        try:
            if hasattr(self.connection, 'close'):
                self.connection.close()
            elif hasattr(self.connection, 'release'):
                self.connection.release()
            else:
                raise AttributeError(
                    f'{self.name}: Aborting - Unknown method to close connection.'
                )

            self.connected = False
            logging.info(f'{self.name}: Successfully disconnected.')

        except Exception as exc:
            raise ConnectionError(f'{self.name}: Unable to close connection.') from exc

    def _stream_task(self) -> Union[Dict[str, Message], Message, None]:
        '''Method of the task to perform during the datastream process.'''
        raise NotImplementedError('Please add this function to your child class.')

    def _compile_message(self, data: any) -> Union[Message, None]:
        '''Compile sensor data into message'''
