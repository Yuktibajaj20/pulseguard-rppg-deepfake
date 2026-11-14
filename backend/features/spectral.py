
import numpy as np
from scipy.stats import entropy


def calculate_spectral_features(output):

    frequencies = np.asarray(output["frequencies"])
    power = np.asarray(output["power_spectrum"])

    valid = (
        (frequencies >= 0.7) &
        (frequencies <= 4.0)
    )

    band_power = power[valid]
    band_freq = frequencies[valid]

    if len(band_power) == 0 or np.sum(band_power) <= 0:
        raise ValueError("Invalid power spectrum")

    # Normalize spectral power
    probabilities = band_power / np.sum(band_power)

    # Spectral entropy
    spectral_entropy = entropy(probabilities)

    # Normalize entropy to 0-1
    normalized_entropy = (
        spectral_entropy / np.log(len(probabilities))
        if len(probabilities) > 1 else 0.0
    )

    peak_index = np.argmax(band_power)

    return {
        "peak_frequency_hz": float(band_freq[peak_index]),
        "spectral_entropy": float(normalized_entropy),
        "peak_power": float(band_power[peak_index])
    }
