'''Mcap Reocrde class module'''
from .io_element import IOElement, IOElementType

class McapRecorder(IOElement):
    '''IOElement class to record input protobuf messages to mcap file.'''
    def __init__(self, name: str):
        super().__init__(IOElementType.PIPELINE_OUTPUT)
        self.name = name
