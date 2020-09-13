import os
import requests
import movieWatchDog as WD
from bs4 import BeautifulSoup as BF

if __name__ == "__main__":
    # main function

    # Set the url link
    URL = 'https://game20.gr/category/news/'

    # Set my-user-aget. If you dont know who is your 'User-aget', just google "my user agent" and it will show it first on result
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

    # Get the whole page content        
    page = requests.get(URL, headers=headers)
    

    soup = BF(page.content, 'lxml')
    sel = " body > div.wrapper > div.container > section > div.container-section > div.list-info > div.movies-info > div.movie-cont-right > div.panel-heading-info > a"    
    xx = soup.select('a.headinglink')
    
    print(xx)
    WD.main()