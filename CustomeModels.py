class Movie:
    
    sent = False    

    def __init__(self, title, grade, imgURL):
        self.title = title
        if grade < 0 or grade > 10:
            self.grade = -1
        else:
            self.grade = grade
        self.imgURL = imgURL