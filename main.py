from fileSniffer import fileSniffer
from tools import open_app
from cpu import askGEM

print("Friday's here.")

runner = True

# Scan installed applications once when Friday starts
apps = fileSniffer()

def fridayOpenApp(app: str):
    open_app(app.lower(), apps) #open installed apps on users computer

while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False
    else:
        answer = askGEM(command, [fridayOpenApp])
        print(f"Friday: {answer}")

    