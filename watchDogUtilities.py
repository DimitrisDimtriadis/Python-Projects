# watchDogUtilities Version 1.0

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
        return checkOSSystem(os.path.dirname(sys.argv[0]) + "\\" + nameOfFile)    
    else:   
        return checkOSSystem(nameOfFile)

# Function which verifies that a file exist
def checkIfFileExists(filePath):
    if os.path.isfile(filePath):
        return True
    else:
        raise Exception("Given path ("+filePath+") of file doesn't exist. Please correct the given path and try again !")