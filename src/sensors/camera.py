'''Camera sensor module'''
import logging
from typing import Dict
from time import sleep

import cv2
import numpy as np
from io_element import Sensor, Message
from messages import CompressedImage

# pylint: disable=too-few-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-member
class Camera(Sensor):
    '''Camera sensor class'''
    def connect(self) -> None:
        '''Connect to camera'''
        super().connect()
        try:
            if not self.simulated:
                self.connection = cv2.VideoCapture(0)
            else:
                self.connection = cv2.VideoCapture(self.simulation_file.as_posix())
                self.sim_fps = self.connection.get(cv2.CAP_PROP_FPS)

            self.connected = True
            logging.info(f'{self.name}: Successfully connected.')
        except Exception as exc:
            raise ConnectionError(f'{self.name}: Unable to connect.') from exc

    def _stream_task(self) -> Dict[str, Message]:
        '''
        Read data from camera, take timestamp and create protobuf message

        Returns
        -------
        -`Message`: CompressedImage (protobuf message)
        '''
        # If Simulated - Simulate framerate of input video
        if self.simulated:
            sleep(1./self.sim_fps)

        self.timestamp.GetCurrentTime()
        success, image = self.connection.read()
        if not success:
            return self.timestamp, None

        logging.debug(f'{self.name}: Got camera data')

        return {'image': self._compile_message(image)}

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
