'''
Module to hold the IOElement class.
'''
from queue import Queue
import logging
from enum import Enum

class IOElementType(Enum):
    '''Class to define IOElement type'''
    PIPELINE_INPUT = 1
    PIPELINE_OUTPUT = 2
    PIPELINE_IO = 3

class IOElement:
    '''
    IOElement is meant to be a general class that can take in elements,
    from an ipnut queue, process data, and output the processed data to
    a output queue.
    '''
    def __init__(self, element_type: IOElementType|int = IOElementType.PIPELINE_IO):
        self.name = None
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.is_running = False
        self.type = element_type
        self.run_requirements = {}

    async def process_data(self, *args, **kwargs):
        '''
        Process data. This function is meant to be overwritten by the
        child class's implementation.
        '''
        raise NotImplementedError("This function hasn't been implemented.")

    async def run_loop(self):
        '''Run loop for IOElement'''
        # Check if any run requirements are false
        if self._any_invalid_requirements():
            logging.error(f'{self.name}: Unable to start running loop: \n{self.run_requirements}')
            return

        # Start loop depending on IOElement type
        logging.info(f'{self.name}: Starting run loop...')
        self.is_running = True
        logging.info(f'{self.name}: Stream run loop.')
        if self.type is IOElementType.PIPELINE_INPUT:
            while self.is_running:
                processed_data = await self.process_data()
                await self.output_queue.put(processed_data)
        elif self.type is IOElementType.PIPELINE_OUTPUT:
            while self.is_running:
                data = await self.input_queue.get()
                await self.process_data(data)
        else:
            while self.is_running:
                data = await self.input_queue.get()
                processed_data = await self.process_data(data)
                await self.output_queue.put(processed_data)

    def stop_stream(self) -> None:
        '''Stop running stream loop.'''
        logging.info(f'{self.name}: Stopping stream...')
        self.is_running = False
        logging.info(f'{self.name}: Running stopped.')

    def add_run_requirement(self, name: str):
        '''Add requirement to start run_loop.'''
        self.run_requirements[name] = False

    def _any_invalid_requirements(self) -> bool:
        '''Check if any elements of the run_requirements are false.'''
        for value in self.run_requirements.values():
            if not value:
                return True

        return False
