import Utilities as ut
import SQLiteTool as sqlT
from bs4 import BeautifulSoup as BF
import re, requests, datetime
from AppSettings import appsettings
import LogTool as log
from AppSettings import LogProfiles
from LogTool import LogStatus

MoviesList = []

def extractImdbGradeFromText(mText):
    mGrade = re.search(r"(?<=imdb:).*?(?=<)", mText, flags=re.I | re.M)
    if mGrade:
        return float(mGrade[0])
    return -1

def createInfoMsgToSend(elementList):

    # Open connection with SQLite DB to interact with it
    dbConnection = sqlT.dbOpenConnection(ut.checkOSSystem(appsettings.DB_FILE_PATH))

    if dbConnection == None:
        sqlT.dbCreateDatabase()

    # Make sure that table exist
    initTable(dbConnection)

    # Loop that add data on message.txt
    for anElementListM in elementList:

        # A attribute that contains name of movie
        nameOfMovie = anElementListM.findAll("a", {"class": "headinglink"})[0]        
        nameOfMovieText = re.sub(r'(?<!\\)\'', "\'\'", nameOfMovie.text)
        
        # IMG attribute that contains image of movie
        imageOfMovie = anElementListM.findAll("img", {"class": "lozad"})[0].get('data-src')

        # DIV attribute that contains imdb grade (if doesn't show only subs4free grade)
        movieGradeAsHtml = str(anElementListM.findAll("div", {"class": "panel-heading-info"}))
        
        # To check if grade exist 
        locationOfGrade = movieGradeAsHtml.lower().find("imdb")        
        gradeOfMovie =  extractImdbGradeFromText(movieGradeAsHtml)
        
        # Search in base if movie alreay exist and return it
        mRes = sqlT.dbSELECT(dbConnection, appsettings.APP_MOVIES_TABLE, whereStatementText= "Title = '"+nameOfMovieText + "'")       
        
        if not mRes:
            # If entry doesn't exist insert new row
            sqlT.dbINSERT(dbConnection, appsettings.APP_MOVIES_TABLE, ['Title', 'Grade', 'Notified', 'ImageUrl', 'EntryDate'], [nameOfMovieText, gradeOfMovie, 1, imageOfMovie, datetime.datetime.now().timestamp()])       
        elif len(mRes)==1:
            # If entry does exist update the row
            if locationOfGrade != -1 or gradeOfMovie != -1:
                sqlT.dbUPDATE(dbConnection, appsettings.APP_MOVIES_TABLE, ['Grade', 'ImageUrl', 'ModifyDate'], [gradeOfMovie, imageOfMovie, datetime.datetime.now().timestamp()], "ID = " + str(mRes[0]['ID']))
            else:
                # If grade is not valid don't add it
                sqlT.dbUPDATE(dbConnection, appsettings.APP_MOVIES_TABLE, ['ImageUrl', 'ModifyDate'], [imageOfMovie, datetime.datetime.now().timestamp()], "ID = " + str(mRes[0]['ID']))
        
    sqlT.dbCloseConnection(dbConnection)

# Function that check if db containts table for Movies. If it hasn't then it create a new one
def initTable(dbConnection):
    tablesOfDB = sqlT.dbGetTableOfDB(dbConnection)
    # If table exist continue with main procedure
    if appsettings.APP_MOVIES_TABLE in tablesOfDB:
        return
    # Create a string that contaitns the SQL command to create a new table
    sqlToCreateTable = '''CREATE TABLE IF NOT EXISTS ''' + appsettings.APP_MOVIES_TABLE + '''(
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	Title TEXT NOT NULL,
	Grade REAL,
	Notified INTEGER NOT NULL,
	EntryDate INTEGER,
	ModifyDate INTEGER,
	ImageUrl TEXT
);'''
    # Execute command to create the
    sqlT.dbCustomQuery(dbConnection, sqlToCreateTable)

# main function
def main():
    # Set my-user-aget. If you dont know who is your 'User-aget', just google "my user agent" and it will show it first on result
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

    # Get the whole page content
    pageMovies = requests.get(appsettings.APP_MOVIES_URL, headers=headers)

    # Convert page to lxml
    soupMovies = BF(pageMovies.content, 'html.parser')
    
    # DIV attribute that contains info for every movie
    elementListMovies = soupMovies.findAll("div", {"class": "movies-info"})

    createInfoMsgToSend(elementListMovies)

if __name__ == "__main__":
    main()
    log.Logger(LogProfiles.D, LogStatus.I, "Ok. All info have been downloaded")
    print("Ok. All info have been downloaded")