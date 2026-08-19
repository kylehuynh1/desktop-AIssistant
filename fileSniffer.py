from pathlib import Path
start_menu = Path("C:/Users/rando/AppData/Roaming/Microsoft/Windows/Start Menu/Programs")

def fileSniffer():
    apps = {}

    for item in start_menu.rglob("*"):
        if(item.is_file() and item.suffix == ".lnk"):
            apps[item.stem.lower()] = item #send application name&pathing to apps dictionary

    return apps