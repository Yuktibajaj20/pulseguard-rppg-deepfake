
import numpy as np


def assess_signal_quality(region_outputs, regional_features):

    reasons = []

    valid_regions = len(region_outputs)

    if valid_regions < 2:
        reasons.append("Insufficient valid facial regions")

    snr_values = [
        output["snr_db"]
        for output in region_outputs.values()
        if np.isfinite(output["snr_db"])
    ]

    if len(snr_values) < 2:
        reasons.append("Insufficient valid SNR measurements")

    # Initial engineering threshold, not a validated clinical cutoff
    if snr_values and np.mean(snr_values) < 0:
        reasons.append("Low average signal-to-noise ratio")

    difference = regional_features["hr_difference_bpm"]

    if difference is None or difference > 15:
        reasons.append("Heart-rate estimates disagree across regions")

    correlation = regional_features["mean_correlation"]

    if correlation is None:
        reasons.append("Regional correlation unavailable")

    quality = "ACCEPTABLE" if not reasons else "LOW"

    return {
        "quality": quality,
        "reasons": reasons,
        "mean_snr_db": (
            float(np.mean(snr_values))
            if snr_values else None
        )
    }
