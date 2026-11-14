
import cv2
import numpy as np

from video.face_detection import FaceDetector
from roi.roi_extraction import (
    extract_rois,
    ROI_LANDMARKS
)


VIDEO_PATH = "test_videos/test_video.mp4"


def test_roi_polygons():

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open video: {VIDEO_PATH}"
        )

    detector = FaceDetector()

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)

        if not fps or fps <= 0:
            fps = 15

        # Read a frame with a detectable face.
        frame = None
        landmarks = None
        frame_number = 0

        while True:
            success, current_frame = cap.read()

            if not success:
                break

            timestamp_ms = int(
                frame_number * 1000 / fps
            )

            current_landmarks = detector.detect(
                current_frame,
                timestamp_ms
            )

            if current_landmarks is not None:
                frame = current_frame.copy()
                landmarks = current_landmarks
                break

            frame_number += 1

        if frame is None or landmarks is None:
            raise RuntimeError(
                "No face detected in the video."
            )

        if len(landmarks) < 478:
            raise RuntimeError(
                f"Expected 478 landmarks, got {len(landmarks)}"
            )

        print("Face detected!")
        print("Landmarks:", len(landmarks))

        height, width = frame.shape[:2]

        # Draw all ROI polygons.
        for region_name, indices in ROI_LANDMARKS.items():

            points = np.array(
                [landmarks[i] for i in indices],
                dtype=np.int32
            )

            points[:, 0] = np.clip(
                points[:, 0], 0, width - 1
            )

            points[:, 1] = np.clip(
                points[:, 1], 0, height - 1
            )

            hull = cv2.convexHull(points)

            if hull is None or len(hull) < 3:
                print(f"{region_name}: Invalid polygon")
                continue

            # Draw polygon outline.
            cv2.polylines(
                frame,
                [hull],
                True,
                (0, 255, 0),
                2
            )

            # Calculate a valid (x, y) text position.
            center = (
                hull.reshape(-1, 2)
                .mean(axis=0)
                .astype(int)
            )

            center = (
                int(center[0]),
                int(center[1])
            )

            cv2.putText(
                frame,
                region_name,
                center,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA
            )

        # Check actual extracted ROI pixels.
        rois = extract_rois(frame, landmarks)

        print("\nROI extraction results:")

        for name, pixels in rois.items():

            if pixels is None:
                print(f"{name}: INVALID")
            else:
                print(
                    f"{name}: {len(pixels)} pixels"
                )

        cv2.imshow(
            "PulseGuard - ROI Polygon Validation",
            frame
        )

        print("\nPress any key to close the preview.")

        cv2.waitKey(0)

    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    test_roi_polygons()
