
import numpy as np
from scipy.signal import welch, find_peaks

from signal_processing.preprocessing import preprocess_signal


def extract_green_signal(rgb_values, timestamps):

    rgb_values = np.asarray(rgb_values, dtype=float)

    if rgb_values.ndim != 2 or rgb_values.shape[1] != 3:
        raise ValueError("Expected RGB array with shape (N, 3)")

    # Extract green channel
    green = rgb_values[:, 1]

    processed = preprocess_signal(
        green,
        timestamps
    )

    signal_data = processed["signal"]
    fs = processed["fps"]

    # Welch power spectral density
    frequencies, power = welch(
        signal_data,
        fs=fs,
        nperseg=min(256, len(signal_data))
    )

    # Physiological frequency range
    valid = (
        (frequencies >= 0.7) &
        (frequencies <= 4.0)
    )

    band_freq = frequencies[valid]
    band_power = power[valid]

    if len(band_power) == 0:
        raise ValueError("No valid frequency components")

    peak_index = np.argmax(band_power)

    peak_frequency = band_freq[peak_index]

    heart_rate = peak_frequency * 60

    # Approximate peak-to-background power ratio
    noise_power = np.sum(band_power) - band_power[peak_index]

    snr = 10 * np.log10(
        (band_power[peak_index] + 1e-12) /
        (noise_power + 1e-12)
    )

    return {
        "filtered_signal": signal_data,
        "frequencies": frequencies,
        "power_spectrum": power,
        "heart_rate_bpm": float(heart_rate),
        "peak_frequency": float(peak_frequency),
        "snr_db": float(snr)
    }
