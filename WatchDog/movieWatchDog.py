import watchDogUtilities as ut
import SqliteQueryTools as sqlT
from bs4 import BeautifulSoup as BF
import re, requests, datetime

messageFile = "flatFilesUtil/message.txt"
dbFile = "DBUtil/watchDogDB.sqlite"

MoviesList = []

def extractImdbGradeFromText(mText):
    mGrade = re.search(r"(?<=imdb:).*?(?=<)", mText, flags=re.I | re.M)
    if mGrade:
        return float(mGrade[0])
    return -1

def createInfoMsgToSend(elementList):

    # Set the right path for the application file 
    messageFilePath = ut.findParentPath(messageFile) 

    # Create (If doesn't exist) message.txt or clean it to create a new message
    msgFile = open(messageFilePath, "w")
    msgFile.write("New movies : \n")

    # Open connection with SQLite DB to interact with it
    dbConnection = sqlT.dbOpenConnection(ut.checkOSSystem(ut.findParentPath(dbFile)))

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
        mRes = sqlT.dbSELECT(dbConnection, 'MoviesTb', whereStatementText= "Title = '"+nameOfMovieText + "'")       
        
        if not mRes:
            if locationOfGrade != -1 or gradeOfMovie != -1:
                sqlT.dbINSERT(dbConnection, "MoviesTb", ['Title', 'Grade', 'Notified', 'ImageUrl', 'EntryDate'], [nameOfMovieText, gradeOfMovie, 0, imageOfMovie, datetime.datetime.now().timestamp()])
            else:
                sqlT.dbINSERT(dbConnection, "MoviesTb", ['Title', 'Notified', 'ImageUrl', 'EntryDate'], [nameOfMovieText, 0, imageOfMovie, datetime.datetime.now().timestamp()])
        
        elif len(mRes)==1:
            print("asd")asd
            
            
        
    sqlT.dbCloseConnection(dbConnection)
        
        # if locationOfGrade != -1 or gradeOfMovie != -1:
        #     # Get only the grade            
        #     msgFile.write("* Name: " + nameOfMovie.text + " || " + str(gradeOfMovie) + " \n " + imageOfMovie + "\n\n" )
        # else: 
        #     msgFile.write("* Name: " + nameOfMovie.text + " \n " + imageOfMovie)
       
        # mGrade = -99
        # try:
        #     mGrade = float(gradeOfMovie)
        # except:
        #     print("Something went wrong with convert string to float. Grade: "+gradeOfMovie)

        # tempMovie = mModel.Movie(nameOfMovie.text, mGrade, imageOfMovie)
        
        # #Append on global list the tempObject
        # MoviesList.append(tempMovie)        

def main():
    # main function

    # Set the url link
    urlMovies = 'https://www.subs4free.club/'

    # Set my-user-aget. If you dont know who is your 'User-aget', just google "my user agent" and it will show it first on result
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

    # Get the whole page content
    pageMovies = requests.get(urlMovies, headers=headers)

    # Convert page to lxml
    soupMovies = BF(pageMovies.content, 'html.parser')
    
    # DIV attribute that contains info for every movie
    elementListMovies = soupMovies.findAll("div", {"class": "movies-info"})

    createInfoMsgToSend(elementListMovies)

    # emailBase.main()

if __name__ == "__main__":
    main()
    print("Ok. All info have been downloaded")
   
