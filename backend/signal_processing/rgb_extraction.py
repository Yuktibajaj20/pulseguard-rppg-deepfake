import numpy as np
import cv2

from video.frame_reader import read_video
from video.face_detection import FaceDetector
from roi.roi_extraction import extract_rois


def extract_rgb_signals(video_path):

    video_data = read_video(video_path)

    frames = video_data["frames"]
    timestamps = video_data["timestamps"]

    fps = video_data["fps"]
    duration = video_data["duration"]

    detector = FaceDetector()

    region_names = [
        "forehead",
        "left_cheek",
        "right_cheek"
    ]

    rgb_signals = {
        name: [] for name in region_names
    }

    face_detected_count = 0

    try:

        for frame, timestamp in zip(frames, timestamps):

            landmarks = detector.detect(
                frame,
                int(timestamp * 1000)
            )

            if landmarks is None:

                for name in region_names:
                    rgb_signals[name].append(
                        [np.nan, np.nan, np.nan]
                    )

                continue

            face_detected_count += 1

            rois = extract_rois(
                frame,
                landmarks
            )

            for name in region_names:

                pixels = rois.get(name)

                if pixels is None or len(pixels) < 30:

                    rgb_signals[name].append(
                        [np.nan, np.nan, np.nan]
                    )

                    continue

                # OpenCV frame is BGR.
                mean_bgr = np.mean(
                    pixels,
                    axis=0
                )

                mean_rgb = mean_bgr[::-1]

                rgb_signals[name].append(
                    mean_rgb.tolist()
                )

    finally:
        detector.close()

    for name in region_names:
        rgb_signals[name] = np.asarray(
            rgb_signals[name],
            dtype=float
        )

    face_detection_rate = (
        face_detected_count / len(frames)
        if frames else 0
    )

    return {
        "timestamps": np.asarray(timestamps),
        "fps": fps,
        "duration": duration,
        "regions": rgb_signals,
        "face_detection_rate": face_detection_rate
    }