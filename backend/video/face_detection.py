import cv2
import mediapipe as mp

from pathlib import Path


class FaceDetector:

    def __init__(self):

        model_path = (
            Path(__file__).resolve().parents[1]
            / "models"
            / "face_landmarker.task"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Face model not found: {model_path}"
            )

        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=str(model_path)
            ),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = (
            mp.tasks.vision.FaceLandmarker.create_from_options(
                options
            )
        )

        self.last_timestamp_ms = -1

    def detect(self, frame, timestamp_ms):

        if timestamp_ms <= self.last_timestamp_ms:
            timestamp_ms = self.last_timestamp_ms + 1

        self.last_timestamp_ms = timestamp_ms

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        if not result.face_landmarks:
            return None

        height, width = frame.shape[:2]

        landmarks = result.face_landmarks[0]

        points = [
            (
                int(point.x * width),
                int(point.y * height)
            )
            for point in landmarks
        ]

        return points

    def close(self):
        self.detector.close()