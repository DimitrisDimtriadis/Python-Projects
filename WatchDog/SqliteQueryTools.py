import sqlite3, sys
from sqlite3 import Error
from typing import Type
import watchDogUtilities as ut

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
# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;
    if len(fieldsList) != len(valueList):
        raise Exception("Number of fields differ from values")
    if not whereStatementText or whereStatementText == '':
        raise Exception("WHERE statement in query is either 'None' either empty")
    
    sql = "UPDATE " + tableName + " SET "
    sql = setValuesInQuery(sql, valueList, " ", fieldsList)
    sql += "WHERE " + whereStatementText
    executeQuery(dbConnection, sql)

def dbDELETE(dbConnection, tableName, whereStatementText):
    
    if not whereStatementText or whereStatementText == '':
        raise Exception("WHERE statement in query is either 'None' either empty")
    
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
    tempFields = ["Title", "Notified"]
    tempValues = ["ok 123", 0]
    
    # dbINSERT(dbConnection, "MoviesTb", tempFields, tempValues)
    # dbUPDATE(dbConnection, "MoviesTb", tempFields, tempValues, "Notified = 0")
    # dbCustomQuery(dbConnection, "INSERT INTO MoviesTb (Title, Grade, Notified) VALUES('Darksiders', 6, 0)")
    # dbDELETE(dbConnection, "MoviesTb", "id != -1")
    # mRes = dbSELECT(dbConnection, "MoviesTb", fieldsToReturn=['title', 'id'])    
    mRes = dbGetColumnNames(dbConnection, "MoviesTb")
    for row in mRes:
        print(row)
    dbCloseConnection(dbConnection)    

# Main function which called when user add argument. It is the main algorithm to manipulate the base
def manualMain():
    
    # After secure that script runned with argument, we save it on a variable
    calledMode = sys.argv[1]
    defaultChoises = ["SELECT", "DELETE", "UPDATE", "INSERT", "CUSTOM"]
    
    # Open the connection with db
    dbConnection = dbOpenConnection(ut.checkOSSystem(ut.findParentPath(dbForTestingPath)))
    
    if calledMode == "db":    
        mTrig = False

        while True:
            
            print("\n\n______________________________________________")
            print("Please select the number of on the following mode:")
            print("(1) SELECT on a specific table")
            print("(2) DELETE rows on a specific table")
            print("(3) UPDATE rows on a specific table")
            print("(4) INSERT rows on a specific table")
            print("(5) Custom query on a specif table")
            print("If you want to exit from program just insert 'exit'.\n")
            
            userEntered = input()
            print("\n")
            try:                
                if userEntered.lower() == "exit":
                    return
                elif int(userEntered)-1 == 4: 
                    # Here is the custom query because it doesn't need to choose on which table you want to work                                        
                    remoteCustomQuery(dbConnection)                    
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
                            return 
                        elif userContinueInput.lower() == 'y':
                            mTrig = False
                            print("Continue using app.")
                        else: 
                            print("Invalid command. Please try again !")

            except ValueError:
                print("Your write a invalid command. Please try again !") 
    else:
        print("Wrong argument. The only argument at this point is 'db' !")

    # Close the db connection before exit the code
    dbCloseConnection(dbConnection)            

# Functionality of manual manipulation of base
def remoteMode(mConnection, mMode):

    print("Please choose on which table you want to work:")
    
    cursor = mConnection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # Create a dictionary with table to use it later for user choice
    dictionaryWithTables = {}

    for i, mTables in enumerate(cursor.fetchall()):
        # Get table's name
        dictionaryWithTables[i] = mTables[0]       
        print("("+str(i+1)+") " + dictionaryWithTables[i])

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
                print("No valid choice. Please try again !")    
        except TypeError:
            print("No valid choice. Please try again !")
        except ValueError:
            print("No valid choice. Please try again !")

# After taking connection, user table choise and mode, we execute the command
def executeUserChoise(mConnection, mMode, mTable):
    
    if mMode == "SELECT":
        print("...Done")
        # dbSELECT(mConnection, mTable, fieldsToReturn, whereStatementText)
    elif mMode == "DELETE":
        whereStatementText = remoteAskUserForInput("Please provide a valid WHERE statement (without write the word 'WHERE' ! )")        
        dbDELETE(mConnection, mTable, whereStatementText)
        print("...Done")
    elif mMode == "UPDATE":        
        print("...Done")
        # dbUPDATE(mConnection, mTable, fieldsList, valueList, whereStatementText)
    elif mMode == "INSERT":        
        print("...Done")
        # dbINSERT(mConnection, mTable, fieldsList, valueList)    
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

# Set Fields and values 
def remoteSetFieldsValues(mConnection, mTable):
    print("\nThe column names of '"+mTable+"' is: ")
    mNames = dbGetColumnNames(mConnection, mTable)
    for name in mNames:
        print("- " + name)
        print("Please write the fiels and the equal value. Do not use 'Enter' to seperate values. Use just ','.")

    
# Main function that script starts
if __name__ == '__main__':
    
    # If user called script without argument execute the default main function
    if len(sys.argv) == 1:
        main()
    else:
        manualMain()        
