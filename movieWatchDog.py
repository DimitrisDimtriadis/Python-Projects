import os
import requests
from bs4 import BeautifulSoup as BF

def checkGradeValidation(mGrade):
    templocation = mGrade.lower().find("<")
    if templocation != -1:
        return mGrade[:templocation]

    return mGrade


def main():
    # main function

    # Set the url link
    urlMovies = 'https://www.subs4free.info/'

    # Set my-user-aget. If you dont know who is your 'User-aget', just google "my user agent" and it will show it first on result
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

    # Get the whole page content
    pageMovies = requests.get(urlMovies, headers=headers)

    # Convert page to lxml
    soupMovies = BF(pageMovies.content, 'lxml')
    
    # DIV attribute that contains info for every movie
    elementListMovies = soupMovies.findAll("div", {"class": "movies-info"})

    msgFile = open("message.txt", "w+")
    
    for anElementListM in elementListMovies:
        # A attribute that contains name of movie
        nameOfMovie = anElementListM.findAll("a", {"class": "headinglink"})[0]
        # IMG attribute that contains image of movie
        imageOfMovie = anElementListM.findAll("img", {"class": "lozad"})[0].get('data-src')

        movieGradeAsHtml = str(anElementListM.findAll("div", {"class": "panel-heading-info"}))
        locationOfGrade = movieGradeAsHtml.lower().find("imdb")
        gradeOfMovie =  movieGradeAsHtml[locationOfGrade : locationOfGrade+9]
        
        if locationOfGrade != -1:
            print("Name: " + nameOfMovie.text + " || " + checkGradeValidation(gradeOfMovie) + " || " + imageOfMovie)
        else: 
            print("Name: " + nameOfMovie.text + " || " + imageOfMovie)

    print("yeah")


if __name__ == "__main__":
    main()
    print("ok")
   
