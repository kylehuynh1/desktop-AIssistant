import os
import subprocess

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
