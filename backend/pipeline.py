
from signal_processing.rgb_extraction import extract_rgb_signals
from signal_processing.green import extract_green_signal

from features.spectral import calculate_spectral_features
from features.regional import calculate_regional_features
from features.quality import assess_signal_quality


def analyze_video(video_path):

    # 1. Extract RGB signals from facial regions
    rgb_data = extract_rgb_signals(video_path)

    region_outputs = {}
    spectral_features = {}

    # 2. Process each facial region
    for name, rgb_values in rgb_data["regions"].items():

        try:
            output = extract_green_signal(
                rgb_values,
                rgb_data["timestamps"]
            )

            region_outputs[name] = output

            spectral_features[name] = calculate_spectral_features(
                output
            )

        except (ValueError, FloatingPointError) as error:
            print(f"{name} processing failed: {error}")

    # 3. Ensure at least one region produced a usable signal
    if not region_outputs:
        raise ValueError(
            "No usable rPPG signals could be extracted from the video. "
            "Try a clearer video with a visible face and sufficient duration."
        )

    # 4. Calculate regional features
    regional_features = calculate_regional_features(
        region_outputs
    )

    # 5. Assess signal quality
    quality = assess_signal_quality(
        region_outputs,
        regional_features
    )

    # 6. Determine preliminary assessment
    if quality["status"] != "ACCEPTABLE":
        assessment = "INCONCLUSIVE"
    else:
        # Signal quality alone cannot establish authenticity.
        assessment = "REVIEW_REQUIRED"

    # 7. Prepare results
    heart_rates = regional_features["heart_rates"]

    return {
        "status": "completed",
        "assessment": assessment,

        "video": {
            "duration_seconds": float(rgb_data["duration"]),
            "fps": float(rgb_data["fps"]),
            "sampled_frames": len(rgb_data["timestamps"])
        },

        "heart_rates": heart_rates,
        "spectral_features": spectral_features,
        "regional_features": regional_features,
        "signal_quality": quality,

        "disclaimer": (
            "Experimental rPPG signal analysis. "
            "This result does not independently establish "
            "whether a video is authentic or manipulated."
        )
    }

