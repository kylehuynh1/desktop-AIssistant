import os


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