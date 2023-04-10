'''Image feature detector class module'''
from typing import Dict, Union, List

import numpy as np
import cv2

from messages.img_annotation_msg import ImageAnnotation
from messages.points_annotation_msg import PointsAnnotation
from messages.point2_msg import Point2
from messages.color_msg import Color

from .io_element import IOElement

class ImgFeatureDetector(IOElement):
    '''
    Image Feature Detector class - detect and save features found in received image
    '''
    def __init__(self, name: str = 'Feature Detector', topic: str = None) -> None:
        super().__init__(name, topic)

        # Setup freak detector
        self.detector = cv2.xfeatures2d.FREAK_create()

    def _stream_task(self) -> Union[Dict[str, ImageAnnotation], ImageAnnotation, None]:
        '''
        Get latest input message and detect features in image.
        '''
        # Read in latest message
        _, message = self.input_queue.get()

        # Extract image from message
        image = cv2.imdecode(np.frombuffer(message.data, np.uint8), cv2.IMREAD_COLOR)
        img_timestamp = message.timestamp

        keypoints = self.__detect_features(image)

        if keypoints is None:
            return None

        return ImgFeatureDetector.__package_keypoints_to_protobuf(img_timestamp, keypoints)

    def __detect_features(self, image: Union[cv2.Mat, np.ndarray]) \
        -> Union[List[cv2.KeyPoint], None]:
        '''
        Convert received image to grayscale and detect features

        Parameters
        ----------
        - `image`: Input image
        '''
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect features on grayscale image
        keypoints = self.detector.detect(gray, None)

        if len(keypoints) == 0:
            return None

        return keypoints

    @staticmethod
    def __package_keypoints_to_protobuf(img_timestamp,
                                        keypoints: List[cv2.KeyPoint]) -> ImageAnnotation:
        '''
        Package found keypoints into message to send

        Parameters
        ----------
        - `img_timestamp`: Timestamp of taken image
        - `keypoints` (`List[cv2.KeyPoint]`): List of found keypoints

        Returns
        -------
        - `ImageAnnotation`: ImageAnnotation protobuf message
        '''
        img_annotation_msg = ImageAnnotation()
        feature_point_color = Color(r=1., g=0., b=0., a=0.)
        points = []
        for keypoint in keypoints:
            points.append(Point2(x=keypoint.pt[0], y=keypoint.pt[1]))

        points_annotation = PointsAnnotation()
        points_annotation.timestamp = img_timestamp
        points_annotation.type = 'POINTS'
        points_annotation.points = points
        points_annotation.outline_color = feature_point_color
        points_annotation.outline_colors = [feature_point_color] * len(points)
        points_annotation.fill_colot = feature_point_color
        points_annotation.thickness = 2.0

        img_annotation_msg.points = [points_annotation]
        img_annotation_msg.circles = []

        return img_annotation_msg
