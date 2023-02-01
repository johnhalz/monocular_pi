import serial
from adafruit_bno08x_rvc import BNO08x_RVC

from pose3d import ET, ER

__VALID_CONNECTION_METHODS = ['uart', 'uart_rvc', 'i2c']

class IMU:
    def __init__(self, method: str, connect_immediately: bool = True) -> None:
        self.connection_method = method

        if connect_immediately:
            self.connect()
    
    def connect(self) -> None:
        match self.connection_method:
            case 'uart_rvc':
                self.connection = serial.Serial("/dev/serial0", 115200)
                self.device = BNO08x_RVC(self.connection)
            case 'uart':
                pass
            case 'i2c':
                pass
            case _:
                raise ValueError(f'Input connection method {self.connection_method} is \
                    not valid. Choose one of the following: {__VALID_CONNECTION_METHODS}.')

    def stream(self) -> None:
        self.acceleration = ET(name='Acceleration')
        self.orientation = ER(name='Orientation')
        pass

    def get_data_uart_rvc(self):
        yaw, pitch, roll, x_accel, y_accel, z_accel = self.device.heading
        self.acceleration.from_vector([x_accel, y_accel, z_accel])
        self.orientation.from_euler('zyx', angles=[yaw, pitch, roll], degrees=True)

    def get_data_uart(self):
        pass

    def get_data_i2c(self):
        pass