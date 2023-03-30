'''IMU sensor module'''
import logging
from serial import Serial

import numpy as np
from pose3d import ER
from adafruit_bno08x_rvc import BNO08x_RVC

from pathlib import Path
from sys import path
path.append(Path(__file__).parents[1].as_posix())

from io_element import Sensor, Message
from messages import Vector3, Quaternion

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

    def _stream_task(self) -> list(Message):
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
        quat_msg = self._compile_quaternion_data()
        acc_msg = self._compile_acceleration_data(
            acceleration=np.array([x_accel, y_accel, z_accel])
        )
        return [acc_msg, quat_msg]

    def _compile_acceleration_data(self, acceleration: np.ndarray) -> Vector3:
        '''
        Compile acceleration data to timestamped Vector3 protobuf message.

        Parameters
        ----------
        - `acceleration` (`np.ndarray`): Acceleration array

        Returns
        -------
        - `Vector3`: Vector3 protobuf message instance
        '''
        return Vector3(
            x=acceleration[0],
            y=acceleration[1],
            z=acceleration[2],
            timestamp=self.timestamp.ToNanoseconds()
        )

    def _compile_quaternion_data(self) -> Quaternion:
        '''
        Compile orientation data to timestamped Quaternion protobuf message.

        Returns
        -------
        - `Quaternion`: Quaternion protobuf message instance
        '''
        quat = self.orientation.as_quat()
        return Quaternion(
            w=quat[0],
            x=quat[1],
            y=quat[2],
            z=quat[3],
            timestamp=self.timestamp.ToNanoseconds()
        )
