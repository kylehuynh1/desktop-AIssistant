import threading
import time

import numpy as np
import soundcard as sc
import pythoncom

import visualState


running = True


def systemAudioLoop():

    # ========================================================
    # INITIALIZE WINDOWS COM FOR THIS THREAD
    # ========================================================

    pythoncom.CoInitialize()

    try:

        # ====================================================
        # FIND DEFAULT WINDOWS OUTPUT DEVICE
        # ====================================================

        speakers = sc.default_speaker()

        print(
            f"Friday Visual: monitoring system audio -> "
            f"{speakers.name}"
        )


        # ====================================================
        # CREATE WASAPI LOOPBACK DEVICE
        # ====================================================

        loopback = sc.get_microphone(
            id=str(speakers.id),
            include_loopback=True
        )

        print(
            "Friday Visual: system audio loopback active."
        )


        # ====================================================
        # CAPTURE WINDOWS OUTPUT
        # ====================================================

        with loopback.recorder(
            samplerate=48000
        ) as recorder:

            while running:

                try:

                    # Small chunks = responsive visualization
                    audio = recorder.record(
                        numframes=1024
                    )

                    if audio.size == 0:
                        continue


                    # =========================================
                    # CALCULATE AUDIO ENERGY
                    # =========================================

                    audioFloat = audio.astype(
                        np.float32
                    )

                    rms = np.sqrt(
                        np.mean(
                            np.square(
                                audioFloat
                            )
                        )
                    )


                    # =========================================
                    # NORMALIZE FOR VISUALIZER
                    # =========================================

                    # System audio normally has relatively
                    # small RMS values, so amplify it visually.
                    level = min(
                        rms * 8.0,
                        1.0
                    )


                    # =========================================
                    # SEND TO FRIDAY VISUAL BODY
                    # =========================================

                    visualState.setSystemAudioLevel(
                        level
                    )


                except Exception as e:

                    print(
                        f"System audio capture error: {e}"
                    )

                    time.sleep(
                        0.5
                    )


    except Exception as e:

        print(
            f"Friday Visual: system audio failed: {e}"
        )


    finally:

        # ====================================================
        # CLEAN UP COM
        # ====================================================

        pythoncom.CoUninitialize()


def startSystemAudio():

    thread = threading.Thread(
        target=systemAudioLoop,
        daemon=True
    )

    thread.start()

    return thread


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    startSystemAudio()

    print(
        "System audio test running..."
    )

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        running = False

        print(
            "System audio test stopped."
        )