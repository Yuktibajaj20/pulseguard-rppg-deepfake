
import numpy as np


def calculate_regional_features(region_outputs):

    names = list(region_outputs.keys())

    heart_rates = {}
    correlations = []

    for name, output in region_outputs.items():
        heart_rates[name] = output["heart_rate_bpm"]

    # Compare filtered signals
    for i in range(len(names)):
        for j in range(i + 1, len(names)):

            signal_a = np.asarray(
                region_outputs[names[i]]["filtered_signal"]
            )

            signal_b = np.asarray(
                region_outputs[names[j]]["filtered_signal"]
            )

            if len(signal_a) != len(signal_b):
                continue

            if len(signal_a) < 3:
                continue

            if np.std(signal_a) < 1e-8 or np.std(signal_b) < 1e-8:
                continue

            corr = np.corrcoef(signal_a, signal_b)[0, 1]

            if np.isfinite(corr):
                correlations.append(float(corr))

    # Heart-rate agreement
    rates = np.array(list(heart_rates.values()))

    hr_difference = (
        float(np.max(rates) - np.min(rates))
        if len(rates) >= 2 else None
    )

    return {
        "heart_rates": heart_rates,
        "mean_correlation": (
            float(np.mean(correlations))
            if correlations else None
        ),
        "hr_difference_bpm": hr_difference,
        "valid_regions": len(heart_rates)
    }
