# Utilities Version 1.0

import os, sys, re

# If os.name == nt then the script runs on windows
def checkOSSystem(mPath):
    if os.name == "nt":                
        return re.sub(r"/", "\\\\", mPath)
    else:        
        return re.sub(r"\\", "/", mPath)

# Check if returns nothing with sys.argv[0]. If its true then check the os to correct the path   
def findParentPath(nameOfFile):
    if os.path.dirname(sys.argv[0]) != "":
        # We add this append only because... when we run as script and not as app then the parent path includes the 'Module' folder. When you run it as app then it doesn't see the folder 'Modules' in parent path
        partsOfPath = os.path.dirname(sys.argv[0]).split(checkOSSystem('/'))
        if partsOfPath[-1] == 'Modules':
            return checkOSSystem(os.path.dirname(sys.argv[0]) + "\\" + nameOfFile)
        return checkOSSystem(os.path.dirname(sys.argv[0]) + "\\Modules\\" + nameOfFile)
    else:   
        return checkOSSystem(nameOfFile)

# Function which verifies that a file exist
def checkIfFileExists(filePath):
    if os.path.isfile(filePath):
        return True
    else:
        raise Exception("Given path ("+filePath+") of file doesn't exist. Please correct the given path and try again !")


# Function that takes a path of the file and returns only the path
def extractPath(mPath):    
    if os.name == "nt": # Windows                
        return "\\".join(mPath.split("\\")[0:-1])
    else: # Unix
        return "/".join(mPath.split("/")[0:-1])