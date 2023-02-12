import Utilities as ut
from bs4 import BeautifulSoup as BF
import re, requests, datetime
from AppSettings import appsettings
import LogTool as log
from AppSettings import LogProfiles
from LogTool import LogStatus
import CsvTool as csvT

MoviesList = []

def extractImdbGradeFromText(mText):
    mGrade = re.search(r"(?<=imdb:).*?(?=<)", mText, flags=re.I | re.M)
    if mGrade:
        return float(mGrade[0])
    return -1

def createInfoMsgToSend(elementList):

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
        existedRow = csvT.alreadyExist(nameOfMovieText)
        
        if existedRow == None:
            # If entry doesn't exist insert new row
            movieDict = {'Title':nameOfMovieText, 'Grade':gradeOfMovie, 'Notified':1, 'EntryDate':datetime.datetime.now().timestamp(), 'ModifyDate':'', 'ImageUrl':imageOfMovie}
            csvT.insertNewRow(movieDict)
        else:
            # If entry does exist update the row
            if locationOfGrade != -1 or gradeOfMovie != -1:                
                csvT.updateRow({'Grade': gradeOfMovie, 'ModifyDate': datetime.datetime.now().timestamp(), 'ImageUrl': imageOfMovie}, existedRow['ID'])
            else:
                # If grade is not valid don't add it
                csvT.updateRow({'ModifyDate': datetime.datetime.now().timestamp(), 'ImageUrl': imageOfMovie})                

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