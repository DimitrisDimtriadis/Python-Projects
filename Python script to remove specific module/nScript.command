#!/usr/bin/env python3
import shutil
import os
import sys

# Function: Checks if user added path of molude he wants to delete. And if he wasn't add one wait to write it
def checkIfLogFileIsEmpty(pathOfModule):
    
    while len(pathOfModule) == 0 :
        print("File 'log.txt' is empty. Please add a valid path in there\n")
        pathOfModule = input()
    
    return pathOfModule

print("\n\n")

# Get path of current script
pathOfScript = os.path.dirname(os.path.abspath(__file__))

# Open log.txt on specific path with "read" accsess
f = open("%s/log.txt" %pathOfScript, "r+")

# Read the text from log.txt
textPath = f.read()

pathOfModule = checkIfLogFileIsEmpty(textPath)

# Check for path existance to not append every time 
if textPath != pathOfModule {
    f.write(str(pathOfModule))
}
f.close

if len(pathOfModule) > 0 :
    # Check if file exists on path
    moduleFileToDelete = "%s/MobilityCommonLib.framework" % pathOfModule

    # Try to avoid show error message when try to remove module
    try :
        shutil.rmtree(moduleFileToDelete)
        print("Module was deleted successfully")

    except :
        print("Module not found! Please rebuild xcode project or check that path was added on log.txt.")
        # Command 'input' used for wait user's interaction
        input("Press Enter to continue...")

# Just simple spaces to make messages more clearly
print("\n\n")
