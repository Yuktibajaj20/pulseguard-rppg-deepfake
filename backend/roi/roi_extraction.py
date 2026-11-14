
import numpy as np


def extract_rois(frame, landmarks):

    height, width = frame.shape[:2]

    points = np.asarray(landmarks)

    if len(points) == 0:
        return None

    x_min = max(0, int(points[:, 0].min()))
    x_max = min(width, int(points[:, 0].max()))

    y_min = max(0, int(points[:, 1].min()))
    y_max = min(height, int(points[:, 1].max()))

    face_width = x_max - x_min
    face_height = y_max - y_min

    if face_width <= 0 or face_height <= 0:
        return None

    def crop(y1, y2, x1, x2):

        top = max(0, min(height, int(y_min + y1 * face_height)))
        bottom = max(0, min(height, int(y_min + y2 * face_height)))

        left = max(0, min(width, int(x_min + x1 * face_width)))
        right = max(0, min(width, int(x_min + x2 * face_width)))

        if bottom <= top or right <= left:
            return None

        region = frame[top:bottom, left:right]

        if region.size == 0:
            return None

        return region

    rois = {
        "forehead": crop(0.08, 0.28, 0.30, 0.70),
        "left_cheek": crop(0.48, 0.72, 0.12, 0.42),
        "right_cheek": crop(0.48, 0.72, 0.58, 0.88)
    }

    if any(region is None for region in rois.values()):
        return None

    return rois
