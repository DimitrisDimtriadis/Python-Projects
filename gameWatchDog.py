import os
import requests
from bs4 import BeautifulSoup as BF

if __name__ == "__main__":
    # main function

    # Set the url link
    urlGames = 'https://game20.gr/category/news/'
    urlMovies = 'https://www.subs4free.info/'
    urlBeta = 'https://www.allgamesdelta.net/'

    # Set my-user-aget. If you dont know who is your 'User-aget', just google "my user agent" and it will show it first on result
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

    # Get the whole page content        
    pageGames = requests.get(urlGames, headers=headers)
    pageMovies = requests.get(urlMovies, headers=headers)
    pageBeta = requests.get(urlBeta, headers=headers)
    
    soupGames = BF(pageGames.content, 'lxml')
    soupMovies = BF(pageMovies.content, 'lxml')
    soupBeta = BF(pageBeta.content, 'lxml')
    sel = " body > div.wrapper > div.container > section > div.container-section > div.list-info > div.movies-info > div.movie-cont-right > div.panel-heading-info > a"    
    # elementListMovies = soupMovies.select('a.headinglink')
    elementListMovies = soupMovies.findAll("div", {"class" : "movie-info"})
    elementListGames = soupGames.findAll('article')
    elementListBeta = soupBeta.findAll("div", {"class" : "post hentry"})    