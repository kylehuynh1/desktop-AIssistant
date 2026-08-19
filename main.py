from fileSniffer import fileSniffer
from tools import open_app


print("Friday's here.")

runner = True

# Scan installed applications once when Friday starts
apps = fileSniffer()


while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False

    elif command.startswith("open "):
        app = command[5:]
        open_app(app, apps)

    else:
        print("Friday: you said: " + command)