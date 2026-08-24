from fileSniffer import fileSniffer
from windowSniffer import windowSniffer
from tools import adjustVolume, open_app, close_app, set_volume, unmute_volume, mute_volume
from manager import find, focus, minimize, maximize
from cpu import askGEM
from router import routeLocal
from localCpu import askLocal
from voiceCMD import getCommand
from tts import speak
runner = True

#scans installed applications once when Friday starts
apps = fileSniffer()

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

    STATUS: ONLINE
    Waiting for wake phrase...
    """)


def fridayOpenApp(app: str):
    """
    Open, launch, show, focus, switch to, or bring up an application.
    If the application is already running, bring its window to the foreground.
    Otherwise, launch the application.
    """
    hwnd = find(app)

    if hwnd:
        success = focus(hwnd)

        if success:
            return f"{app} was successfully focused."

        return f"{app} is running but could not be focused."

    success = open_app(app.lower(), apps)

    if success:
        return f"{app} was successfully launched."

    return f"{app} could not be launched."

def fridayCloseApp(app: str):
    """
    Close, kill, quit, terminate, exit, or shut down a running application.
    Use this tool when the user asks to close or kill an application.
    """
    result = close_app(app.lower())

    if result:
        return f"{app} was successfully closed."

    return f"{app} could not be closed."

def fridaySetVolume(volume: int):
    """set volume on users computer"""
    set_volume(volume)
    return f"System volume was successfully set to {volume}%."

def fridayMute():
    """mutes volume on user computer"""
    mute_volume()

def fridayUnmute():
    """unmutes the volume on user computer"""
    unmute_volume()

def fridayAdjustVolume(amount: int):
    """Increase or decrease the current Windows volume by a percentage amount. Use positive values to increase and negative values to decrease."""
    adjustVolume(amount)

def fridayMinimize(app: str):
    """Minimize an already running application window."""

    success = minimize(app)

    if success:
        return f"{app} was successfully minimized."

    return f"{app} could not be minimized because no matching window was found."

def fridayMaximize(app: str):
    """Maximize an already running application window."""

    success = maximize(app)

    if success:
        return f"{app} was successfully maximized."

    return f"{app} could not be maximized because no matching window was found."

def fridayReturnWindows():
    """Return a list of currently open windows on the user's computer."""
    windows = windowSniffer()
    titles=[]

    for window in windows:
        titles.append(window["title"])

    return titles

startupDisplay()

while runner:
    try:
        command = getCommand()

        cleanCommand = command.lower().strip().rstrip(".!?")

        if cleanCommand in [
            "go offline",
            "shut down friday",
            "shutdown friday",
            "terminate",
            "goodbye friday"
        ]:
            print("Friday: going offline.")
            speak("Going offline.")
            runner = False
            continue

        # Only reaches Qwen if it wasn't a shutdown command
        response = askLocal(command, tools=[
            # your tools
        ])

        if response:
            print("Friday:", response)
            speak(response)

    except KeyboardInterrupt:
        print("\nFriday: terminating.")
        runner = False

    except Exception as e:
        print(f"Friday: error: {e}")