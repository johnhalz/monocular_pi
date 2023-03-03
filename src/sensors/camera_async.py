import logging

import cv2
import numpy as np
from .sensor_async import ASensor

from sys import path
from pathlib import Path
path.append(Path(__file__).parents[1].as_posix())

from src.recorder.foxglove.CompressedImage_pb2 import CompressedImage

class ACamera(ASensor):
    def __init__(self, name: str, sensor_type: str = 'camera') -> None:
        super().__init__(name, sensor_type)

    async def connect(self) -> None:
        super().connect()
        try:
            self.read_source = cv2.VideoCapture(0)
            self.connection = self.read_source
            self.connected = True
            logging.info(f'{self.name}: Successfully connected.')
        except Exception as exc:
            raise ConnectionError(f'Unable to connect to {self.name}.') from exc

    async def _read_data(self) -> tuple[int, np.ndarray | None]:
        self.timestamp.GetCurrentTime()
        success, image = self.read_source.read()
        if not success:
            return self.timestamp, None

        logging.debug('Got camera data')
        return self.timestamp, image

    @staticmethod
    def package_data(timestamp, data, encoding: str = 'jpeg') -> CompressedImage:
        success, enc_img = cv2.imencode(f'.{encoding}', data)
        if not success:
            return None

        byte_img = enc_img.tobytes()
        message = CompressedImage()

        message.timestamp.CopyFrom(timestamp)
        message.frame_id = ''
        message.format = encoding
        message.data = byte_img

        return message
