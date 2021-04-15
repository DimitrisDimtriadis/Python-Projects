import sqlite3
from sqlite3 import Error

# Creater a database connection to a sqlite database
def openConnectionToDB(dbFile):
    try:
        tempConnection = sqlite3.connect(dbFile)
        print(sqlite3.version)
        #Returns the connection to execute the sql commands
        return tempConnection
    except Error:
        print(Error)
    return None

# If connection already exist. Close it
def closeConnectionToDB(connectionToClose):    
    if connectionToClose:
        connectionToClose.close()

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
    
    rows = mCursor.fetchall()
    for row in rows:
        print(row)
        
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
def dbUpdate(dbConnection, tableName, fieldsList, valueList, whereStatementText):
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
    print(sql)
    executeQuery(dbConnection, sql)

# To avoid repeate the bellow code. It just execute the given sql query to base
def executeQuery(mConnection, mSQL):
    mCursor = mConnection.cursor()
    mCursor.execute(mSQL)
    mConnection.commit()

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
    
if __name__ == '__main__':
    """ We need to make openConnectionToDB to throw exception if it find an error to avoid any problem """
    dbConnection = openConnectionToDB("D:\sTree\Python Tool\WatchDog\watchDogDB.sqlite")
    tempFields = ["Title", "Grade", "Notified", "ImageUrl"]
    tempValues = ["Actionman", 3.3, 0, "mUrl"]
    
    # dbINSERT(dbConnection, "MoviesTb", tempFields, tempValues)    
    # dbUpdate(dbConnection, "MoviesTb", tempFields, tempValues, "id = 1")
    dbSELECT(dbConnection, "MoviesTb", fieldsToReturn=['id', 'Title','Grade'])
    closeConnectionToDB(dbConnection)