# LogTool version 1.2
from enum import Enum
from datetime import datetime
import os, re, time
from AppSettings import appsettings
from inspect import getframeinfo, stack
from pathlib import Path

# Path where the program will find or create the Developement/Production folder to save the loggers
# If variable is equal to "" then use the current folder
pathForFolderWithLoggers = appsettings.LOGGER_FILES_PATH
# Maximum size of each file to avoid the big files !!! In MegaBytes (MB) !!!
# If it is equal to -1 then, there is no limitation on each file
maxSizeOfEachFile = float(appsettings.LOGGER_FILE_MAX_SIZE)

# Profiles that we will use them for diffrent actions
class LogProfile(Enum):
    D = "Development"
    P = "Production"
# Choose which profile is active
activeProfile = appsettings.LOGGER_ACTIVE_PROFILE

# Statuses that we will use them to be easier to distrinct the log
class LogStatus(Enum):
    D = "DEBUG"
    I = "INFO"
    W = "WARNING"
    E = "ERROR"
    L = "LOADING"

class Logger():    
    # The other files will call this function with specific arguments to update log file
    def __init__(self, profileToImplement, statusOfLog, textToWrite, DictionaryForVariables=[]):
        
        if profileToImplement == LogProfile.D and activeProfile.value == LogProfile.P.value:
            return
        # Path of folder where we will place/edit log file
        folderPath = self.profileLogFolder(profileToImplement)
        # if Logger.profileLogFolder is None then exit the procedure
        if not folderPath:
            # Do not log anything
            return
            
        # Check if we need to create new log file or to append on a existing one
        caller = getframeinfo(stack()[1][0])
        callerLine = caller.lineno
        callerFilename = caller.filename.split(self.checkOSSystem("/"))[-1]
        logFileToAddInfo = self.nameOfLogFile(folderPath)

        # Message to append
        logToAppendInFile = '- ' + self.timestampInString() + statusOfLog.value + " (" + callerFilename + ":" + str(callerLine) + "): " + textToWrite     
        if not logFileToAddInfo:
            logFileToAddInfo = folderPath + '/' + str(round(datetime.now().timestamp() * 1000)) + '_log.txt'
        
        if len(DictionaryForVariables) != 0:
            for mKey in DictionaryForVariables.keys():
                logToAppendInFile += '\n\t ' + str(mKey) + ' = ' + str(DictionaryForVariables[mKey])
        
        if statusOfLog == LogStatus.L:
            self.writeOnSameLine(self.checkOSSystem(logFileToAddInfo), logToAppendInFile)
        else:
            self.writeOnFirstLine(self.checkOSSystem(logFileToAddInfo), logToAppendInFile)        
        
    # If os.name == nt then the script runs on windows
    def checkOSSystem(self, mPath):
        if os.name == "nt":                
            return re.sub(r"/", "\\\\", mPath)
        else:        
            return re.sub(r"\\", "/", mPath)

    # Function that used for retrieving the first part of Log which containts informations about time date and timezone    
    def timestampInString(self):
        # We take given timestamp and convert it to date to use it on format we want
        mDate = datetime.fromtimestamp(time.time())
        # sample of what we return '2021-Apr-28 11:34:21,233157 '
        return mDate.strftime("%Y-%b-%d %H:%M:%S,%f %z ")

    # Function that base on global var (pathForFolderWithLogger) return the right path
    def pathOfLogsFolder(self):
        # Get the whole path of Logger
        pathOfLogger = os.path.realpath(__file__)
        parentPath = str(Path(*Path(pathOfLogger).parts[:-1]))
        if pathForFolderWithLoggers == "":
            return self.checkOSSystem(parentPath+'/Logs')        
        else:
            return self.checkOSSystem(pathForFolderWithLoggers + '/Logs')

    #Check if 'Logs' folder exist If Logs dir doesn't exist, create it
    def createFolder(self, mPath):
        if not os.path.isdir(mPath):
            try:
                os.mkdir(mPath)
            except OSError:
                print("Creation of the directory %s failed !" % mPath)

    # Function that add on first line the given text
    def writeOnFirstLine(self, fileName, textToAdd):
        try:
            if os.path.exists(fileName):
                with open(fileName, 'r', encoding='utf-8') as readFile: data = readFile.read()
            else:
                data = ''
            # Write the data on file
            with open(fileName, 'w', encoding='utf-8') as writeFile: writeFile.write(textToAdd + '\n' + data)
        except Exception as e:
            print("Something happen on try to insert data in log. Error: " + str(e))
        except OSError as oe:
            print("Something happen on try to insert data in log. Error: " + str(oe))
    
    # Function that replace the first line in given text
    def writeOnSameLine(self, fileName, textToAdd):
        try:
            if os.path.exists(fileName):
                with open(fileName, 'r', encoding='utf-8') as readFile: data = readFile.read()
                # With the below lines we check if logger went on loop
                listText = data.split('\n')
                # Check if message on loop logger is the first to avoid losing data 
                if "LOADING" in listText[0]:
                    listText[0] = textToAdd
                else:
                    listText.insert(0, textToAdd)
                data = '\n'.join(listText)
            else:
                # If we don't have preivously log we dont do anything
                data = textToAdd
            # Write the data on file
            with open(fileName, 'w', encoding='utf-8') as writeFile: writeFile.write(data)
        except Exception as e:
            print("Something happen on try to insert data in log. Error: " + str(e))
        except OSError as oe:
            print("Something happen on try to insert data in log. Error: " + str(oe))

    # Function that gets the names from given folder to find the file name we want.
    # Returns either the name of file to append the text either nothing which means that we need to create a new folder
    def nameOfLogFile(self, folderPath):
        itemInFolder = os.listdir(folderPath)
        listWithLogs = []
        
        for item in itemInFolder:
            if re.match(r'[0-9]{9,}_log\.txt', item):
                listWithLogs.append(item)
        
        # If there is no file then stop
        if len(listWithLogs) == 0:
            return 

        try:
            lastUpdatedFile = self.checkOSSystem(folderPath + '/' + sorted(listWithLogs, reverse=True)[0])
            # Get the size of last updated file
            sizeOfFile = os.path.getsize(lastUpdatedFile)
            if maxSizeOfEachFile == -1 or maxSizeOfEachFile >= (sizeOfFile / 1000000):
                # returns the pathName of file we want to update
                return lastUpdatedFile
        except OSError:
            print("File doesn't exists !")
        
        # If return nothing then we create a new file on the next functions
        return 

    # Simple function that checks if folder for Logs (base on profile) exists or need to create it
    # It returns the path of folder we want to edit log
    def profileLogFolder(self, givenProfile):
        # Get the path we want to save the logs    
        pathOfLogsFolder = self.pathOfLogsFolder()
        #Check if 'Logs' folder exist If Logs dir doesn't exist, create it
        self.createFolder(pathOfLogsFolder)
        # Development mode
        developFolderPath = self.checkOSSystem(pathOfLogsFolder+'/'+LogProfile.D.value)
        self.createFolder(developFolderPath)
        
        if givenProfile == LogProfile.P and activeProfile == LogProfile.P:
            productFolderPath = self.checkOSSystem(pathOfLogsFolder+'/'+LogProfile.P.value)
            self.createFolder(productFolderPath)
            return productFolderPath
        elif givenProfile == LogProfile.D and activeProfile == LogProfile.P:        
            return
        
        return developFolderPath