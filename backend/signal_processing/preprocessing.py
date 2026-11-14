
import numpy as np
from scipy import signal


def preprocess_signal(
    values,
    timestamps,
    target_fs=15,
    lowcut=0.7,
    highcut=4.0
):

    values = np.asarray(values, dtype=float)
    timestamps = np.asarray(timestamps, dtype=float)

    valid = (
        np.isfinite(values) &
        np.isfinite(timestamps)
    )

    values = values[valid]
    timestamps = timestamps[valid]

    if len(values) < 2:
        raise ValueError("Not enough valid signal samples")

    # Remove duplicate timestamps
    timestamps, unique_idx = np.unique(
        timestamps, return_index=True
    )
    values = values[unique_idx]

    duration = timestamps[-1] - timestamps[0]

    if duration < 15:
        raise ValueError(
            "At least 15 seconds of valid signal required"
        )

    # Create uniform sampling timestamps
    uniform_time = np.arange(
        timestamps[0],
        timestamps[-1],
        1 / target_fs
    )

    if len(uniform_time) < 2:
        raise ValueError("Insufficient resampled data")

    # Interpolate missing samples
    resampled = np.interp(
        uniform_time,
        timestamps,
        values
    )

    # Remove linear trend
    detrended = signal.detrend(resampled)

    # Normalize
    std = np.std(detrended)

    if std < 1e-8:
        raise ValueError("Signal has insufficient variation")

    normalized = (
        detrended - np.mean(detrended)
    ) / std

    # Butterworth bandpass filter
    sos = signal.butter(
        3,
        [lowcut, highcut],
        btype="bandpass",
        fs=target_fs,
        output="sos"
    )

    filtered = signal.sosfiltfilt(
        sos,
        normalized
    )

    return {
        "signal": filtered,
        "timestamps": uniform_time,
        "fps": target_fs
    }
