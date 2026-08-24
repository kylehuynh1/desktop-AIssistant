import sys
import threading


# ============================================================
# WINDOWS AUDIO / COM
#
# IMPORTANT:
# pycaw uses comtypes. Load tools BEFORE PySide6 and
# SoundCard so comtypes gets first shot at COM initialization.
# ============================================================

from tools import (
    adjustVolume,
    open_app,
    close_app,
    set_volume,
    unmute_volume,
    mute_volume,
    media_play_pause,
    media_stop,
    media_next,
    media_previous
)


# ============================================================
# OTHER FRIDAY MODULES
# ============================================================

from fileSniffer import fileSniffer
from windowSniffer import windowSniffer

from manager import (
    find,
    focus,
    minimize,
    maximize
)

from localCpu import askLocal

from voiceCMD import (
    getCommand,
    getCommandAfterInterrupt,
    wakeModel
)

from tts import speak


# ============================================================
# VISUAL BODY
# ============================================================

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from visuals import FridayWindow

import visualState


# ============================================================
# SYSTEM AUDIO
#
# Keep this AFTER tools/pycaw and Qt imports.
# ============================================================

from sysAudio import startSystemAudio


# ============================================================
# GLOBAL STATE
# ============================================================

runner = True

# If Friday is interrupted while speaking,
# the new command gets stored here
pendingCommand = None


# ============================================================
# APPLICATION SCAN
# ============================================================

# Scan installed applications once when Friday starts
apps = fileSniffer()


# ============================================================
# STARTUP DISPLAY
# ============================================================

def startupDisplay():

    print(r"""
    ███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗
    ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝
    █████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝
    ██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝
    ██║     ██║  ██║██║██████╔╝██║  ██║   ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝

                 F.R.I.D.A.Y.
          Desktop Intelligence System

    [✓] Wake Engine
    [✓] Speech Recognition
    [✓] Local Intelligence
    [✓] System Control
    [✓] Voice Synthesis
    [✓] Visual Interface

    STATUS: ONLINE
    Waiting for wake phrase...
    """)


# ============================================================
# FRIDAY TOOLS
# ============================================================

def fridayOpenApp(app: str):
    """
    Open, launch, show, focus, switch to,
    or bring up an application.

    If the application is already running,
    bring its window to the foreground.

    Otherwise launch the application.
    """

    visualState.setActiveTool("OPEN APP")

    hwnd = find(app)

    if hwnd:

        success = focus(hwnd)

        if success:
            return f"{app} was successfully focused."

        return f"{app} is running but could not be focused."


    success = open_app(
        app.lower(),
        apps
    )

    if success:
        return f"{app} was successfully launched."

    return f"{app} could not be launched."


def fridayCloseApp(app: str):
    """
    Close, kill, quit, terminate,
    exit, or shut down a running application.
    """

    visualState.setActiveTool("CLOSE APP")

    result = close_app(
        app.lower()
    )

    if result:
        return f"{app} was successfully closed."

    return f"{app} could not be closed."


def fridaySetVolume(volume: int):
    """Set system volume."""

    visualState.setActiveTool("VOLUME")

    set_volume(volume)

    return (
        f"System volume was successfully "
        f"set to {volume}%."
    )


def fridayMute():
    """Mute system volume."""

    visualState.setActiveTool("AUDIO")

    mute_volume()

    return "System volume was successfully muted."


def fridayUnmute():
    """Unmute system volume."""

    visualState.setActiveTool("AUDIO")

    unmute_volume()

    return "System volume was successfully unmuted."


def fridayAdjustVolume(amount: int):
    """
    Increase or decrease Windows volume
    by a percentage amount.
    """

    visualState.setActiveTool("VOLUME")

    adjustVolume(amount)

    return (
        f"System volume was successfully "
        f"adjusted by {amount}%."
    )


def fridayMinimize(app: str):
    """Minimize a running application."""

    visualState.setActiveTool("WINDOW CONTROL")

    success = minimize(app)

    if success:
        return f"{app} was successfully minimized."

    return (
        f"{app} could not be minimized because "
        f"no matching window was found."
    )


def fridayMaximize(app: str):
    """Maximize a running application."""

    visualState.setActiveTool("WINDOW CONTROL")

    success = maximize(app)

    if success:
        return f"{app} was successfully maximized."

    return (
        f"{app} could not be maximized because "
        f"no matching window was found."
    )


def fridayReturnWindows():
    """
    Return currently open Windows windows.
    """

    visualState.setActiveTool("WINDOW SCAN")

    windows = windowSniffer()

    titles = []

    for window in windows:
        titles.append(
            window["title"]
        )

    return titles


def fridayPlayPause():
    """
    Play, pause, or resume active media.
    """

    visualState.setActiveTool("MEDIA")

    return media_play_pause()


def fridayNextTrack():
    """Skip to next media item."""

    visualState.setActiveTool("MEDIA")

    return media_next()


def fridayPreviousTrack():
    """Return to previous media item."""

    visualState.setActiveTool("MEDIA")

    return media_previous()


def fridayStopMedia():
    """Stop currently playing media."""

    visualState.setActiveTool("MEDIA")

    return media_stop()


# ============================================================
# TOOL LIST
# ============================================================

fridayTools = [

    fridayOpenApp,
    fridayCloseApp,

    fridaySetVolume,
    fridayMute,
    fridayUnmute,
    fridayAdjustVolume,

    fridayMinimize,
    fridayMaximize,
    fridayReturnWindows,

    fridayPlayPause,
    fridayNextTrack,
    fridayPreviousTrack,
    fridayStopMedia
]


# ============================================================
# FRIDAY BACKEND LOOP
# ============================================================

def fridayLoop():

    global runner
    global pendingCommand

    visualState.setState("IDLE")
    visualState.setActiveTool("NONE")

    while runner:

        try:

            # =================================================
            # WAITING / WAKE DETECTION
            # =================================================

            visualState.setState("IDLE")
            visualState.setActiveTool("NONE")

            # If Friday was interrupted,
            # use that command immediately.
            if pendingCommand:

                command = pendingCommand
                pendingCommand = None

            else:

                command = getCommand()


            # Nothing useful was recorded
            if not command:
                continue


            # =================================================
            # COMMAND RECEIVED
            # =================================================

            visualState.setLastCommand(
                command
            )

            visualState.setState(
                "THINKING"
            )


            # =================================================
            # FRIDAY SHUTDOWN
            # =================================================

            cleanCommand = (
                command
                .lower()
                .strip()
                .rstrip(".!?")
            )


            if cleanCommand in [

                "go offline",
                "shut down friday",
                "shutdown friday",
                "terminate",
                "goodbye friday"

            ]:

                print(
                    "Friday: going offline."
                )

                visualState.setState(
                    "OFFLINE"
                )

                speak(
                    "Going offline."
                )

                runner = False

                continue


            # =================================================
            # LOCAL AI
            # =================================================

            response = askLocal(
                command,
                tools=fridayTools
            )


            # =================================================
            # RESPONSE / TTS
            # =================================================

            if response:

                print(
                    "Friday:",
                    response
                )

                print(
                    "DEBUG: about to call speak"
                )

                visualState.setState(
                    "SPEAKING"
                )

                interrupted = speak(
                    response,
                    wakeModel=wakeModel
                )


                # =============================================
                # INTERRUPTION
                # =============================================

                if interrupted:

                    print(
                        "Friday: listening."
                    )

                    visualState.setState(
                        "LISTENING"
                    )

                    pendingCommand = (
                        getCommandAfterInterrupt()
                    )

                else:

                    visualState.setState(
                        "IDLE"
                    )


        # =====================================================
        # CTRL+C
        # =====================================================

        except KeyboardInterrupt:

            print(
                "\nFriday: terminating."
            )

            visualState.setState(
                "OFFLINE"
            )

            runner = False


        # =====================================================
        # ERROR
        # =====================================================

        except Exception as e:

            print(
                f"Friday: error: {e}"
            )

            visualState.setState(
                "ERROR"
            )


# ============================================================
# START FRIDAY
# ============================================================

if __name__ == "__main__":

    startupDisplay()
    startSystemAudio()

    # ========================================================
    # QT APPLICATION
    # ========================================================

    app = QApplication(
        sys.argv
    )


    # ========================================================
    # FRIDAY VISUAL BODY
    # ========================================================

    fridayVisual = FridayWindow()

    fridayVisual.show()


    # ========================================================
    # BACKEND THREAD
    # ========================================================

    backendThread = threading.Thread(
        target=fridayLoop,
        daemon=True
    )

    backendThread.start()


    # ========================================================
    # VISUAL STATE SYNCHRONIZATION
    # ========================================================

    def syncVisualState():

        # Outer microphone visualizer
        fridayVisual.setEnvironmentLevel(
            visualState.getEnvironmentLevel()
        )

        # Inner Friday voice visualizer
        fridayVisual.setFridayVoiceLevel(
            visualState.getFridayVoiceLevel()
        )

        # Current Friday state
        fridayVisual.setState(
            visualState.getState()
        )

        # Last voice command
        fridayVisual.setLastCommand(
            visualState.getLastCommand()
        )

        # Current tool
        fridayVisual.setActiveTool(
            visualState.getActiveTool()
        )


    # Update body ~60 times per second
    visualSyncTimer = QTimer()

    visualSyncTimer.timeout.connect(
        syncVisualState
    )

    visualSyncTimer.start(
        16
    )


    # ========================================================
    # START QT EVENT LOOP
    # ========================================================

    exitCode = app.exec()

    runner = False

    sys.exit(
        exitCode
    )