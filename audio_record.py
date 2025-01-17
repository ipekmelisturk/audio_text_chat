import sounddevice as sd
import numpy as np

def record_audio(duration=5, sample_rate=16000):
    """
    Record audio using sounddevice for the specified duration and sample rate.
    """
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait for the recording to complete
    print("Audio recording completed.")
    return np.squeeze(audio_data)
