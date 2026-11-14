import numpy as np


def assess_signal_quality(region_outputs, regional_features):
    """
    Provisional quality gate.

    Thresholds are engineering starting points, not validated
    deepfake-detection thresholds.
    """

    reasons = []

    valid_regions = {}

    for region, output in region_outputs.items():
        if output is None:
            continue

        hr = output.get("heart_rate_bpm")
        snr = output.get("snr_db")

        if (
            hr is not None
            and snr is not None
            and np.isfinite(hr)
            and np.isfinite(snr)
        ):
            valid_regions[region] = output

    if len(valid_regions) < 2:
        reasons.append("Fewer than two valid facial regions")

    snr_values = [
        output["snr_db"]
        for output in valid_regions.values()
    ]

    mean_snr = (
        float(np.mean(snr_values))
        if snr_values else None
    )

    if mean_snr is None:
        reasons.append("No valid SNR measurements")
    elif mean_snr < -5:
        reasons.append("Low spectral pulse SNR")

    heart_rates = [
        output["heart_rate_bpm"]
        for output in valid_regions.values()
    ]

    hr_spread = (
        float(max(heart_rates) - min(heart_rates))
        if len(heart_rates) >= 2 else None
    )

    if hr_spread is not None and hr_spread > 15:
        reasons.append("Large heart-rate disagreement between regions")

    status = "ACCEPTABLE" if not reasons else "LOW"

    return {
        "status": status,
        "mean_snr_db": mean_snr,
        "heart_rate_spread_bpm": hr_spread,
        "valid_region_count": len(valid_regions),
        "reasons": reasons
    }
