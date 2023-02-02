import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

while True:
    time.sleep(0.001)
    accel_x, accel_y, accel_z = bno.acceleration
    print("Acceleration: X: %0.6f Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    quat_w, quat_i, quat_j, quat_k = bno.quaternion
    print("Orientation:  W: %0.6f I: %0.6f J: %0.6f K: %0.6f" % (quat_w, quat_i, quat_j, quat_k))
    print("")

    # print("Gyro:")
    # gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
    # print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
    # print("")

    # print("Rotation Vector Quaternion:")
    # quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
    # print(
    #     "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    # )
    # print("")