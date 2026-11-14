import numpy as np

from signal_processing.green import pulse_snr_db


def test_known_pulse():
    fps = 15
    duration = 30

    t = np.arange(0, duration, 1 / fps)

    true_bpm = 72
    true_frequency = true_bpm / 60

    clean_signal = np.sin(
        2 * np.pi * true_frequency * t
    )

    rng = np.random.default_rng(42)

    noisy_signal = clean_signal + 0.25 * rng.normal(
        size=len(t)
    )

    from scipy.signal import welch

    frequencies, power = welch(
        noisy_signal,
        fs=fps,
        nperseg=450
    )

    band = (
        (frequencies >= 0.75)
        & (frequencies <= 3.0)
    )

    peak_frequency = frequencies[band][
        np.argmax(power[band])
    ]

    bpm = peak_frequency * 60

    snr = pulse_snr_db(
        frequencies,
        power,
        peak_frequency
    )

    print("Expected BPM:", true_bpm)
    print("Estimated BPM:", bpm)
    print("Absolute error:", abs(bpm - true_bpm))
    print("SNR:", snr, "dB")

    assert abs(bpm - true_bpm) <= 3


if __name__ == "__main__":
    test_known_pulse()