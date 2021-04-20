# SqliteQueryTools version 1.0
import sqlite3, sys
from sqlite3 import Error
import OSUtilities as ut

dbForTestingPath = "DBUtil\watchDogDB.sqlite"
# Creater a database connection to a sqlite database
def dbOpenConnection(dbFile):
    try:
        tempConnection = sqlite3.connect(dbFile)
        # print("DB connection OPEN !")
        #Returns the connection to execute the sql commands
        return tempConnection
    except sqlite3.Error:
        print(Error)
    return None

# If connection already exist. Close it
def dbCloseConnection(connectionToClose):
    if connectionToClose:
        connectionToClose.close()
        # print("DB connection CLOSE !")

# Function we need to execute SELECT command to given connection (DB)
def dbSELECT(dbConnection, tableName, fieldsToReturn=None, whereStatementText=None):
    
    sql = "SELECT "
    if fieldsToReturn:
        sql = setValuesInQuery(sql, fieldsToReturn, ' FROM ' + tableName, isField=True)
    else:
        sql += '* FROM ' + tableName
    if whereStatementText:
        sql += ' WHERE ' + whereStatementText
    
    mCursor = dbConnection.cursor()
    mCursor.execute(sql)
    mRows = mCursor.fetchall()
    mDictList = returnDictWithFieldAndValues(mCursor, mRows)
    return mDictList
        
# Function we need to execute INSERT command to given connection (DB)
def dbINSERT(dbConnection, tableName, fieldsList, valueList):
    #Catch error with wrong number of fields or values
    if len(fieldsList) != len(valueList):
        raise Exception("Number of fields differ from values")
        
    sql = "INSERT INTO "+ tableName + "("
    sql = setValuesInQuery(sql, fieldsList, ") VALUES(", isField=True)
    sql = setValuesInQuery(sql, valueList, ")")
    executeQuery(dbConnection, sql)

# Function we need to execute UPDATE command to given connection (DB)
def dbUPDATE(dbConnection, tableName, fieldsList, valueList, whereStatementText):

    if len(fieldsList) != len(valueList):
        raise Exception("Number of fields differ from values")
    
    sql = "UPDATE " + tableName + " SET "
    sql = setValuesInQuery(sql, valueList, " ", fieldsList)
    if whereStatementText != '':
        sql += "WHERE " + whereStatementText
    executeQuery(dbConnection, sql)

def dbDELETE(dbConnection, tableName, whereStatementText):
    
    if whereStatementText == '':
        sql = "DELETE FROM " + tableName
    else:
        sql = "DELETE FROM " + tableName + " WHERE " + whereStatementText

    executeQuery(dbConnection, sql)

# Function to execute a custom query user gave.
def dbCustomQuery(dbConnection, customQuery):
    mRes = executeCustomQuery(dbConnection, customQuery)
    if mRes:
        return mRes

# Get all the column names from a given table of db
def dbGetColumnNames(dbConnection, mTable):
    mCursor = dbConnection.execute("SELECT * FROM " + mTable)
    return list(map(lambda x:x[0], mCursor.description))

# Function that returns all the tables that db contains
def dbGetTableOfDB(mConnection):
    cursor = mConnection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()

# To avoid repeate the bellow code. It just execute the given sql query to base
def executeQuery(mConnection, mSQL):
    mCursor = mConnection.cursor()
    mCursor.execute(mSQL)
    mConnection.commit()

def executeCustomQuery(mConnection, mSQL):
    mCursor = mConnection.cursor()
    mCursor.execute(mSQL)
    nRows = mCursor.fetchall()
    if nRows != []:
        return returnDictWithFieldAndValues(mCursor, nRows)
    else:
        mConnection.commit()

# Function that returns a list with dictionaries that on key they have the field name and on value the value of the field
# It was created to support SELECT queries
def returnDictWithFieldAndValues(nCursor, mRows):
    
    fieldNames = list(map(lambda x:x[0], nCursor.description))
    dictList = []

    for row in mRows:
        # for field in 
        tempDict = {}
        mCount = 0 
        for keyField in fieldNames:
            tempDict[keyField] = row[mCount]
            mCount += 1
        dictList.append(tempDict)
    return dictList

# Simple definition which takes values and if it is string then add '' for query
def checkIfNeedsTextSymbolForQuery(mVal, isField=False):
    if isinstance(mVal, str) and not isField:
        return '\'' + str(mVal) + '\''
    return str(mVal)

# Simple return 'field = value' to append it on UPDATE query
def setEqualityForQuery(mField, mVal):
     return mField + "=" + mVal

# A For-loop to add all the value to query from a list with values
def setValuesInQuery(mQuery, valueList, stringToAppendOnEnd, equalFields=None, isField=False):
    
    for i, mVal in enumerate(valueList):
        if i != 0: mQuery += ',' #Append , between values
        if equalFields:
            mQuery += setEqualityForQuery(equalFields[i], checkIfNeedsTextSymbolForQuery(mVal))
        else:
            mQuery += checkIfNeedsTextSymbolForQuery(mVal, isField)
              
    mQuery += stringToAppendOnEnd
    return mQuery

# The main function that called when you excecute te file.
# I basically create it to test function of the class 
def main():
    """ We need to make openConnectionToDB to throw exception if it find an error to avoid any problem """
    dbConnection = dbOpenConnection(ut.checkOSSystem(ut.findParentPath(dbForTestingPath)))    
    # dbCustomQuery(dbConnection, "INSERT INTO MoviesTb (Title, Grade, Notified) VALUES('Darksiders', 6, 0)")    
    mRes = dbSELECT(dbConnection, "MoviesTb", fieldsToReturn=['title', 'id'])    
    # mRes = dbGetColumnNames(dbConnection, "MoviesTb")
    for row in mRes:
        print(row)
    dbCloseConnection(dbConnection)    

# Main function which called when user add argument. It is the main algorithm to manipulate the base
def manualMain():
    
    # After secure that script runned with argument, we save it on a variable
    pathToDb = sys.argv[1]
    defaultChoises = ["SELECT", "DELETE", "UPDATE", "INSERT", "CUSTOM"]    
    # Open the connection with db
    dbConnection = dbOpenConnection(ut.checkOSSystem(pathToDb))
    mTrig = False

    while True:
            
        print("\n\n______________________________________________")
        print("Please select the number of on the following mode:")
        print("(1) SELECT on a specific table")
        print("(2) DELETE rows on a specific table")
        print("(3) UPDATE rows on a specific table")
        print("(4) INSERT rows on a specific table")
        print("(5) Custom query on a specif table")
        print("(6) Just show all TABLE of db file")
        print("(7) Just show all COLUMN Names of a specific table in db")
        print("If you want to exit from program just insert 'exit'.\n")
        
        userEntered = input()
        print("\n")
        try:                
            if userEntered.lower() == "exit":
                remoteClose(dbConnection)
            # User select to create a CUSTOM query
            elif int(userEntered)-1 == 4: 
                # Here is the custom query because it doesn't need to choose on which table you want to work                                        
                remoteCustomQuery(dbConnection)                    
                mTrig = True
            # User select to him the TABLES of db
            elif int(userEntered)-1 == 5:                     
                remoteShowTablesAndReturnThem(dbConnection, "*")
                mTrig = True
            # User select to show him all the COLUMN names of a specific table
            elif int(userEntered)-1 == 6: 
                print("Please choose the number of table you want to learn its column names.")
                ductionaryWithTables = remoteShowTablesAndReturnThem(dbConnection)       
                print("If you want to exit from program just insert 'exit'.\n")

                modeTrig = True
                while modeTrig:
                    userInput = input()
                    print("\n")
                    try:            
                        if userInput.lower() == "exit":
                            remoteClose(dbConnection)
                        elif int(userInput)-1 in ductionaryWithTables.keys():
                            tbNames = dbGetColumnNames(dbConnection, ductionaryWithTables[int(userInput)-1])
                            for name in tbNames:
                                print(" - "+name)
                            modeTrig = False
                        else:
                            print("No valid choice. Please try again !")    
                    except TypeError:
                        print("No valid choice. Please try again !")
                    except ValueError:
                        print("No valid choice. Please try again !")
                mTrig = True
            elif int(userEntered)-1 < len(defaultChoises) and int(userEntered)-1 >= 0:
                remoteMode(dbConnection, defaultChoises[int(userEntered)-1])        
                mTrig = True
            else:
                print("Your write a invalid command. Please try again !") 
            
            # Triger to ask user if he want to continue on making queries
            if mTrig:
                
                while mTrig:                         
                    print("\nDo you want to execute another one command ? (Y/N):", end="")
                    userContinueInput = input()
                    
                    if userContinueInput.lower() == 'n':
                        remoteClose(dbConnection) 
                    elif userContinueInput.lower() == 'y':
                        mTrig = False
                        print("Continue using app.")
                    else: 
                        print("Invalid command. Please try again !")

        except ValueError:
            print("Your write a invalid command. Please try again !") 
    
# Functionality of manual manipulation of base
def remoteMode(mConnection, mMode):
    
    print("Please choose on which table you want to work:")
    # Create a dictionary with table to use it later for user choice
    dictionaryWithTables = remoteShowTablesAndReturnThem(mConnection)
    print("If you want to exit from program just insert 'exit'.\n")
    
    modeTrig = True
    while modeTrig:
        userInput = input()
        print("\n")
        try:            
            if userInput.lower() == "exit":
                return
            elif int(userInput)-1 in dictionaryWithTables.keys():
                executeUserChoise(mConnection, mMode, dictionaryWithTables[int(userInput)-1])
                modeTrig = False
            else:
                print("No valid choice. Please try again! 1")    
        except TypeError:
            print("No valid choice. Please try again! 2")
        except ValueError:
            print("No valid choice. Please try again! 3")

    
# After taking connection, user table choise and mode, we execute the command
def executeUserChoise(mConnection, mMode, mTable):
    
    if mMode == "SELECT" or mMode == "UPDATE" or mMode == "INSERT":
        remoteSetFieldsValues(mConnection, mTable, mMode)
        print("...Done")                    
    elif mMode == "DELETE":
        whereStatementText = remoteAskUserForInput("Please provide a valid WHERE statement (without write the word 'WHERE' ! )")        
        dbDELETE(mConnection, mTable, whereStatementText)
        print("...Done")
    else:
        print("Something went wrong")

# A simple function that ask from user to write sql to send it to sqlite3 to execute SQL query
def remoteCustomQuery(mConnection):
    userQuery = remoteAskUserForInput("\nPlease write a SQL query and then press 'ENTER'. \n")
    mRes = dbCustomQuery(mConnection, userQuery)
    if mRes:
        for row in mRes:
            print(row)

# Ask from user to provide something to use it for remote-manual mode
def remoteAskUserForInput(textForUser):
    print(textForUser)
    return input()    

# Function to close smoothly app and db
def remoteClose(mConnection):
    # Close the db connection before exit the code
    dbCloseConnection(mConnection)
    sys.exit(66) 

# Set Fields and values 
def remoteSetFieldsValues(mConnection, mTable, mMode):    
    print("\nUse some of the following columns to create the " + mMode + " query in " + mTable+ " table:")
    names = dbGetColumnNames(mConnection, mTable)
    for name in names:
        print("*" + name)

    tempListWithColumns = []
    tempListWithColumnsValue = []
    columnTrig = True
    print('''\nPlease insert only ONE name of column and press the button 'Enter'.\nYou can repeat this step to implement as many column you want.
    \nIf you want to add all fields just write '*' (works only for SELECT). \nTo end this procedure just write '-' and press 'Enter'. ''')         
    while columnTrig:
        userInput = input()
        if userInput == '*' or userInput == '-':
            columnTrig = False
        elif userInput != "":
            print(userInput)
            tempListWithColumns.append(str(userInput))
        else:
            print("Invalid argument. Try again")
    
    # if true then it means that we need to *
    if len(tempListWithColumns) == 0 and mMode == 'SELECT':        
        
        whereText = remoteAskUserForInput("Please write a valid WHERE statement (without adding the word 'where'). If you don't want to add 'where' statement just press 'Enter'.")
        if whereText == "":
            mRes = dbSELECT(mConnection, mTable)
        else:
            mRes = dbSELECT(mConnection, mTable, whereStatementText=whereText)
        # Show results
        for row in mRes:
            print(row)

    elif len(tempListWithColumns) != 0:
        
        if mMode == 'SELECT':
            whereText = remoteAskUserForInput("Please write a valid WHERE statement (without adding the word 'where'). If you don't want to add 'where' statement just press 'Enter'.")
            if whereText == "":
                mRes = dbSELECT(mConnection, mTable, tempListWithColumns)
            else:
                mRes = dbSELECT(mConnection, mTable, tempListWithColumns, whereText)
            # Show results
            for row in mRes:
                print(row)            
        else:
            print("Please add to wanted value on each given field")
            for col in tempListWithColumns:
                print(col+"= ", end="")
                mUserInput = input()
                # Add values for each 
                tempListWithColumnsValue.append(str(mUserInput))

            if mMode == 'UPDATE':
                
                whereText = remoteAskUserForInput("Please write a valid WHERE statement (without adding the word 'where'). If you don't want to add 'where' statement just press 'Enter'.")                
                if whereText == "":
                    dbUPDATE(mConnection, mTable, tempListWithColumns, tempListWithColumnsValue)
                else:
                    dbUPDATE(mConnection, mTable, tempListWithColumns, tempListWithColumnsValue, whereText)                

            elif mMode == 'INSERT':
                dbINSERT(mConnection, mTable, tempListWithColumns, tempListWithColumnsValue) 
    else:
        print("Something went wrong with adding column names. Please try again from the beginning")
        remoteClose(mConnection)

# Create a dict with tables name and it prints them.
def remoteShowTablesAndReturnThem(mConnection, textPrefix=""):
    tempDict = {}                    
    for i, mTables in enumerate(dbGetTableOfDB(mConnection)):
        # Get table's name
        tempDict[i] = mTables[0]
        if textPrefix == "":
            print("("+str(i+1)+") " + mTables[0])
        else:
            print(textPrefix + " " + mTables[0])
    return tempDict
    
# Main function that script starts
if __name__ == '__main__':    
    # If user called script without argument execute the default main function
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        ut.checkIfFileExists(sys.argv[1])
        manualMain()       
    else: 
        print("You should add only one argument and that is the path of db to manipulate db")