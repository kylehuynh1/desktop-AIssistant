import sounddevice as sd
from piper import PiperVoice
import io
import wave
import numpy as np

voice = PiperVoice.load(
    "voices/en_GB-cori-high.onnx"
)

def speak(text):
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wavFile:
        voice.synthesize_wav(text, wavFile)

    buffer.seek(0)

    with wave.open(buffer, "rb") as wavFile:
        rate = wavFile.getframerate()
        audio = wavFile.readframes(wavFile.getnframes())

    audio = np.frombuffer(audio, dtype=np.int16)

    sd.play(audio, rate)
    sd.wait()


speak("Friday is online and ready.")