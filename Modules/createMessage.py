import SQLiteTool as sqlT
import Utilities as ut
from AppSettings import appsettings
import Models as cModels
from AppSettings import appsettings


def createTxtMessage():
    # Create the whole path for message.txt and watchDog.sqlite files
    messagePath = ut.checkOSSystem(appsettings.EMAIL_MESSAGE_PATH)
    # Full path for the DB
    dbPath = ut.checkOSSystem(appsettings.DB_FILE_PATH)
    # Create db Connection
    dbConnection = sqlT.dbOpenConnection(dbPath)
    # Fetch all wanted data from base
    moviesList = sqlT.dbSELECT(dbConnection, appsettings.APP_MOVIES_TABLE, whereStatementText="Notified = 1")    
    
    # Create (If doesn't exist) message.txt or clean it to create a new message
    msgFile = open(messagePath, "w")

    # Add headline
    if len(moviesList) > 1:
        msgFile.write(str(len(moviesList)) + " new movies ! \n")
    elif len(moviesList) == 1:
        msgFile.write("1 new movie ! \n")
    else:
        return

    msgFile.write("<html><body>")
    msgFile.write(appsettings.MSG_SUB_TITLE)
    for row in moviesList:
        # Create a Movie Model to manipulate easier the data
        tempMovieObj = cModels.Movie(row["ID"], row['Title'], row['Grade'], row['ImageUrl'], row['Notified'], row['EntryDate'], row['ModifyDate'])
        # Add on message.txt file a new line with info for this movie
        msgFile.write(appsettings.MSG_MAIN_BODY_TEMPLATE % (tempMovieObj.imgURL, tempMovieObj.title, str(tempMovieObj.grade)))
    
    msgFile.write("</html></body>")
    msgFile.close()
    # Close db connection
    sqlT.dbCloseConnection(dbConnection)

# When append all movies to message.txt then we need to mark them as readed
def updateDataInDB():
    # Full path for the DB
    dbPath = ut.checkOSSystem(appsettings.DB_FILE_PATH)
    # Create db Connection
    dbConnection = sqlT.dbOpenConnection(dbPath)    
    # Mark entries ass seen
    sqlT.dbUPDATE(dbConnection, appsettings.APP_MOVIES_TABLE, ['Notified'], [0], "Notified = 1")
    #Close the connection
    sqlT.dbCloseConnection(dbConnection)

def cleanTxtMessage():
    # Create the whole path for message.txt and watchDog.sqlite files
    messagePath = ut.checkOSSystem(appsettings.EMAIL_MESSAGE_PATH)
    # It open it on 'w' mode and close it to erase it
    open(messagePath, "w").close()

# Main part of script. Decide what user need the script do
if __name__=="__main__":
    # For creating a message.txt
    createTxtMessage()
    # For mark data in db as seen
    updateDataInDB()
    # Clean the txt file
    cleanTxtMessage()
