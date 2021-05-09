import sys
import SqliteQueryTools as sqlT
import watchDogUtilities as ut
import CustomeModels as cModels

# Names of files that script needs
nameOfEmailMessage = "flatFilesUtil/message.txt"
dbPath = ut.findParentPath("DBUtil/watchDogDB.sqlite")

mSubTitle = "Hey, see what's new today!"
messageTemplate = '''<div id="image" style="display: inline-block; margin: 20px;"><img style="font-size: 14px; float: left; margin-right: 10px;" src="%s" width="60" />
    <p style="float: left;">%s <br /><span style="font-size: 8px;">IMDB: </span>%s</p>
    </div>'''

def createMessageToSendWithEmail(mTableName, pathForMessageFile='', pathForDatabase=''):
    # Create the whole path for message.txt and watchDog.sqlite files
    if pathForMessageFile != '':
        messagePath = pathForMessageFile
    else:        
        messagePath = ut.findParentPath(nameOfEmailMessage)    
    # Create db Connection
    if pathForDatabase != '':
        dbConnection = sqlT.dbOpenConnection(str(pathForDatabase))
    else:
        dbConnection = sqlT.dbOpenConnection(dbPath)

    # Fetch all wanted data from base
    moviesList = sqlT.dbSELECT(dbConnection, mTableName, whereStatementText="Notified = 1")

    # If it doen't contain any data to send EXIT with this code to notify bash script
    if len(moviesList) == 0:
        # Custom exit code to avoid misleading on main pipe of script
        sys.exit(33)
    
    # Create (If doesn't exist) message.txt or clean it to create a new message
    msgFile = open(messagePath, "w")

    # Add headline
    if len(moviesList) > 1:
        msgFile.write(str(len(moviesList)) + " new movies ! \n")
    else:
        msgFile.write("1 new movie ! \n")

    msgFile.write("<html><body>")
    msgFile.write(mSubTitle)
    for row in moviesList:
        # Create a Movie Model to manipulate easier the data
        tempMovieObj = cModels.Movie(row["ID"], row['Title'], row['Grade'], row['ImageUrl'], row['Notified'], row['EntryDate'], row['ModifyDate'])
        # Add on message.txt file a new line with info for this movie
        msgFile.write(messageTemplate % (tempMovieObj.imgURL, tempMovieObj.title, str(tempMovieObj.grade)))
    
    msgFile.write("</html></body>")
    # Close db connection
    sqlT.dbCloseConnection(dbConnection)

# When append all movies to message.txt then we need to mark them as readed
def updateDBThatUserReceiveTheInfo(mTableName, pathForDatabase=''):

    # Open Connection with db
    if pathForDatabase != '':
        dbConnection = sqlT.dbOpenConnection(pathForDatabase)
    else:
        dbConnection = sqlT.dbOpenConnection(dbPath)
        
    # Mark entries ass seen
    sqlT.dbUPDATE(dbConnection, mTableName, ['Notified'], [0], "Notified = 1")

    #Close the connection
    sqlT.dbCloseConnection(dbConnection)

# Function that finds which function need to be call for the right project based on table's name
def decideActiveProjectBasedOnTable(mTableName, itsUpdate, pathForMsg="", pathForDB=""):
    # For Movies Watch Dog project
    if mTableName.lower() == 'moviestb':
        if itsUpdate:
            # Update data on base
            updateDBThatUserReceiveTheInfo('MoviesTb', pathForDB)
        else:
            # Just create the message to send
            createMessageToSendWithEmail('MoviesTb', pathForMessageFile=pathForMsg, pathForDatabase=pathForDB)
    else:
        print('Wrong table name. Please try again !')
        

# Main part of script. Decide what user need the script do
if __name__=="__main__":
    # Check if script call with input
    # 1) tableName
    if len(sys.argv) == 2:
        decideActiveProjectBasedOnTable(sys.argv[1], False)
    # 2) tableName update
    elif len(sys.argv) == 3 and sys.argv[2] == 'update':
        decideActiveProjectBasedOnTable(sys.argv[1], True)
    # 3) tableName pathForMessage
    elif len(sys.argv) == 3:
        usersPathForMsg = ut.checkOSSystem(sys.argv[2])        
        decideActiveProjectBasedOnTable(sys.argv[1], False, usersPathForMsg)
    # 4) tableName pathForDb update
    elif len(sys.argv) == 4 and sys.argv[3] == 'update':
        print(ut.checkOSSystem(sys.argv[2]))
        if ut.checkIfFileExists(ut.checkOSSystem(sys.argv[2])):
            usersPathForDB = ut.checkOSSystem(sys.argv[2])
        decideActiveProjectBasedOnTable(sys.argv[1], True, pathForDB=usersPathForDB)
    # 5) tableName pathForMessage pathForDb
    elif len(sys.argv) == 4:
        usersPathForMsg = ut.checkOSSystem(sys.argv[2])
        if ut.checkIfFileExists(ut.checkOSSystem(sys.argv[3])):
            usersPathForDB = ut.checkOSSystem(sys.argv[3])
        decideActiveProjectBasedOnTable(sys.argv[1], False, pathForMsg=usersPathForMsg, pathForDB=usersPathForDB)
    else:
        print("Something went wrong with the arguments. Please visit the WatchDogTutorial.txt for more informations")