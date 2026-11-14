import cv2


def read_video(video_path, target_fps=15):
    """Original version: loads every sampled frame into memory.
    Kept for the test scripts. Do NOT use it on the server."""

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video")

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if original_fps <= 0 or total_frames <= 0:
        cap.release()
        raise ValueError("Invalid video metadata")

    duration = total_frames / original_fps

    frame_interval = max(1, round(original_fps / target_fps))

    frames = []
    timestamps = []

    frame_number = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_number % frame_interval == 0:

            frames.append(frame)

            timestamps.append(
                frame_number / original_fps
            )

        frame_number += 1

    cap.release()

    return {
        "frames": frames,
        "timestamps": timestamps,
        "fps": original_fps,
        "duration": duration,
        "total_frames": total_frames
    }


def iter_video(video_path, target_fps=15, max_width=640, max_seconds=30):
    """Memory-safe reader: yields one frame at a time.

    - frames are shrunk to max_width so large videos use little RAM
    - only the first max_seconds of video are analysed
    Returns (meta, generator of (timestamp, frame)).
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video")

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if original_fps <= 0 or total_frames <= 0:
        cap.release()
        raise ValueError("Invalid video metadata")

    meta = {
        "fps": original_fps,
        "duration": total_frames / original_fps,
        "total_frames": total_frames
    }

    frame_interval = max(1, round(original_fps / target_fps))
    last_frame = int(max_seconds * original_fps)

    def frames():
        try:
            frame_number = 0

            while frame_number < last_frame:

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_number % frame_interval == 0:

                    height, width = frame.shape[:2]

                    if width > max_width:
                        scale = max_width / width
                        frame = cv2.resize(
                            frame,
                            (max_width, int(height * scale)),
                            interpolation=cv2.INTER_AREA
                        )

                    yield frame_number / original_fps, frame

                frame_number += 1
        finally:
            cap.release()

    return meta, frames()