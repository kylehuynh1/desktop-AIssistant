from fileSniffer import fileSniffer
from tools import adjustVolume, open_app, close_app, set_volume, unmute_volume, mute_volume
from manager import find, focus, minimize, maximize
from cpu import askGEM
from router import routeLocal
from localCpu import askLocal

print("Friday's here.")

runner = True

# Scan installed applications once when Friday starts
apps = fileSniffer()

def fridayOpenApp(app: str):
    """
    Open, launch, show, focus, switch to, or bring up an application.
    If the application is already running, bring its window to the foreground.
    Otherwise, launch the application.
    """
    hwnd = find(app)

    if hwnd:
        focus(hwnd)
    else:
        open_app(app.lower(), apps)

def fridayCloseApp(app: str):
    """close installed apps on users computer"""
    close_app(app.lower())

def fridaySetVolume(volume: int):
    """set volume on users computer"""
    set_volume(volume)

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
    minimize(app)


def fridayMaximize(app: str):
    """Maximize an already running application window."""
    maximize(app)

while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False
    else:
        response = askLocal(command, tools=[
            fridayOpenApp, fridayCloseApp, fridaySetVolume, 
            fridayMute, fridayUnmute, fridayAdjustVolume, 
            fridayMinimize, fridayMaximize
            ])
        if response:
            print("Friday:", response)

    