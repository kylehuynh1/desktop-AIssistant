import os
import subprocess
from pycaw.pycaw import AudioUtilities

process_names = {
    "spotify": "Spotify.exe",
    "visual studio code": "Code.exe",
    "vscode": "Code.exe"
}

def open_app(app, apps):
    try:
        app_path = apps[app]

        os.startfile(app_path)

        print(f"Friday: now opening {app}.")

    except KeyError:
        print(
            f"Friday: I couldn't find '{app}' "
            "in your installed applications."
        )

    except OSError:
        print(
            f"Friday: I found '{app}', "
            "but Windows couldn't launch it."
        )

def close_app(app):
    app = app.lower()

    if app in process_names:
        process = process_names[app]
    else:
        process = app + ".exe" 

    result = subprocess.run(
        ["taskkill", "/IM", process, "/F"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Friday: now closing {app}.")
    else:
        print(f"Friday: I couldn't close {app}.")


def set_volume(volume):
    volume = int(volume)
    if volume < 0:
        volume = 0
    elif volume > 100:
        volume = 100
        
    volumeScalar = volume / 100 #windows audio value conversion
    device = AudioUtilities.GetSpeakers()
    volume_control = device.EndpointVolume
    volume_control.SetMasterVolumeLevelScalar(volumeScalar, None)

    print(f"Friday: volume set to {volume}%.")

def unmute_volume():
    device = AudioUtilities.GetSpeakers()
    volume_control = device.EndpointVolume
    volume_control.SetMute(0, None)
    print(f"Friday: audio now unmuted.")

def mute_volume():
    device = AudioUtilities.GetSpeakers()
    volume_control = device.EndpointVolume
    volume_control.SetMute(1, None)
    print(f"Friday: audio now muted.")

def adjustVolume(volume):
    volume = int(volume)

    specification = volume / 100 #windows audio value conversion
    device = AudioUtilities.GetSpeakers()
    volume_control = device.EndpointVolume
    currentScalar = volume_control.GetMasterVolumeLevelScalar()
    adjustScalar = currentScalar + specification

    if adjustScalar < 0:
        adjustScalar = 0
    elif adjustScalar > 1:
        adjustScalar = 1

    volume_control.SetMasterVolumeLevelScalar(adjustScalar, None)
