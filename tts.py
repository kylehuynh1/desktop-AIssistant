import sounddevice as sd
from piper import PiperVoice
from scipy.signal import resample_poly
import io
import wave
import numpy as np

import visualState


# ============================================================
# LOAD FRIDAY VOICE
# ============================================================

voice = PiperVoice.load(
    "voices/en_GB-cori-high.onnx"
)


# ============================================================
# CONVERT TTS AUDIO -> VISUAL LEVEL
# ============================================================

def getVoiceLevel(audioChunk):

    if len(audioChunk) == 0:
        return 0.0

    # Convert to float before squaring
    audioFloat = audioChunk.astype(
        np.float32
    )

    # RMS = actual energy of this piece of speech
    rms = np.sqrt(
        np.mean(
            np.square(audioFloat)
        )
    )

    # Piper audio is int16, so its RMS values
    # are much larger than normalized audio.
    #
    # Tune this divisor later if we want the
    # core more/less sensitive.
    level = rms / 6000.0

    return max(
        0.0,
        min(level, 1.0)
    )


# ============================================================
# SPEAK
# ============================================================

def speak(text, wakeModel=None):

    # --------------------------------------------------------
    # GENERATE PIPER AUDIO
    # --------------------------------------------------------

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wavFile:
        voice.synthesize_wav(
            text,
            wavFile
        )

    buffer.seek(0)

    with wave.open(buffer, "rb") as wavFile:

        outputRate = wavFile.getframerate()

        channels = wavFile.getnchannels()

        audio = wavFile.readframes(
            wavFile.getnframes()
        )

    audio = np.frombuffer(
        audio,
        dtype=np.int16
    )


    # ========================================================
    # NORMAL NON-INTERRUPTIBLE TTS
    # ========================================================
    #
    # Used for things such as:
    #
    # "Going offline."
    #
    # We still want the center core to indicate that
    # Friday is speaking.
    # ========================================================

    if wakeModel is None:

        visualState.setFridayVoiceLevel(
            0.7
        )

        try:

            sd.play(
                audio,
                outputRate
            )

            sd.wait()

        finally:

            visualState.setFridayVoiceLevel(
                0.0
            )

        return False


    # ========================================================
    # RESAMPLE FOR WAKE DETECTION
    # ========================================================

    # openWakeWord expects 16 kHz.
    #
    # The full-duplex stream runs at 16 kHz so both
    # microphone input and speaker output share the
    # same stream rate.

    streamRate = 16000

    if outputRate != streamRate:

        audio = resample_poly(
            audio,
            streamRate,
            outputRate
        )

        audio = np.clip(
            audio,
            -32768,
            32767
        ).astype(
            np.int16
        )


    # ========================================================
    # INTERRUPTIBLE TTS
    # ========================================================

    blockSize = 1280

    audioPosition = 0

    interrupted = False

    wakeModel.reset()


    # ========================================================
    # AUDIO CALLBACK
    # ========================================================

    def audioCallback(
        indata,
        outdata,
        frames,
        time,
        status
    ):

        nonlocal audioPosition
        nonlocal interrupted


        if status:

            print(
                "audio status:",
                status
            )


        # ====================================================
        # SPEAKER OUTPUT
        # ====================================================

        outdata[:] = 0

        remaining = (
            len(audio)
            - audioPosition
        )

        amount = min(
            frames,
            remaining
        )


        if amount > 0:

            # Get THIS exact chunk of Friday's voice
            voiceChunk = audio[
                audioPosition:
                audioPosition + amount
            ]


            # -----------------------------------------------
            # SEND AUDIO TO SPEAKERS
            # -----------------------------------------------

            outdata[
                :amount,
                0
            ] = voiceChunk


            # -----------------------------------------------
            # SEND FRIDAY VOICE LEVEL TO VISUAL BODY
            # -----------------------------------------------

            voiceLevel = getVoiceLevel(
                voiceChunk
            )

            visualState.setFridayVoiceLevel(
                voiceLevel
            )


            # -----------------------------------------------
            # MOVE FORWARD THROUGH TTS AUDIO
            # -----------------------------------------------

            audioPosition += amount


        else:

            # Friday isn't outputting anything
            visualState.setFridayVoiceLevel(
                0.0
            )


        # ====================================================
        # MICROPHONE / WAKE DETECTION
        # ====================================================

        micAudio = indata[
            :,
            0
        ].copy()


        prediction = wakeModel.predict(
            micAudio
        )

        score = prediction[
            "hey_jarvis"
        ]


        if score > 0.05:

            print(
                "interrupt wake score:",
                score
            )


        # ====================================================
        # INTERRUPT DETECTED
        # ====================================================

        if score > 0.5:

            print(
                "Friday: interrupted."
            )

            interrupted = True

            # Immediately kill Friday's visual voice level
            visualState.setFridayVoiceLevel(
                0.0
            )

            raise sd.CallbackStop()


        # ====================================================
        # TTS FINISHED
        # ====================================================

        if audioPosition >= len(audio):

            visualState.setFridayVoiceLevel(
                0.0
            )

            raise sd.CallbackStop()


    # ========================================================
    # FULL DUPLEX AUDIO STREAM
    # ========================================================

    try:

        with sd.Stream(
            samplerate=streamRate,
            blocksize=blockSize,
            channels=1,
            dtype="int16",
            callback=audioCallback
        ) as stream:

            while stream.active:

                sd.sleep(
                    50
                )


    finally:

        # Always return the inner core to idle,
        # including if TTS crashes or is interrupted.

        visualState.setFridayVoiceLevel(
            0.0
        )


    # ========================================================
    # RESET WAKE MODEL
    # ========================================================

    wakeModel.reset()


    # ========================================================
    # RETURN INTERRUPTION STATE
    # ========================================================

    return interrupted