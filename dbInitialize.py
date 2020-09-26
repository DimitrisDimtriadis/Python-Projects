import sqlite3
import os
import sys 

projectPath = os.path.dirname(os.path.abspath(__file__))

# Function that check if given path is a valid DB path file
def checkValidationOfDBPath(pathForBase):
    # If already path exist on file, check if file is valid
    if len(pathForBase) != 0:
        try: 
            sqlite3.connect(pathForBase)
            # If file is valid set needToCreateNewBase as true to avoid enter on while loop
            return True
        except sqlite3.Error:
            return False
    else:
        return False


# Function that check if path for database exist
# If there is no database path make user add it and save it on pathFile
def getPathOfDB():
    
    nameOfDB = ''
    if sys.platform.__contains__("win"):
        # For windows enviroment
        nameOfDB = '\path.txt'
    else:
        # For linux enviroment
        nameOfDB = '/path.txt'
        
    # Open path.txt to get path of base. 
    # If file not exist, it creates a new one
    f = open(projectPath + nameOfDB, "r+")    
    
    # Read file to get path
    pathForBase = f.read()
    
    # Trigger to manipulate while loop
    needToStopInsertProcedure = checkValidationOfDBPath(pathForBase)

    while (len(pathForBase) == 0 or not os.path.exists(pathForBase) or not checkValidationOfDBPath(pathForBase)) and not needToStopInsertProcedure:
        
        if len(pathForBase) == 0:
            print("\nIt seems that there is no path for Database. Please add a valid path of database."
            + " If you don't have one, write 'new db' to create a new DB: ")

        # Get user input
        pathForBase = input()

        # Option to create a new base
        if pathForBase.lower() == 'new db':
            print("Set name for Database")
            dbName = input()
            print("The new base was created!")
            # Create new DB 
            sqlite3.connect(r"./"+dbName+".db")   
            # Set the path on var so function can return it      
            pathForBase = "./"+dbName+".db"
            # Stop while loop
            needToStopInsertProcedure = True
            # Save path on path.txt
            f.write(str(pathForBase))
        elif not os.path.exists(pathForBase) or not checkValidationOfDBPath(pathForBase):
            print("\nThis path is not valid! Please add a new path or write 'new db' to create a new one: \n")
        elif checkValidationOfDBPath(pathForBase): 
            print("\nAll about DB has been set!\n")
            # Save path on path.txt
            f.write(str(pathForBase))
            needToStopInsertProcedure = True
    
    mConnection = sqlite3.connect(pathForBase)
    mCursor = mConnection.cursor()
    qCheckTB = """ CREATE TABLE IF NOT EXISTS Movies_info(	
	                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
	                    Title TEXT NOT NULL,
	                    Grade REAL,
	                    IMDB INT
	                ); """
    
    mCursor.execute(qCheckTB)

    f.close()
    return pathForBase


# Main function of current script
if __name__ == "__main__":

    # Connect with database
    mConnection = sqlite3.connect(getPathOfDB())
    mCursor = mConnection.cursor()
    
    # Query to execute
    q1 = "Select * from Movies_info"
    
    # Execute query
    mCursor.execute(q1)
    
    # Fetch all result from query
    rows = mCursor.fetchall()

    for row in rows:
        print(row)