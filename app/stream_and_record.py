from time import sleep
from sys import path
from pathlib import Path
import logging

path.append(Path(__file__).parents[1].as_posix())

from src.sensors import IMU, Camera
from src.recorder import McapRecorder
from src.log_handler import LogHandler

def main():
    # Create logger
    log_handler = LogHandler()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(log_handler)

    # Create sensor instances
    camera = Camera(name='raspi-cam')
    imu = IMU(name='bno085')

    # Create recorder instance and add data queues
    recorder = McapRecorder(filepath=Path.home()/'data/test.mcap', with_date=True)
    recorder.add_sensor(camera)
    recorder.add_sensor(imu)
    recorder.add_subscription(name='log', subscription_type='logger', data_queue=log_handler.data_queue)

    # Connect to sensors
    camera.connect()
    imu.connect()

    # Start streaming data from sensors
    recorder.start()
    camera.start_stream()
    imu.start_stream()

    sleep(2)

    # Stop stream from sensors
    camera.stop_stream()
    imu.stop_stream()
    recorder.join()

    # Disconnect from sensors
    camera.disconnect()
    imu.disconnect()

if __name__ == '__main__':
    main()
