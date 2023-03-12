'''Live Streamer class module'''
from .io_element import IOElement, IOElementType

class LiveStreamer(IOElement):
    '''Class to livestream input data to Foxglove instance.'''
    def __init__(self, name: str):
        super().__init__(IOElementType.PIPELINE_IO)
        self.name = name
