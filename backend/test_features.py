
from signal_processing.rgb_extraction import extract_rgb_signals
from signal_processing.green import extract_green_signal

from features.spectral import calculate_spectral_features
from features.regional import calculate_regional_features
from features.quality import assess_signal_quality


rgb_data = extract_rgb_signals("test_video.mp4")

region_outputs = {}
spectral_features = {}

for name, values in rgb_data["regions"].items():

    try:
        output = extract_green_signal(
            values,
            rgb_data["timestamps"]
        )

        region_outputs[name] = output

        spectral_features[name] = (
            calculate_spectral_features(output)
        )

    except ValueError as error:
        print(name, "failed:", error)

regional = calculate_regional_features(region_outputs)

quality = assess_signal_quality(
    region_outputs,
    regional
)

print("\nREGIONAL FEATURES")
print(regional)

print("\nSPECTRAL FEATURES")
print(spectral_features)

print("\nQUALITY ASSESSMENT")
print(quality)
