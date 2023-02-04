from serial import Serial
from adafruit_bno08x_rvc import BNO08x_RVC
from pose3d import ET, ER

from .sensor import Sensor

class IMU(Sensor):
    def __init__(self, name: str,
                       serial_port: str = '/dev/serial0',
                       baudrate: int = 115200) -> None:
        super().__init__(name)
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.acceleration = ET(name='IMU Acceleration')
        self.orientation = ER(name='IMU Orientation')

    def connect(self) -> None:
        '''
        Connect to IMU.
        '''
        self.connection = Serial(self.serial_port, self.baudrate)
        self.read_source = BNO08x_RVC(self.connection)
        self.connected = True

    def disconnect(self) -> None:
        '''
        Disconnect from IMU.
        '''
        self.connection.close()
        self.connected = False

    def __read_data(self) -> None:
        '''
        Read data from IMU
        '''
        yaw, pitch, roll, x_accel, y_accel, z_accel = self.read_source.heading
        self.acceleration.from_vector([x_accel, y_accel, z_accel])
        self.orientation.from_euler('zyx', [yaw, pitch, roll], degrees=True)
