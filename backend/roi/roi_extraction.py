import cv2
import numpy as np


# Landmark groups defining approximate skin regions.
# Indices refer to MediaPipe Face Mesh's 478-point output.

ROI_LANDMARKS = {

    "forehead": [
        10, 109, 67, 103, 54, 21, 162, 127,
        234, 454, 356, 389, 251, 284, 332,
        297, 338
    ],

    "left_cheek": [
        50, 101, 118, 117, 123, 147,
        213, 192, 214, 212, 216, 206,
        203, 129, 98
    ],

    "right_cheek": [
        280, 330, 347, 346, 352, 376,
        433, 416, 434, 432, 436, 426,
        423, 358, 327
    ]
}


def extract_rois(frame, landmarks):

    if landmarks is None:
        return None

    height, width = frame.shape[:2]

    if len(landmarks) < 478:
        return None

    regions = {}

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

        mask = np.zeros(
            (height, width),
            dtype=np.uint8
        )

        cv2.fillPoly(
            mask,
            [hull],
            255
        )

        # Keep only pixels inside the polygon.
        pixels = frame[mask > 0]

        # Reject extremely small regions.
        if len(pixels) < 30:
            regions[region_name] = None
        else:
            regions[region_name] = pixels

    return regions