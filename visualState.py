environmentLevel = 0.0
fridayVoiceLevel = 0.0
systemAudioLevel = 0.0
state = "IDLE"
lastCommand = "SYSTEM READY"
activeTool = "NONE"


def setEnvironmentLevel(level):
    global environmentLevel

    environmentLevel = max(
        0.0,
        min(float(level), 1.0)
    )


def getEnvironmentLevel():
    return environmentLevel


def setFridayVoiceLevel(level):
    global fridayVoiceLevel

    fridayVoiceLevel = max(
        0.0,
        min(float(level), 1.0)
    )


def getFridayVoiceLevel():
    return fridayVoiceLevel


def setState(newState):
    global state
    state = str(newState).upper()


def getState():
    return state


def setLastCommand(command):
    global lastCommand
    lastCommand = str(command)


def getLastCommand():
    return lastCommand


def setActiveTool(tool):
    global activeTool
    activeTool = str(tool)


def getActiveTool():
    return activeTool

def setSystemAudioLevel(level):
    global systemAudioLevel

    systemAudioLevel = max(
        0.0,
        min(float(level), 1.0)
    )


def getSystemAudioLevel():
    return systemAudioLevel