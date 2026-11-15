import cv2
import numpy as np

from video.frame_reader import iter_video
from video.face_detection import FaceDetector
from roi.roi_extraction import extract_rois


def extract_rgb_signals(video_path):

    # Frames are streamed one by one, so memory stays small.
    meta, frame_stream = iter_video(video_path, target_fps=10, max_width=480, max_seconds=20)
    timestamps = []

    detector = FaceDetector()

    regions = {
        "forehead": [],
        "left_cheek": [],
        "right_cheek": []
    }

    try:
        for timestamp, frame in frame_stream:

            timestamps.append(timestamp)

            landmarks = detector.detect(frame, int(timestamp * 1000))

            if landmarks is None:
                for name in regions:
                    regions[name].append([np.nan, np.nan, np.nan])
                continue

            rois = extract_rois(frame, landmarks)

            if rois is None:
                for name in regions:
                    regions[name].append([np.nan, np.nan, np.nan])
                continue

            for name, roi in rois.items():

                # OpenCV stores images in BGR order.
                rgb = cv2.cvtColor(
                    roi,
                    cv2.COLOR_BGR2RGB
                )

                mean_rgb = np.mean(
                    rgb.reshape(-1, 3),
                    axis=0
                )

                regions[name].append(mean_rgb)

    finally:
        detector.close()

    return {
        "timestamps": np.asarray(timestamps, dtype=float),
        "fps": meta["fps"],
        "duration": meta["duration"],
        "regions": {
            name: np.asarray(values, dtype=float)
            for name, values in regions.items()
        }
    }