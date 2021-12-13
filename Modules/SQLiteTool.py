# SqliteQueryTools version 1.0
import sqlite3
from AppSettings import appsettings
from sqlite3 import Error
import Utilities as ut

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
def dbUPDATE(dbConnection, tableName, fieldsList, valueList, whereStatementText=''):

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

# Create a database connection to a SQLite database
def dbCreateDatabase():    
    conn = None
    try:
        conn = sqlite3.connect(ut.checkOSSystem(ut.findParentPath(appsettings.DB_FILE_PATH)))
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

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