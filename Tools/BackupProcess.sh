#!/bin/bash

#Get the parent path
parentFilePath=$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
#Number of arguments
numberOfArgs=$#
#Path of file that contains the output of back up procedure
pathOfOutput=$parentFilePath"/output.txt"

echo 'Start Back up procedure...'

#Check if arguments is not valid
if [ $numberOfArgs -le 0 ] || [ $numberOfArgs -gt 3 ]
then
    echo "Something went wrong with arguments."
    echo "Please visit Tutorial.txt for more information"
    #If arguments not valid stop script
    exit
fi

emailAvailable=true

if [ $numberOfArgs -eq 1 ]
then
    #Back up script
    python3 "$parentFilePath/BackupToolSqlite.py" "$1" &> "$parentFilePath/output.txt"
    #Exit status code from excecution of BackupToolSqlite.py
    backUpStatusCode=$?
    #Set it false to be sure that script to send email will not be execute
    emailAvailable=false

elif [ $numberOfArgs -eq 2 ]
then
    if [ -f "$2" ]
    then
        python3 "$parentFilePath/BackupToolSqlite.py" "$1" &> "$parentFilePath/output.txt"
        backUpStatusCode=$?
    else
        python3 "$parentFilePath/BackupToolSqlite.py" "$1" $2 &> "$parentFilePath/output.txt"
        #Set it false to be sure that script to send email will not be execute
        emailAvailable=false
    fi    
else
    python3 "$parentFilePath/BackupToolSqlite.py" "$1" $3 &> "$parentFilePath/output.txt"
    backUpStatusCode=$?
fi

#Check if previouse script with error
if $emailAvailable && [ $backUpStatusCode != '0' ] 
then
    echo "Back up procedure for $1 Failed !"
    echo "Senting email to notify user "
    # Append on first line the title for email
    sed -i '1,2s/^/Error on Back up procedure on raspberry\n /' "$parentFilePath/output.txt"
    #Call script to send the error via email on user
    python3 "$parentFilePath/EmailSendTool.py" "$2" "$pathOfOutput"
fi

#Remove the output.txt file because there is no use for it
rm "$pathOfOutput"
echo "Procedure finished"