import cv2
import logging
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

from sys import path
from pathlib import Path
path.append(Path(__file__).parent.as_posix())

from foxglove import IMUMessage, CompressedImage, Log

class Parse:
    @staticmethod
    def imu_msg(data) -> IMUMessage:
        return IMUMessage(
            accel_x = data[0],
            accel_y = data[1],
            accel_z = data[2],
            orient_w = data[3],
            orient_i = data[4],
            orient_j = data[5],
            orient_k = data[6]
        )

    @staticmethod
    def compressed_image_msg(timestamp, data, encoding: str = 'jpeg') -> CompressedImage:
        success, enc_img = cv2.imencode(f'.{encoding}', data)
        if not success:
            return None

        byte_img = enc_img.tobytes()
        message = CompressedImage()

        message.timestamp.CopyFrom(timestamp)
        message.frame_id = ''
        message.format = encoding
        message.data = byte_img

        return message

    @staticmethod
    def log_msg(log_message_data: logging.LogRecord) -> Log:
        message = Log()
        ts = Timestamp()
        ts.FromDatetime(datetime.fromtimestamp(log_message_data.created))
        message.timestamp.CopyFrom(ts)
        message.file = log_message_data.filename
        message.line = log_message_data.lineno
        message.message = log_message_data.getMessage()
        message.level = log_message_data.levelname
        message.name = log_message_data.processName

        return message
