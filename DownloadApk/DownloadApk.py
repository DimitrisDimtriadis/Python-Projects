import requests
import json
import os

# Path to save apks files
PATH_FOR_APKS = 'apks'

# Get the app version number from name of .apk
def getVersionNumber(flavorString):
    # Version number to return 
    versionNUmber = ''

    # If name start with number add it on versionNUmber until find something that is not number
    for mChar in flavorString:
        if mChar.isdigit():
            versionNUmber += mChar
        else:
            break
    return versionNUmber

def createAppropiateDir(mPath):
    # If file not exist, it creates it
    if not os.path.exists(mPath):
        os.makedirs(mPath)
    

# Main methon for current file
if __name__ == "__main__":

    print("Start looking for apks to download...")

    # Direct link to download link for apks
    mURL = 'https://circleci.com/api/v1.1/project/github/IQTaxi/android_driver/latest/artifacts'
    payload = {'key': 'val'}
    
    # Add authentication token
    headers = {'Circle-Token': '### ADD AUTH TOKEN HERE ###'}
    
    # Get the result from url
    res = requests.get(mURL, data=payload, headers=headers)

    # List with all elements of result from get request
    list_with_elements = json.loads(res.text)

    #Create list to save apk's url
    apkUrls = []

    # Chek all elements of array
    for mVal in list_with_elements:
        
        # Check if link is for apk
        if mVal['url'].endswith('.apk'):
            # Add url with apk on list to use it later
            apkUrls.append(mVal['url'])

    # Show message with the number of apk found
    print("\n\n * " + str(len(apkUrls)) + " apk" + ("s" if apkUrls.count != 1 else "") + " found !\n\n")

    # If not exist. Create apk folder
    createAppropiateDir(PATH_FOR_APKS)

    trigerForAddApks = {
        "trigerForCreateFolder": False,
        "pathToSave": ""
    }    
    
    # Loop to download all the flavors
    for mUrl in apkUrls:
        
        mUrlSubStr = mUrl.split('/')
        
        print("\nDownloading " + mUrlSubStr[-1] + " ...")
        
        if not trigerForAddApks["trigerForCreateFolder"]:
            createAppropiateDir(PATH_FOR_APKS + '/' + getVersionNumber(mUrlSubStr[-1]))
            trigerForAddApks["trigerForCreateFolder"] = True
            trigerForAddApks["pathToSave"] = PATH_FOR_APKS + '/' + getVersionNumber(mUrlSubStr[-1])
        
        # Download the apk
        downloaded_file = requests.get(mUrl, data=payload, headers=headers)
        
        # Save it with specific name
        open(trigerForAddApks["pathToSave"] + '\\'+ mUrlSubStr[-1], 'wb+').write(downloaded_file.content)
        print("DONE")

    print("Proccess... end")