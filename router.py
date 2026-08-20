from tools import open_app

def routeLocal(command, apps):
    command = command.lower()

    if command.startswith("open "):
        app = command[5:].strip()
        if app in apps:
            open_app(app, apps)
            return True
    return False