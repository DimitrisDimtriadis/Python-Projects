import requests
import json
import os

# Path to save apks files
PATH_FOR_APKS = 'apks'

# Main methon for current file
if __name__ == "__main__":

    # Direct link to download link for apks
    mURL = 'https://circleci.com/api/v1.1/project/github/IQTaxi/android_driver/latest/artifacts'
    payload = {'key': 'val'}
    
    # Add authentication token
    headers = {'Circle-Token': ''}
    
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

    # If file not exist, it creates it
    if not os.path.exists(PATH_FOR_APKS):
        os.makedirs(PATH_FOR_APKS)
    
    # Loop to download all the flavors
    # for mUrl in apkUrls:
    
    mUrlSubStr = apkUrls[0].split('/')
    
    # Download the apk
    downloaded_file = requests.get(apkUrls[0], data=payload, headers=headers)
        
    # Save it with specific name
    open(PATH_FOR_APKS + '\\'+ mUrlSubStr[-1], 'wb+').write(downloaded_file.content)

    print("assssd")
 