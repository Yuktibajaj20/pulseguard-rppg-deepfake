import numpy as np

from scipy.signal import (
    butter,
    detrend,
    sosfiltfilt,
    welch,
    find_peaks
)


def resample_rgb(rgb_values, timestamps, target_fps=15):
    """
    Resample RGB values onto a uniform time grid.

    Rejects long missing-data gaps rather than interpolating across them.
    rgb_values shape: (N, 3)
    """

    rgb = np.asarray(rgb_values, dtype=float)
    timestamps = np.asarray(timestamps, dtype=float)

    if rgb.ndim != 2 or rgb.shape[1] != 3:
        raise ValueError("RGB input must have shape (N, 3)")

    if len(rgb) != len(timestamps):
        raise ValueError("RGB values and timestamps must have equal lengths")

    valid = (
        np.isfinite(timestamps)
        & np.all(np.isfinite(rgb), axis=1)
    )

    rgb = rgb[valid]
    timestamps = timestamps[valid]

    if len(timestamps) < 30:
        raise ValueError("Not enough valid RGB samples")

    order = np.argsort(timestamps)
    rgb = rgb[order]
    timestamps = timestamps[order]

    timestamps, unique_indices = np.unique(
        timestamps,
        return_index=True
    )
    rgb = rgb[unique_indices]

    if len(timestamps) < 30:
        raise ValueError("Not enough unique timestamps")

    gaps = np.diff(timestamps)

    if np.any(gaps > 0.5):
        raise ValueError(
            "Long missing-data gap detected. "
            "Process valid continuous segments separately."
        )

    duration = timestamps[-1] - timestamps[0]

    if duration < 15:
        raise ValueError("At least 15 seconds of valid signal required")

    uniform_timestamps = np.arange(
        timestamps[0],
        timestamps[-1],
        1.0 / target_fps
    )

    uniform_rgb = np.column_stack([
        np.interp(
            uniform_timestamps,
            timestamps,
            rgb[:, channel]
        )
        for channel in range(3)
    ])

    return uniform_rgb, uniform_timestamps


def bandpass_filter(signal, fps, low=0.75, high=3.0):
    """Filter the signal to the expected cardiac frequency range."""

    signal = np.asarray(signal, dtype=float)

    if len(signal) < fps * 10:
        raise ValueError("Signal is too short for filtering")

    nyquist = fps / 2

    if high >= nyquist:
        raise ValueError("Sampling frequency is too low")

    sos = butter(
        3,
        [low / nyquist, high / nyquist],
        btype="bandpass",
        output="sos"
    )

    filtered = sosfiltfilt(sos, detrend(signal))

    return filtered


def pulse_snr_db(
    freqs,
    power,
    f_peak,
    band=(0.75, 3.0),
    half_width=0.10
):
    """
    Pulse SNR using the fundamental and second harmonic.

    This is a spectral peak-to-background metric, not a validated
    physiological signal-quality score.
    """

    freqs = np.asarray(freqs)
    power = np.asarray(power)

    in_band = (
        (freqs >= band[0])
        & (freqs <= band[1])
    )

    fundamental = np.abs(freqs - f_peak) <= half_width
    harmonic = np.abs(freqs - 2 * f_peak) <= half_width

    signal_bins = in_band & (fundamental | harmonic)
    noise_bins = in_band & ~signal_bins

    signal_power = np.sum(power[signal_bins])
    noise_power = np.sum(power[noise_bins])

    if signal_power <= 0:
        return float("-inf")

    return float(
        10 * np.log10(
            signal_power / (noise_power + 1e-12)
        )
    )


def extract_green_signal(rgb_values, timestamps, fps=15):
    """
    Extract and analyze the green-channel pulse signal.

    Returns heart rate, filtered signal, spectrum and SNR.
    """

    rgb, uniform_timestamps = resample_rgb(
        rgb_values,
        timestamps,
        target_fps=fps
    )

    green = rgb[:, 1]

    filtered = bandpass_filter(
        green,
        fps
    )

    frequencies, power = welch(
        filtered,
        fs=fps,
        nperseg=min(len(filtered), fps * 10),
        noverlap=None
    )

    valid_band = (
        (frequencies >= 0.75)
        & (frequencies <= 3.0)
    )

    if not np.any(valid_band):
        raise ValueError("No cardiac frequency bins available")

    band_power = power.copy()
    band_power[~valid_band] = 0

    peak_index = np.argmax(band_power)
    peak_frequency = float(frequencies[peak_index])

    # Reject peaks too close to the search-band boundaries.
    if peak_frequency <= 0.76 or peak_frequency >= 2.99:
        raise ValueError("Pulse peak is too close to the frequency boundary")

    heart_rate = peak_frequency * 60

    snr_db = pulse_snr_db(
        frequencies,
        power,
        peak_frequency
    )

    return {
        "filtered_signal": filtered,
        "timestamps": uniform_timestamps,
        "frequencies": frequencies,
        "power_spectrum": power,
        "peak_frequency": peak_frequency,
        "heart_rate_bpm": float(heart_rate),
        "snr_db": snr_db
    }