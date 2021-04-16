import sqlite3
import SqliteQueryTools as sqlT
import watchDogUtilities as ut
import CustomeModels as cModels

# Names of files that script needs
nameOfEmailMessage = "flatFilesUtil/message.txt"
dbPath = ut.findParentPath("DBUtil/watchDogDB.sqlite")

def createMessageToSendWithEmail():
    # Create the whole path for message.txt and watchDog.sqlite files
    messagePath = ut.findParentPath(nameOfEmailMessage)    

    # Create (If doesn't exist) message.txt or clean it to create a new message
    msgFile = open(messagePath, "w")

    # Create db Connection
    dbConnection = sqlT.dbOpenConnection(dbPath)

    # Fetch all wanted data from base
    moviesList = sqlT.dbSELECT(dbConnection, "MoviesTb", whereStatementText="Notified = 1")
    
    # Add headline
    msgFile.write("New (" + str(len(moviesList)) + ") movies : \n")     

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
    createMessageToSendWithEmail()
    print("ok")
    createMessageToSendWithEmail()   
    updateDBThatUserReceiveTheInfo()