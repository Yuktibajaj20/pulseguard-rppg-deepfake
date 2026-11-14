
import cv2

from video.frame_reader import read_video
from backend.signal_processing.face_detection import FaceDetector

result = read_video("test_video.mp4")

detector = FaceDetector()

frame = result["frames"][0].copy()

landmarks = detector.detect(frame)

if landmarks:
    for x, y in landmarks:
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    print("Face detected!")
    print("Number of landmarks:", len(landmarks))

    cv2.imshow("Face Detection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("No face detected")

detector.close()


import cv2

from video.frame_reader import read_video
from backend.signal_processing.face_detection import FaceDetector

result = read_video("test_video.mp4")

detector = FaceDetector()

frame = result["frames"][0].copy()

try:
    landmarks = detector.detect(frame)

    if landmarks:

        for x, y in landmarks:
            cv2.circle(
                frame,
                (x, y),
                1,
                (0, 255, 0),
                -1
            )

        print("FACE DETECTED!")
        print("Landmarks:", len(landmarks))

        cv2.imshow("Face Landmarks", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("No face detected")

finally:
    detector.close()
