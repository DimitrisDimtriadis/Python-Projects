import CustomeModels as mModel
import csvBase as CB
import requests
import emailBase
from bs4 import BeautifulSoup as BF
import re

MoviesList = []

def extractImdbGradeFromText(mText):
    mGrade = re.search(r"(?<=imdb:).*?(?=<)", mText, flags=re.I | re.M)
    if mGrade:
        return float(mGrade[0])
    return -1

def createInfoMsgToSend(elementList):

    # Create (If doesn't exist) message.txt or clean it to create a new message
    msgFile = open("message.txt", "w")
    msgFile.write("New movies : \n")
    
    # Reset list to avoid conflicts
    MoviesList = []

    # Loop that add data on message.txt
    for anElementListM in elementList:

        # A attribute that contains name of movie
        nameOfMovie = anElementListM.findAll("a", {"class": "headinglink"})[0]

        # IMG attribute that contains image of movie
        imageOfMovie = anElementListM.findAll("img", {"class": "lozad"})[0].get('data-src')

        # DIV attribute that contains imdb grade (if doesn't show only subs4free grade)
        movieGradeAsHtml = str(anElementListM.findAll("div", {"class": "panel-heading-info"}))
        # To check if grade exist 
        locationOfGrade = movieGradeAsHtml.lower().find("imdb")
        
        gradeOfMovie =  extractImdbGradeFromText(movieGradeAsHtml)
        
        if locationOfGrade != -1 or gradeOfMovie != -1:
            # Get only the grade            
            msgFile.write("* Name: " + nameOfMovie.text + " || " + str(gradeOfMovie) + " \n " + imageOfMovie + "\n\n" )
        else: 
            msgFile.write("* Name: " + nameOfMovie.text + " \n " + imageOfMovie)
       
        mGrade = -99
        try:
            mGrade = float(gradeOfMovie)
        except:
            print("Something went wrong with convert string to float. Grade: "+gradeOfMovie)
        if "Two of Us (Deux) (2019)" == nameOfMovie.text:
            print("asd")
        tempMovie = mModel.Movie(nameOfMovie.text, mGrade, imageOfMovie)
        
        #Append on global list the tempObject
        MoviesList.append(tempMovie)
        CB.main(MoviesList)


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
    print("ok")
   
