import SQLiteTool as sqlT
import Utilities as ut
from AppSettings import appsettings
import Models as cModels
from AppSettings import appsettings


def createMessageToSendWithEmail(mTableName):
    # Create the whole path for message.txt and watchDog.sqlite files
    messagePath = ut.findParentPath(appsettings.EMAIL_MESSAGE_PATH)    
    # Full path for the DB
    dbPath = ut.findParentPath(appsettings.DB_FILE_PATH)
    # Create db Connection
    dbConnection = sqlT.dbOpenConnection(dbPath)
    # Fetch all wanted data from base
    moviesList = sqlT.dbSELECT(dbConnection, mTableName, whereStatementText="Notified = 1")    
    
    # Create (If doesn't exist) message.txt or clean it to create a new message
    msgFile = open(messagePath, "w")

    # Add headline
    if len(moviesList) > 1:
        msgFile.write(str(len(moviesList)) + " new movies ! \n")
    else:
        msgFile.write("1 new movie ! \n")

    msgFile.write("<html><body>")
    msgFile.write(appsettings.MSG_SUB_TITLE)
    for row in moviesList:
        # Create a Movie Model to manipulate easier the data
        tempMovieObj = cModels.Movie(row["ID"], row['Title'], row['Grade'], row['ImageUrl'], row['Notified'], row['EntryDate'], row['ModifyDate'])
        # Add on message.txt file a new line with info for this movie
        msgFile.write(appsettings.MSG_MAIN_BODY_TEMPLATE % (tempMovieObj.imgURL, tempMovieObj.title, str(tempMovieObj.grade)))
    
    msgFile.write("</html></body>")
    # Close db connection
    sqlT.dbCloseConnection(dbConnection)

# Function that called to use it as a start
def main():
    createMessageToSendWithEmail(appsettings.APP_MOVIES_TABLE)

# Main part of script. Decide what user need the script do
if __name__=="__main__":
    main()