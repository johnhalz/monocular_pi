import logging
import cv2
from .sensor import Sensor, time, Any

class Camera(Sensor):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def connect(self) -> None:
        super().connect()
        try:
            self.read_source = cv2.VideoCapture(0)
            self.connection = self.read_source
            self.connected = True
            logging.info(f'{self.name}: Successfully connected.')
        except Exception as exc:
            raise ConnectionError(f'Unable to connect to {self.name}.') from exc

    def __read_data(self) -> tuple[int, Any]:
        timestamp = time.perf_counter_ns()
        success, data = self.read_source.read()
        if not success:
            return timestamp, None

        logging.debug('Got camera data')
