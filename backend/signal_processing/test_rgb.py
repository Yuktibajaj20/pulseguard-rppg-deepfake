
import numpy as np

from signal_processing.rgb_extraction import extract_rgb_signals

result = extract_rgb_signals("test_video.mp4")

print("Duration:", result["duration"])
print("FPS:", result["fps"])

for name, values in result["regions"].items():

    valid = np.isfinite(values).all(axis=1)

    print("\nRegion:", name)
    print("RGB array shape:", values.shape)
    print("Valid frames:", valid.sum())

    if valid.any():
        print("Mean RGB:", np.nanmean(values, axis=0))

