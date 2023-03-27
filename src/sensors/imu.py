'''IMU sensor module'''
import logging
from serial import Serial

import numpy as np
from pose3d import ER
from adafruit_bno08x_rvc import BNO08x_RVC
from io_element import Sensor, Message
from messages import IMUMessage

# pylint: disable=too-few-public-methods
class IMU(Sensor):
    '''IMU sensor class'''
    def __init__(self, name: str,
                       topic: str = 'imu',
                       serial_port: str = '/dev/serial0',
                       baudrate: int = 115200) -> None:
        super().__init__(name, topic)
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
            raise ConnectionError(f'{self.name}: Unable to connect.') from exc

    def _stream_task(self) -> Message:
        '''
        Read data from IMU, take timestamp and create protobuf message

        Returns
        -------
        -`Message`: IMUMessage (protobuf message)
        '''
        self.timestamp.GetCurrentTime()
        yaw, pitch, roll, x_accel, y_accel, z_accel = self.read_source.heading
        logging.debug(f'{self.name}: Got IMU data')
        self.orientation.from_euler('zyx', [yaw, pitch, roll], degrees=True)
        return self._compile_message(acceleration=np.array([x_accel, y_accel, z_accel]))

    def _compile_message(self, acceleration: np.ndarray) -> IMUMessage:
        '''
        Compile data into protobuffer message

        Parameters
        ----------
        - `acceleration` (`np.ndarray`): Acceleration data

        Returns
        -------
        -`IMUMessage`: IMUMessage (protobuf message)
        '''
        quaternion = self.orientation.as_quat()
        return IMUMessage(
            accel_x = acceleration[0],
            accel_y = acceleration[1],
            accel_z = acceleration[2],
            orient_w = quaternion[0],
            orient_i = quaternion[1],
            orient_j = quaternion[2],
            orient_k = quaternion[3]
        )
