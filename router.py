from tools import open_app

def routeLocal(command, apps):
    if command.startswith("open "):
        app = command[5:]
        open_app(app.lower(), apps)
        return True
    else:
        return False
        