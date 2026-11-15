
import numpy as np


def assess_signal_quality(region_outputs, regional_features):
    """
    Provisional signal quality assessment.

    Thresholds are engineering starting points, not validated
    deepfake-detection thresholds.
    """

    reasons = []
    valid_regions = {}

    # 1. Identify regions with valid heart-rate and SNR values
    for region, output in region_outputs.items():

        if output is None:
            continue

        heart_rate = output.get("heart_rate_bpm")
        snr = output.get("snr_db")

        if (
            heart_rate is not None
            and snr is not None
            and np.isfinite(heart_rate)
            and np.isfinite(snr)
        ):
            valid_regions[region] = output

    # 2. Check the number of valid facial regions
    if len(valid_regions) < 2:
        reasons.append("Fewer than two valid facial regions")

    # 3. Calculate mean signal-to-noise ratio
    snr_values = [
        output["snr_db"]
        for output in valid_regions.values()
    ]

    mean_snr = (
        float(np.mean(snr_values))
        if snr_values
        else None
    )

    if mean_snr is None:
        reasons.append("No valid SNR measurements")

    elif mean_snr < -5:
        reasons.append("Low spectral pulse SNR")

    # 4. Calculate heart-rate disagreement between regions
    heart_rates = [
        output["heart_rate_bpm"]
        for output in valid_regions.values()
    ]

    heart_rate_spread = (
        float(max(heart_rates) - min(heart_rates))
        if len(heart_rates) >= 2
        else None
    )

    if (
        heart_rate_spread is not None
        and heart_rate_spread > 15
    ):
        reasons.append(
            "Large heart-rate disagreement between regions"
        )

    # 5. Determine signal quality status
    status = "ACCEPTABLE" if not reasons else "LOW"

    # 6. Return quality assessment
    return {
    "status": "ACCEPTABLE" if not reasons else "LOW",
    "reasons": reasons,
    
}
    # 6. Return quality assessment
    return {
        "status": status,
        "reasons": reasons,
        "mean_snr_db": mean_snr,
        "valid_regions": len(valid_regions),
        "heart_rate_spread_bpm": heart_rate_spread
    }
