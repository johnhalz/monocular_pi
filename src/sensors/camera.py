import logging
import cv2
import numpy as np
from .sensor import Sensor

class Camera(Sensor):
    def __init__(self, name: str, sensor_type: str = 'camera') -> None:
        super().__init__(name, sensor_type)

    def connect(self) -> None:
        super().connect()
        try:
            self.read_source = cv2.VideoCapture(0)
            self.connection = self.read_source
            self.connected = True
            logging.info(f'{self.name}: Successfully connected.')
        except Exception as exc:
            raise ConnectionError(f'Unable to connect to {self.name}.') from exc

    def _read_data(self) -> tuple[int, np.ndarray | None]:
        self.timestamp.GetCurrentTime()
        success, image = self.read_source.read()
        if not success:
            return self.timestamp, None

        logging.debug('Got camera data')
        return self.timestamp, image
