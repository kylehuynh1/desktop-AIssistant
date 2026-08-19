from fileSniffer import fileSniffer
from tools import open_app
from cpu import askGEM

print("Friday's here.")

runner = True

# Scan installed applications once when Friday starts
apps = fileSniffer()


while runner:
    command = input("You: ")

    if command == "exit":
        print("Friday: terminating.")
        runner = False
    else:
        action, target = askGEM(command)

        if action == "open_app":
            open_app(target.lower(), apps) #case sensitivity  
        elif action == "respond":
            print(f"Friday: {target}")        

    