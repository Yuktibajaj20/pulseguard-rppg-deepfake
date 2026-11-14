
import cv2
import mediapipe as mp
from pathlib import Path


class FaceDetector:

    def __init__(self):

        # Locate the downloaded MediaPipe model
        model_path = (
            Path(__file__).resolve().parents[1]
            / "models"
            / "face_landmarker.task"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {model_path}"
            )
        

        # Configure MediaPipe Face Landmarker
        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=str(model_path)
            ),
            running_mode=(
                mp.tasks.vision.RunningMode.IMAGE
            ),
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = (
            mp.tasks.vision.FaceLandmarker
            .create_from_options(options)
        )

    def detect(self, frame):

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert image to MediaPipe format
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect facial landmarks
        result = self.detector.detect(mp_image)

        if not result.face_landmarks:
            return None

        height, width = frame.shape[:2]

        landmarks = []

        for point in result.face_landmarks[0]:

            x = int(point.x * width)
            y = int(point.y * height)

            landmarks.append((x, y))

        return landmarks

    def close(self):
        self.detector.close()
