import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from openwakeword.model import Model
import numpy as np
import visualState


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

    # Dashboard state while waiting for wake word
    visualState.setState("IDLE")

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

            # --------------------------------
            # MICROPHONE VISUAL LEVEL
            # --------------------------------

            micLevel = np.abs(
                audio.astype(np.float32)
            ).mean()

            micLevel = min(
                micLevel / 3000.0,
                1.0
            )

            visualState.setEnvironmentLevel(
                micLevel
            )

            # --------------------------------
            # WAKE DETECTION
            # --------------------------------

            prediction = wakeModel.predict(audio)
            score = prediction["hey_jarvis"]

            if score > 0.05:
                print("wake score:", score)

            if score > 0.5:
                print("Friday: listening.")

                # Dashboard now immediately shows LISTENING
                visualState.setState("LISTENING")

                wakeModel.reset()
                return


def listen():
    print("now listening...")

    # Make sure dashboard stays in listening state
    visualState.setState("LISTENING")

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

            if overflowed:
                print("audio overflow")

            # --------------------------------
            # MICROPHONE VISUAL LEVEL
            # --------------------------------

            flatAudio = audio.flatten()

            micLevel = np.abs(
                flatAudio.astype(np.float32)
            ).mean()

            micLevel = min(
                micLevel / 3000.0,
                1.0
            )

            visualState.setEnvironmentLevel(
                micLevel
            )

            # --------------------------------
            # RECORD AUDIO
            # --------------------------------

            audioChunks.append(
                audio.copy()
            )

            # Average volume of this chunk
            volume = np.abs(audio).mean()

            totalTime += blockDuration

            # --------------------------------
            # SPEECH / SILENCE DETECTION
            # --------------------------------

            if volume > silenceThreshold:
                speaking = True
                silenceTime = 0

            elif speaking:
                silenceTime += blockDuration

                if silenceTime >= silenceLimit:
                    break

    # --------------------------------
    # NOTHING SPOKEN
    # --------------------------------

    if not speaking:
        return False

    # --------------------------------
    # SAVE COMMAND
    # --------------------------------

    audio = np.concatenate(
        audioChunks
    )

    write(
        "command.wav",
        rate,
        audio
    )

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

    # --------------------------------
    # WAIT FOR WAKE WORD
    # --------------------------------

    wakeListen()

    # --------------------------------
    # RECORD COMMAND
    # --------------------------------

    recorded = listen()

    if not recorded:
        print("Friday: no command detected.")

        visualState.setState("IDLE")

        return ""

    # --------------------------------
    # TRANSCRIBE
    # --------------------------------

    command = transcription()

    print("You:", command)

    return command


def getCommandAfterInterrupt():

    # No wakeListen() here because Friday was
    # already interrupted by the wake phrase.
    visualState.setState("LISTENING")

    recorded = listen()

    if not recorded:
        print("Friday: no command detected.")

        visualState.setState("IDLE")

        return ""

    command = transcription()

    print("You:", command)

    return command