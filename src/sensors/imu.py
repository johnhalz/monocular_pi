from serial import Serial
from adafruit_bno08x_rvc import BNO08x_RVC
from pose3d import ET, ER
import logging

from .sensor import Sensor

class IMU(Sensor):
    def __init__(self, name: str,
                       sensor_type: str = 'imu',
                       serial_port: str = '/dev/serial0',
                       baudrate: int = 115200) -> None:
        super().__init__(name, sensor_type)
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.orientation = ER(name='IMU Orientation')

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
        self.timestamp.GetCurrentTime()
        yaw, pitch, roll, x_accel, y_accel, z_accel = self.read_source.heading
        logging.debug('Got IMU data')
        self.orientation.from_euler('zyx', [yaw, pitch, roll], degrees=True)
        quat = self.orientation.as_quat()

        return self.timestamp, (x_accel, y_accel, z_accel, quat[0], quat[1], quat[2], quat[3])
