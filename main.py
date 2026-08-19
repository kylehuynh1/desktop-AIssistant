import subprocess
import os
from fileSniffer import fileSniffer

print("Friday's here.")
runner = True 

def open_app(app):
    try:
        app_path = apps[app]
        os.startfile(app_path)
        print(f"Friday: now opening {app}.")

    except KeyError:
        print(f"Friday: I couldn't find '{app}' in your installed applications.")

    except FileNotFoundError:
        print(f"Friday: I found '{app}', but couldn't launch it.")

apps = fileSniffer()  # Call the fileSniffer function to get the apps dictionary

while runner:
    command = input("You: ")


    if command == "exit":
        print("Friday: terminating.")
        runner = False 
    elif command.startswith("open "):
        app = command[5:]  # Remove "open " from the command
        open_app(app)
    else:
        print("Friday: you said: " + command)

     