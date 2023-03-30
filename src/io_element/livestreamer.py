'''Livestreaming class module'''
import logging

from foxglove_websocket.server import FoxgloveServer

from .io_element import IOElement

class LiveStreamer(IOElement):
    '''LiveStreamer class - Livestream captured data to connected foxglove studio instance.'''
    def __init__(self, name: str, ip_address: str, port: int, topic: str = None) -> None:
        super().__init__(name, topic)
        self.ip_address = ip_address
        self.port = port
        self.known_topics = {}

    async def _a_streaming_loop(self) -> None:
        logging.info(f'{self.name}: Starting livestreaming on {self.ip_address}:{self.port}.')
        async with FoxgloveServer(self.ip_address, self.port, self.name) as server:
            try:
                while not self.stop_flag:
                    self._stream_task(server)

            except Exception as exc:
                raise AttributeError(
                    f'Unable to stream data to {self.ip_address}:{self.port}.'
                ) from exc

    # pylint: disable=arguments-differ
    def _stream_task(self, server: FoxgloveServer) -> None:
        '''
        Get latest input message and stream it to listeners.

        Parameters
        ----------
        - `server` (`FoxgloveServer`): Server instance
        '''
        self.timestamp.GetCurrentTime()
        topic, message = self.input_queue.get()
        if topic not in self.known_topics:
            channel_id = server.add_channel(
                {
                    'topic': topic,
                    'encoding': 'protobuf'
                }
            )
            self.known_topics[topic] = channel_id

        server.send_message(self.known_topics[topic], self.timestamp.ToNanoseconds(), message)
