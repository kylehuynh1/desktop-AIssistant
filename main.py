from fileSniffer import fileSniffer
from tools import open_app
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

while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False
    else:
        handled = routeLocal(command, apps)
        if handled == False:
            response = askLocal(command, tools=[fridayOpenApp])
            if response:
                print("Friday:", response)

    