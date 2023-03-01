import queue
import threading
import logging
from pathlib import Path
from datetime import datetime

from mcap_protobuf.writer import Writer
from mcap.exceptions import McapError

from google.protobuf.timestamp_pb2 import Timestamp

from .msg_parser import Parse

from sys import path
path.append(Path(__file__).parents[1].as_posix())

from sensors import Sensor

class McapRecorder(threading.Thread):
    def __init__(self, filepath: Path, with_date: bool = True) -> None:
        super().__init__()

        # Add prefix to date if requested
        if with_date:
            self.filepath = filepath.with_stem(f"{datetime.strftime(datetime.now(), '%y-%m-%d_%H-%M-%S')}_{filepath.stem}")
        else:
            self.filepath = filepath

        self.filepath = self.filepath.with_suffix('.mcap')
        self.subscriptions = {}
        self.stop_request = threading.Event()
        self.recording_timestamp = Timestamp()

    def run(self) -> None:
        if len(self.subscriptions) == 0:
            raise AttributeError('No data queue have been added to this recorder instance.')

        with open(self.filepath, 'wb') as file_stream, Writer(file_stream) as writer:
            try:
                while not self.stop_request.is_set():
                    # Iterate through all subscriptions
                    for sub_name, sub_data_queue in self.subscriptions.items():
                        if not sub_data_queue.empty():
                            item = sub_data_queue.get()
                            if item is None:
                                continue

                            timestamp, data = item
                            if 'imu' in sub_name:
                                message = Parse.imu_msg(data)

                            elif 'camera' in sub_name:
                                message = Parse.compressed_image_msg(timestamp, data)

                            elif 'log' in sub_name:
                                message = Parse.log_msg(data)

                            self.recording_timestamp.GetCurrentTime()
                            writer.write_message(
                                topic=sub_name,
                                message=message,
                                log_time=self.recording_timestamp.ToNanoseconds(),
                                publish_time=timestamp.ToNanoseconds()
                            )

            except Exception as exc:
                raise McapError(f'Unable to write data to {self.filepath.as_posix()}.') from exc

            finally:
                writer.finish()

    def add_subscription(self, name: str, subscription_type: str, data_queue: queue.Queue) -> None:
        self.subscriptions[f'/{subscription_type}/{name}'] = data_queue
        logging.debug(f'/{subscription_type}/{name} added to subscriptions')

    def add_sensor(self, sensor: Sensor):
        self.add_subscription(name=sensor.name, subscription_type=sensor.sensor_type, data_queue=sensor.data_queue)

    def join(self, timeout: float = None):
        self.stop_request.set()
        super().join(timeout)
