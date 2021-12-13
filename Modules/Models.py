class Movie:
    
    def __init__(self, id, title, grade, imgURL, notified, entryDate, modifyDate):
        self.id = id
        self.title = title
        self.imgURL = imgURL
        self.notified = notified
        self.entryDate = entryDate
        self.modifyDate = modifyDate
        if grade < 0 or grade > 10:
            self.grade = -1
        else:
            self.grade = grade