
import cv2


def read_video(video_path, target_fps=15):

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

