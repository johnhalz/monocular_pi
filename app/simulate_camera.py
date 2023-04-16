'''Stream and record app'''
from time import sleep
from pathlib import Path
import logging
from sys import path

path.append(Path(__file__).parents[1].as_posix())

from src.sensors import Camera
from src.io_element import Recorder, LogHandler

# pylint: disable=missing-function-docstring
def main():
    # Create logger
    log_handler = LogHandler()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(log_handler)

    # Create sensor instances
    camera_0 = Camera(name='cam_0',
                    topic='image',
                    simulated=Path.home() / 'Downloads/kitti/05/cam_0.mp4')
    camera_1 = Camera(name='cam_1',
                    topic='image',
                    simulated=Path.home() / 'Downloads/kitti/05/cam_1.mp4')

    # Create recorder instance and add data queues
    recorder = Recorder(filepath=Path.home()/'data/test.mcap', with_date=True)
    camera_0.add_subscriber(recorder)
    camera_1.add_subscriber(recorder)
    log_handler.add_subscriber(recorder)

    # Connect to sensors
    camera_0.connect()
    camera_1.connect()

    # Start streaming data from sensors
    recorder.start_stream()
    camera_0.start_stream()
    camera_1.start_stream()

    sleep(5)

    # Stop stream from sensors
    camera_0.stop_stream()
    camera_1.stop_stream()
    recorder.stop_stream()

    # Disconnect from sensors
    camera_0.disconnect()
    camera_1.disconnect()

if __name__ == '__main__':
    main()
