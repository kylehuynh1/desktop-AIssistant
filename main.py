from fileSniffer import fileSniffer
from tools import open_app, close_app
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


while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False
    else:
        handled = routeLocal(command, apps)
        if not handled:
            response = askLocal(command, tools=[fridayOpenApp, fridayCloseApp])
            if response:
                print("Friday:", response)

    