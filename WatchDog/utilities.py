import os, sys, re

def checkOSSystem(mPath):
    # If os.name == nt then the script runs on windows
    if os.name == "nt" and False:                
        return mPath
    else:        
        newPath = re.sub(r"\\", "/", mPath)
        return newPath

def findParentPath(nameOfFile):
    # Check if returns nothing with sys.argv[0]. If its true then check the os to correct the path   
    if os.path.dirname(sys.argv[0]) != "":
        return checkOSSystem(os.path.dirname(sys.argv[0]) + "\\" + nameOfFile)    
    else:   
        return checkOSSystem(nameOfFile)
