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
    camera = Camera(name='raspi-cam',
                    topic='image',
                    simulated=Path.home() / 'Downloads/kitti/05/image_1/output.mp4')

    # Create recorder instance and add data queues
    recorder = Recorder(filepath=Path.home()/'data/test.mcap', with_date=True)
    camera.add_subscriber(recorder)
    log_handler.add_subscriber(recorder)

    # Connect to sensors
    camera.connect()

    # Start streaming data from sensors
    recorder.start_stream()
    camera.start_stream()

    sleep(10)

    # Stop stream from sensors
    camera.stop_stream()
    recorder.stop_stream()

    # Disconnect from sensors
    camera.disconnect()

if __name__ == '__main__':
    main()
