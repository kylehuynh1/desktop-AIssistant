from fileSniffer import fileSniffer
from tools import adjustVolume, open_app, close_app, set_volume, unmute_volume, mute_volume
from cpu import askGEM
from router import routeLocal
from localCpu import askLocal

print("Friday's here.")

runner = True

# Scan installed applications once when Friday starts
apps = fileSniffer()

def fridayOpenApp(app: str):
    """open installed apps on users computer"""
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

while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False
    else:
        handled = routeLocal(command, apps)
        if not handled:
            response = askLocal(command, tools=[fridayOpenApp, fridayCloseApp, fridaySetVolume, fridayMute, fridayUnmute, fridayAdjustVolume])
            if response:
                print("Friday:", response)

    