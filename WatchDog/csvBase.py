import csv
import CustomeModels
from os import path

moviedb = 'moviesDB.csv'
# Function that create base if not exist
def createFile():
    # Create .csv file to save movies if not exist
    if not path.exists(moviedb):
        with open(moviedb, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting = csv.QUOTE_MINIMAL) 
            filewriter.writerow(['Title','Grade', 'Sent', 'ImageUrl'])

# Function that insert all values
def insertNewValues(moviesList):
    for mMovie in moviesList:
       
        isSaved = False
        with open(moviedb) as f:
            reader = csv.DictReader(f,delimiter=',')
            #Check if movie is already saved
            for row in reader:                
                if mMovie.title == row['Title']:
                    isSaved=True
                    break
        
        # If it isn't. Add new entry
        if not isSaved:
            with open(moviedb, 'a', newline='') as f:
                filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting = csv.QUOTE_MINIMAL)
                filewriter.writerow([mMovie.title, mMovie.grade, mMovie.sent, mMovie.imgURL])
                        
def main(movieList):
    createFile()
    insertNewValues(movieList)

if __name__ == "__main__":
    createFile()
    print("ok")