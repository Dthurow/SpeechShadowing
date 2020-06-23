global infoMessage
infoMessage = None
global errorMessage
errorMessage = None
global root
root = None

def displayErrorMessage(err):
    global errorMessage
    global root
    print(err)
    if errorMessage is not None:
        errorMessage.set(err)
        root.update()
    else:
        print("error message var is not set")

def displayInfoMessage(msg):
    global infoMessage
    global root
    print(msg)
    if infoMessage is not None:
        infoMessage.set(msg)
        root.update()
    else:
        print("info message var is not set")

