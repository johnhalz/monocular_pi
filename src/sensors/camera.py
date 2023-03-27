'''Camera sensor module'''
import logging

import cv2
import numpy as np
from io_element import Sensor, Message
from messages import CompressedImage

# pylint: disable=too-few-public-methods
class Camera(Sensor):
    '''Camera sensor class'''
    def __init__(self, name: str, topic: str = 'camera') -> None:
        super().__init__(name, topic)

    def connect(self) -> None:
        super().connect()
        try:
            self.connection = cv2.VideoCapture(0)
            self.read_source = self.connection
            self.connected = True
            logging.info(f'{self.name}: Successfully connected.')
        except Exception as exc:
            raise ConnectionError(f'{self.name}: Unable to connect.') from exc

    def _stream_task(self) -> Message:
        '''
        Read data from camera, take timestamp and create protobuf message

        Returns
        -------
        -`Message`: CompressedImage (protobuf message)
        '''
        self.timestamp.GetCurrentTime()
        success, image = self.read_source.read()
        if not success:
            return self.timestamp, None

        logging.debug(f'{self.name}: Got camera data')

        return self._compile_message(image)

    def _compile_message(self, img_data: np.ndarray, encoding: str = 'jpeg') -> CompressedImage:
        '''
        Compile image data into protobuffer message

        Parameters
        ----------
        - `img_data` (`np.ndarray`): Image data
        - `encoding` (`str`): Encoding setting (default: 'jpeg')

        Returns
        -------
        -`CompressedImage`: CompressedImage (protobuf message)
        '''
        success, enc_img = cv2.imencode(f'.{encoding}', img_data)
        if not success:
            return None

        byte_img = enc_img.tobytes()
        message = CompressedImage()

        message.timestamp.CopyFrom(self.timestamp)
        message.frame_id = ''
        message.format = encoding
        message.data = byte_img

        return message
