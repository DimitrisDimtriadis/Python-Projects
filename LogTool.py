# LogTool version 1.0

from enum import Enum
from datetime import date, datetime
import os, re, sys

# Path where the program will find or create the Developement/Production folder to save the loggers
# If variable is equal to "" then use the current folder
pathForFolderWithLoggers = ""
# Maximum size of each file to avoid the big files !!! In MegaBytes (MB) !!!
# If it is equal to -1 then, there is no limitation on each file
maxSizeOfEachFile = -1

# Profiles that we will use them for diffrent actions
class LogProfile(Enum):
    D = "Development"
    P = "Production"
# Choose which profile is active
activeProfile = LogProfile.P

# Statuses that we will use them to be easier to distrinct the log
class LogStatus(Enum):
    D = "DEBUG"
    I = "INFO"
    W = "WARNING"
    E = "ERROR"

# If os.name == nt then the script runs on windows
def checkOSSystem(mPath):
    if os.name == "nt":                
        return re.sub(r"/", "\\\\", mPath)
    else:        
        return re.sub(r"\\", "/", mPath)

# Function that used for retrieving the first part of Log which containts informations about time date and timezone    
def retrieveTimeStampInStringFormat(mTimeStamp=datetime.now().timestamp()):
    # We take given timestamp and convert it to date to use it on format we want
    mDate = datetime.fromtimestamp(mTimeStamp)
    # sample of what we return '2021-Apr-28 11:34:21,233157 '
    return mDate.strftime("%Y-%b-%d %H:%M:%S,%f %z ")

# Function that base on global var (pathForFolderWithLogger) return the right path
def returnPathOfLogsFolder():
    if pathForFolderWithLoggers == "":
        return checkOSSystem(os.path.dirname(sys.argv[0])+'/Logs')        
    else:
        return checkOSSystem(pathForFolderWithLoggers + '/Logs')

#Check if 'Logs' folder exist If Logs dir doesn't exist, create it
def createFolder(mPath):
    if not os.path.isdir(mPath):
        try:
            os.mkdir(mPath)
        except OSError:
            print("Creation of the directory %s failed !" % mPath)

# Function that add on first line the given text
def writeTextOnFirstLine(fileName, textToAdd):
    if os.path.exists(fileName):
        with open(fileName, 'r') as readFile: data = readFile.read()
    else:
        data = ''
    with open(fileName, 'w') as writeFile: writeFile.write(textToAdd + '\n' + data)

# Function that gets the names from given folder to find the file name we want.
# Returns either the name of file to append the text either nothing which means that we need to create a new folder
def findNameOfFileToUpdateLog(folderPath):
    itemInFolder = os.listdir(folderPath)
    listWithLogs = []
    
    for item in itemInFolder:
        if re.match(r'[0-9]{9,}_log\.txt', item):
            listWithLogs.append(item)
    
    # If there is no file then stop
    if len(listWithLogs) == 0:
        return 

    try:
        lastUpdatedFile = checkOSSystem(folderPath + '/' + sorted(listWithLogs, reverse=True)[0])
        # Get the size of last updated file
        sizeOfFile = os.path.getsize(lastUpdatedFile)
        if maxSizeOfEachFile == -1 or maxSizeOfEachFile >= (sizeOfFile / 1000):
            # returns the pathName of file we want to update
            return lastUpdatedFile
    except OSError:
        print("File doesn't exists !")
    
    # If return nothing then we create a new file on the next functions
    return 

# Simple function that checks if folder for Logs (base on profile) exists or need to create it
# It returns the path of folder we want to edit log
def folderBasedOnProfile(givenProfile):
    # Get the path we want to save the logs    
    pathOfLogsFolder = returnPathOfLogsFolder()
    #Check if 'Logs' folder exist If Logs dir doesn't exist, create it
    createFolder(pathOfLogsFolder)
    # Development mode
    developFolderPath = checkOSSystem(pathOfLogsFolder+'/'+LogProfile.D.value)
    createFolder(developFolderPath)
    
    if givenProfile == LogProfile.P and activeProfile == LogProfile.P:
        productFolderPath = checkOSSystem(pathOfLogsFolder+'/'+LogProfile.P.value)
        createFolder(productFolderPath)
        return productFolderPath
    
    return developFolderPath

# The other files will call this function with specific arguments to update log file
def Log(profileToImplement, statusOfLog, textToWrite, listWithDictForVariables=[]):
    
    # Path of folder where we will place/edit log file
    folderPath = folderBasedOnProfile(profileToImplement)

    # Check if we need to create new log file or to append on a existing one
    logFileToAddInfo = findNameOfFileToUpdateLog(folderPath)

    # Message to append
    logToAppendInFile = '- ' + retrieveTimeStampInStringFormat() + statusOfLog.value + ": " + textToWrite     
    if not logFileToAddInfo:
        logFileToAddInfo = folderPath + '/' + str(round(datetime.now().timestamp() * 1000)) + '_log.txt'
    writeTextOnFirstLine(checkOSSystem(logFileToAddInfo), logToAppendInFile)

if __name__ == "__main__":
    Log(LogProfile.P, LogStatus.I, "Something went wrong here")
    # findNameOfFileToUpdateLog('D:\sTree\WatchDog\Logs\Development')