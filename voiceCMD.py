import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

rate = 16000
duration = 5
model = WhisperModel("base", device="cpu", compute_type="int8")

def listen():
    print("now listening... ")

    audio = sd.rec(
        int(duration*rate),
        samplerate=rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()
    write("command.wav", rate, audio)

def transcription():
    segments, info = model.transcribe("command.wav")
    text=""

    for segment in segments:
        text += segment.text
    return text.strip()

def getCommand():
    listen()
    command = transcription()

    print("You: ", command)
    return command