# BackupToolSqlite version 1.0

import watchDogUtilities as ut
import sys, os, time, sqlite3, re

backupDir = "BackupDB"

# Main function of the script to back the sqlite3 db
def main(pathForDB, filesLimitationPerDir=50):
    # Get the name of db to use it on next function
    dbName = extractNameFromPath(pathForDB)
    dbLocatedPath = extractNameFromPath(pathForDB, needWholePath=True)
    dbBackupPath = ut.checkOSSystem(dbLocatedPath + "\\" + backupDir)    
    # If doesn't exist create the main folder where will save the back up files
    checkExistanceOrCreateDir(dbBackupPath)
    checkIfExceedBackupLimitation(dbBackupPath, filesLimitationPerDir, dbName)
    createBackUpFile(pathForDB, dbBackupPath)
    print("Backup for " + dbName + " finished")

# Function that extract the name of base
def extractNameFromPath(mPath, needExtension=False, needWholePath=False):
    # If it is Windows    
    if os.name == "nt":
        tempStringList = mPath.split("\\")
    # If it is Unix
    else:
        tempStringList = mPath.split("/")

    if needWholePath:
        # To seperate the string we need to now the number of substrings    
        sizeOfSubStrings = len(tempStringList)
        pathDBLocated = "\\".join(tempStringList[0:sizeOfSubStrings-1])        
        return ut.checkOSSystem(pathDBLocated)
    else:
        nameOfDB = tempStringList[-1]
        # Check if need to return name with extension or not
        if not needExtension:
            # Cut the extension
            nameOfDB = nameOfDB.split('.')[0]
        return nameOfDB

# Function that checks if dir (from path) exist in project and if it doesn't, It create it
def checkExistanceOrCreateDir(dirPath):
    # Check if dir exist
    if not os.path.exists(dirPath):
        try:
            # Create folder
            os.mkdir(dirPath)
        except OSError:
            raise Exception("Creation of directory %s failed !" % dirPath)
        else:
            print("Successfully created the directory %s " % dirPath)

def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

# Function that create a copy of db on specific folder
def createBackUpFile(pathForDB, pathForProjectBackUp):
    con = sqlite3.connect(pathForDB)
    # Get the name from path
    nameOfBackupFile = createFileName(extractNameFromPath(pathForDB, True))
    # Get the path for backups
    customPathForBackupFile = ut.checkOSSystem(pathForProjectBackUp + '/' + nameOfBackupFile)
    bck = sqlite3.connect(customPathForBackupFile)
    with bck:
        con.backup(bck, pages=1, progress=progress)
    bck.close()
    con.close()

# Function that checks how many backups containt in dir. And If exceed remove some files to avoid conflicts
def checkIfExceedBackupLimitation(mPathForDir, limitNum, dbNameWithoutExtinction):
    # List with files of given path    
    dirListing = os.listdir(mPathForDir)
    # Number of files in given path
    numOfFileInFolder = len(dirListing)
    # Check if folders exceed the size of given limitation
    if numOfFileInFolder >= limitNum: 
        # Create the test string for regex 
        regexString = r"\d+_"+ dbNameWithoutExtinction + r'(\.sqlite|\.db)'
        # The number of files to delete in 'Backup project' folder. Number with limit and one more to place the new one
        numberOfFilesToDelte = numOfFileInFolder - limitNum + 1 
        # List with the names of backup files
        listWithBackupFiles = []
        # Take one-one the names of files in given path to check if it is one of X oldest to delete later 
        for mFileName in dirListing:
            # Check if file is matching with naming standarts 
            if re.match(regexString, mFileName):
                # Add it to list to delete some of them later
                listWithBackupFiles.append(mFileName)
                    
        listWithBackupFilesRevSorted = sorted(listWithBackupFiles, reverse=True)
        # Use this number to set the limits of list you want to delete
        endOfMapToDelete = (0-numberOfFilesToDelte-1)
        # Get new map with filenames we want to delete
        filesToDelete = listWithBackupFilesRevSorted[-1:endOfMapToDelete:-1]
        print("Files need to delete: " + str(numberOfFilesToDelte))
        deleteGivenFileNames(filesToDelete, mPathForDir)

def deleteGivenFileNames(listWithFileNames, pathWhereFileLocated):
    for mFile in listWithFileNames:
        tempFileName = ut.checkOSSystem(pathWhereFileLocated + "\\" + mFile)
        if os.path.exists(tempFileName):
            os.remove(tempFileName)
        else:
            print("Error: Something went wrong with file name or its path !")

# Function that creates the name for back up file
def createFileName(dbName):
    # current timestamp with milisec
    mTimeStamp = round(time.time() * 1000)    
    return str(mTimeStamp) + "_" + dbName

# Start of the script that checks the given arguments
if __name__ == "__main__":
    # The number of arguments that user user
    numOfArg = len(sys.argv)
    # arg[1] = Path for DB
    if numOfArg == 2:
        # Call the main function wit
        # Checking if db exist (simultaneously)
        if ut.checkIfFileExists(ut.checkIfFileExists(sys.argv[1])):
            main(ut.checkOSSystem(sys.argv[1]))
        else:
            raise Exception("File of given db doesn't exist !")
    # arg[1] = Path for DB, arg[2] = Limit of files per directory
    elif numOfArg == 3:
        # Call the main function with checking if db exist (simultaneously)        
        try:
            ut.checkIfFileExists(ut.checkOSSystem(sys.argv[1]))
            main(ut.checkOSSystem(sys.argv[1]), filesLimitationPerDir=int(sys.argv[2]))
        except ValueError:        
            raise Exception("The second argument is Invalid ! : %s" %ValueError)
    else:
        raise Exception("Script require argument(s) to start. Please visit ToolTutorial.txt to learn more about it.")