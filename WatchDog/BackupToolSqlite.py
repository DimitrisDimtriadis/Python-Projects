# BackupToolSqlite version 1.0

import watchDogUtilities as ut
import sys, os, pathlib

backupDir = "BackupDB" 

# Main function of the script to back the sqlite3 db
def main(pathForDB, filesLimitationPerDir=50):
    # If doesn't exist create the main folder where will save the back up files
    checkExistanceOrCreateDir(ut.findParentPath(backupDir))
    # Get the name of db to use it on next function
    dbName = extractNameFromPath(pathForDB)
    # If doesn't exist the folder where will save the db backup. Create it
    folderPathForProject = ut.checkOSSystem(ut.findParentPath(backupDir)+"\\" +dbName)
    checkExistanceOrCreateDir(folderPathForProject)
    '''Need to fix the backup process first'''
    # checkIfExceedBackupLimitation(folderPathForProject, filesLimitationPerDir)
    print("OK")

# Function that extract the name of base
def extractNameFromPath(mPath, needExtension=False):
    # If it is Windows    
    if os.name == "nt":
        tempStringList = mPath.split("\\")
    # If it is Unix
    else:
        tempStringList = mPath.split("/")
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
            print("Creation of directory %s failed !" % dirPath)
        else:
            print("Successfully created the directory %s " % dirPath)

# Function that checks how many backups containt in dir. And If exceed remove some files to avoid conflicts
def checkIfExceedBackupLimitation(mPathForDir, limitNum):
    dirListing = os.listdir(mPathForDir)
    numOfFileInFolder = len(dirListing)
    # Check if folders exceed the size of given limitation
    ''' remove TRUE trig before release'''
    if numOfFileInFolder >= limitNum or True: 
        # The number of files to delete in 'Backup project' folder
        numberOfFilesToDelte = numOfFileInFolder - limitNum
        for xx in dirListing:
            fname = pathlib.Path(ut.checkOSSystem(mPathForDir+"\\"+xx)).stat()
            print(fname)        
        print("Files need to delete: " + str(numberOfFilesToDelte))        

# Start of the script that checks the given arguments
if __name__ == "__main__":
    # The number of arguments that user user
    numOfArg = len(sys.argv)
    # arg[1] = Path for DB
    if numOfArg == 2:
        # Call the main function wit
        # h checking if db exist (simultaneously)xaxax
        main(ut.checkIfFileExists(ut.checkOSSystem(sys.argv[1])))
    # arg[1] = Path for DB, arg[2] = Limit of files per directory
    elif numOfArg == 3:
        # Call the main function with checking if db exist (simultaneously)        
        try:
            ut.checkIfFileExists(ut.checkOSSystem(sys.argv[1]))
            main(ut.checkOSSystem(sys.argv[1]), filesLimitationPerDir=int(sys.argv[2]))
        except ValueError:        
            print("The second argument is Invalid ! : %s" %ValueError)
    else:
        print("Script require argument(s) to start. Please visit ToolTutorial.txt to learn more about it.")