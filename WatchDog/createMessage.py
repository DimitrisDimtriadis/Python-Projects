import sqlite3, sys
import SqliteQueryTools as sqlT
import watchDogUtilities as ut
import CustomeModels as cModels

# Names of files that script needs
nameOfEmailMessage = "flatFilesUtil/message.txt"
dbPath = ut.findParentPath("DBUtil/watchDogDB.sqlite")

def createMessageToSendWithEmail():
    # Create the whole path for message.txt and watchDog.sqlite files
    messagePath = ut.findParentPath(nameOfEmailMessage)    

    # Create db Connection
    dbConnection = sqlT.dbOpenConnection(dbPath)

    # Fetch all wanted data from base
    moviesList = sqlT.dbSELECT(dbConnection, "MoviesTb", whereStatementText="Notified = 1")

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

    for row in moviesList:
        tempMovieObj = cModels.Movie(row["ID"], row['Title'], row['Grade'], row['ImageUrl'], row['Notified'], row['EntryDate'], row['ModifyDate'])

        #Add on message.txt file a new line with info for this movie
        msgFile.write("* Name: " + tempMovieObj.title + " || " + str(tempMovieObj.grade) + " \n " + tempMovieObj.imgURL + "\n\n" )
    
    # Close db connection
    sqlT.dbCloseConnection(dbConnection)

# When append all movies to message.txt then we need to mark them as readed
def updateDBThatUserReceiveTheInfo():

    # Open Connection with db
    dbConnection = sqlT.dbOpenConnection(dbPath)
        
    # Mark entries ass seen
    sqlT.dbUPDATE(dbConnection, "MoviesTb", ['Notified'], [0], "Notified = 1")

    #Close the connection
    sqlT.dbCloseConnection(dbConnection)

if __name__=="__main__":

    # Check if script call with input
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        # Update data on base
        updateDBThatUserReceiveTheInfo()
        print("!!! Mark them as read !!!")    
    else:
        # Just create the message to send
        createMessageToSendWithEmail()
        print("!!! Create message !!!")    