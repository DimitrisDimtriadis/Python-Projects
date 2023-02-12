# CsvTool Version 1.0
import csv
from AppSettings import appsettings
import pandas as pd

def alreadyExist(titleName):
    with open(appsettings.APP_MOVIES_CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
           if row["Title"] == titleName:
            return row
    return None

def getUnsentMoview():
    df = pd.read_csv(appsettings.APP_MOVIES_CSV_PATH)
    return (df.loc[df['Notified'] == 1]).to_dict("records") 

def markAllAsNotified():
    df = pd.read_csv(appsettings.APP_MOVIES_CSV_PATH)
    df['Notified'] = df['Notified'].replace(1,0)
    df.to_csv(appsettings.APP_MOVIES_CSV_PATH, index=False)

def getLastId():
    with open(appsettings.APP_MOVIES_CSV_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)        
        # This for loop exist because in other case the return line number didn't updated
        for row in csv_reader:
           print("")
        return csv_reader.line_num

def insertNewRow(dictRow):    
    with open(appsettings.APP_MOVIES_CSV_PATH, mode='a') as csv_file:
        fieldnames = ['ID', 'Title', 'Grade', 'Notified', 'EntryDate', 'ModifyDate', 'ImageUrl']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'ID': getLastId(), 'Title': dictRow['Title'], 'Grade': dictRow['Grade'], 'Notified': dictRow['Notified'], 'EntryDate': dictRow['EntryDate'], 'ModifyDate': dictRow['ModifyDate'], 'ImageUrl': dictRow['ImageUrl']})

def updateRow(dictWithValues, idOfRow):
    df = pd.read_csv(appsettings.APP_MOVIES_CSV_PATH)
    # +1 For header +1 Because it start from 0 index
    indexToAdd = int(float(idOfRow)) - 1
    
    for mKey in dictWithValues.keys():
        df.loc[indexToAdd, mKey] = dictWithValues[mKey]
    
    df.to_csv(appsettings.APP_MOVIES_CSV_PATH, index=False)