
import cv2
import numpy as np

from video.frame_reader import read_video
from video.face_detection import FaceDetector
from roi.roi_extraction import extract_rois


def extract_rgb_signals(video_path):

    video = read_video(video_path)

    frames = video["frames"]
    timestamps = np.asarray(video["timestamps"], dtype=float)

    detector = FaceDetector()

    regions = {
        "forehead": [],
        "left_cheek": [],
        "right_cheek": []
    }

    try:
        for frame in frames:

            landmarks = detector.detect(frame)

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
        "timestamps": timestamps,
        "fps": video["fps"],
        "duration": video["duration"],
        "regions": {
            name: np.asarray(values, dtype=float)
            for name, values in regions.items()
        }
    }
