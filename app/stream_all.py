from time import sleep
from sys import path
from pathlib import Path
import logging

path.append(Path(__file__).parents[1].as_posix())

from src.sensors import IMU, Camera

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='example.log',
        format=('[%(asctime)s] %(levelname)-9s %(message)s')
    )
    camera = Camera(name='raspi-cam')
    imu = IMU(name='bno085')

    camera.connect()
    imu.connect()

    camera.start_stream()
    imu.start_stream()

    sleep(2)

    camera.stop_stream()
    imu.stop_stream()

    camera.disconnect()
    imu.disconnect()

if __name__ == '__main__':
    main()
