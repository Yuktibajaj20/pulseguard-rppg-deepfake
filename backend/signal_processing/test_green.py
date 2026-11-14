
from signal_processing.rgb_extraction import extract_rgb_signals
from signal_processing.green import extract_green_signal

result = extract_rgb_signals("test_video.mp4")

for name, rgb_values in result["regions"].items():

    try:
        output = extract_green_signal(
            rgb_values,
            result["timestamps"]
        )

        print("\nRegion:", name)
        print("Heart Rate:", output["heart_rate_bpm"], "BPM")
        print("Peak Frequency:", output["peak_frequency"], "Hz")
        print("SNR:", output["snr_db"], "dB")

    except ValueError as error:
        print(name, ":", error)
