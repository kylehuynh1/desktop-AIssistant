import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from openwakeword.model import Model
import numpy as np

rate = 16000

# Command can currently be up to 5 seconds
commandDuration = 5


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

wakeModel = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)
def wakeListen():
    print("Friday: idling...")

    with sd.InputStream(
        samplerate=rate,
        channels=1,
        dtype="int16",
        blocksize=1280
    ) as stream:

        while True:
            audio, overflowed = stream.read(1280)

            if overflowed:
                print("audio overflow")

            audio = audio.flatten()

            prediction = wakeModel.predict(audio)
            score = prediction["hey_jarvis"]

            if score > 0.05:
                print("wake score:", score)

            if score > 0.5:
                print("Friday: listening.")
                wakeModel.reset()
                return


def listen():
    print("now listening...")

    blockDuration = 0.1
    blockSize = int(rate * blockDuration)

    silenceThreshold = 500
    silenceLimit = 1.0
    maxDuration = 15

    audioChunks = []

    speaking = False
    silenceTime = 0
    totalTime = 0

    with sd.InputStream(
        samplerate=rate,
        channels=1,
        dtype="int16",
        blocksize=blockSize
    ) as stream:

        while totalTime < maxDuration:
            audio, overflowed = stream.read(blockSize)

            audioChunks.append(audio.copy())

            # Average volume of this chunk
            volume = np.abs(audio).mean()

            totalTime += blockDuration

            if volume > silenceThreshold:
                speaking = True
                silenceTime = 0

            elif speaking:
                silenceTime += blockDuration

                if silenceTime >= silenceLimit:
                    break

    # Nothing was actually spoken
    if not speaking:
        return False

    audio = np.concatenate(audioChunks)

    write("command.wav", rate, audio)

    return True

def transcription():
    segments, info = model.transcribe(
        "command.wav",
        language="en"
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()

def getCommand():
    wakeListen()

    recorded = listen()

    if not recorded:
        print("Friday: no command detected.")
        return ""

    command = transcription()

    print("You:", command)

    return command