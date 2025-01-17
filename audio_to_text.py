import whisper
import scipy.io.wavfile as wavfile

# Load Whisper model
model = whisper.load_model("base")

def save_audio(file_name, audio_data, sample_rate=16000):
    """
    Save audio data to a WAV file.
    """
    wavfile.write(file_name, sample_rate, audio_data)

def transcribe_audio(file_name):
    """
    Transcribe audio using Whisper.
    """
    print("Transcribing audio...")
    result = model.transcribe(file_name)
    print("Transcription completed.")
    return result["text"]
