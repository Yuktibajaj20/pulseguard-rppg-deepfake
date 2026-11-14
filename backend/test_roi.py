
import cv2

from video.frame_reader import read_video
from backend.signal_processing.face_detection import FaceDetector
from roi.roi_extraction import extract_rois

result = read_video("test_video.mp4")

detector = FaceDetector()

try:
    frame = result["frames"][0].copy()
    landmarks = detector.detect(frame)

    if landmarks:
        rois = extract_rois(frame, landmarks)

        if rois:
            for name, region in rois.items():
                print(name, region.shape)
                cv2.imshow(name, region)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("ROI extraction failed")
    else:
        print("No face detected")

finally:
    detector.close()
