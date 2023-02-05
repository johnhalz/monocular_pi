from time import perf_counter_ns
from serial import Serial
from adafruit_bno08x_rvc import BNO08x_RVC
from pose3d import ET, ER
import logging

from .sensor import Sensor

class IMU(Sensor):
    def __init__(self, name: str,
                       serial_port: str = '/dev/serial0',
                       baudrate: int = 115200) -> None:
        super().__init__(name)
        self.serial_port = serial_port
        self.baudrate = baudrate

    def connect(self) -> None:
        '''
        Connect to IMU.
        '''
        super().connect()
        try:
            self.connection = Serial(self.serial_port, self.baudrate)
            self.read_source = BNO08x_RVC(self.connection)
            self.connected = True
            logging.info(f'{self.name}: Successfully connected.')
        except Exception as exc:
            raise ConnectionError(f'Unable to connect to {self.name}.') from exc

    def _read_data(self) -> tuple[int, tuple[ET, ER]]:
        '''
        Read data from IMU
        '''
        timestamp = perf_counter_ns()
        acceleration = ET(name='IMU Acceleration')
        orientation = ER(name='IMU Orientation')
        yaw, pitch, roll, x_accel, y_accel, z_accel = self.read_source.heading
        logging.debug('Got IMU data')
        acceleration.from_vector([x_accel, y_accel, z_accel])
        orientation.from_euler('zyx', [yaw, pitch, roll], degrees=True)

        return timestamp, (acceleration, orientation)
