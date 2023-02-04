from time import sleep
from sys import path
from pathlib import Path

path.append(Path(__file__).parents[2].as_posix())

from src import Camera, IMU

def main():
    camera = Camera(name='raspi-cam')
    imu = IMU(name='bno085')

    camera.connect()
    imu.connect()

    camera.start_stream()
    imu.start_stream()

    sleep(2)

    camera.stop_stream()
    imu.stop_stream()

if __name__ == '__main__':
    main()