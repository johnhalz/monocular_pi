'''Recorder class module'''
import logging
from pathlib import Path
from datetime import datetime

from mcap_protobuf.writer import Writer
from mcap.exceptions import McapError

from .io_element import IOElement

class Recorder(IOElement):
    '''
    Recorder class - record incoming messages to mcap file
    '''
    def __init__(self, filepath: Path, name: str = 'MCAP Recorder',
                 topic: str = None, with_date: bool = True) -> None:
        super().__init__(name, topic)

        # Set output filepath
        if with_date:
            self.filepath = filepath.with_stem(
                f"{datetime.strftime(datetime.now(), '%y-%m-%d_%H-%M-%S')}_{filepath.stem}"
            )
        else:
            self.filepath = filepath

        self.filepath = self.filepath.with_suffix('.mcap')

    def _streaming_loop(self) -> None:
        logging.info(f'{self.name}: Starting recording to {self.filepath.as_posix()}')
        with open(self.filepath, 'wb') as file_stream, Writer(file_stream) as writer:
            try:
                while not self.stop_flag:
                    self._stream_task(writer)

            except Exception as exc:
                raise McapError(
                    f'Unable to write data to {self.filepath.as_posix()}'
                ) from exc

            finally:
                writer.finish()

    # pylint: disable=arguments-differ
    def _stream_task(self, writer: Writer) -> None:
        '''
        Get latest input message and write it to the mcap file

        Parameters
        ----------
        - `writer` (`Writer`): File stream writer instance
        '''
        self.timestamp.GetCurrentTime()
        topic, message = self.input_queue.get()
        writer.write_message(
            message = message,
            topic = topic,
            log_time = self.timestamp.ToNanoseconds(),
            publish_time = message.timestamp.ToNanoseconds()
        )
