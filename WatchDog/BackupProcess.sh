#!/bin/bash

#Get the parent path
parentFilePath=$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo 'Start Back up procedure...'
#Back up script
python BackupToolSqlite.py "$1" $2 &> output.txt

#Exit status code from excecution of BackupToolSqlite.py
backUpStatusCode=$?

#Path of file that contains the output of back up procedure
pathOfOutput=$parentFilePath"/output.txt"

#Check if previouse script with error
if [ $backUpStatusCode != '0' ]
then
    echo "Back up procedure for $1 Failed !"
    echo "Senting email to notify user "
    # Append on first line the title for email
    sed -i '1,2s/^/Error on Back up procedure on raspberry\n /' output.txt
    #Call script to send the error via email on user
    python emailBase.py "D:\sTree\Python Tool\WatchDog\flatFilesUtil\data.csv" "$pathOfOutput"
fi

#Remove the output.txt file because there is no use for it
rm "$pathOfOutput"
echo "Procedure finished"
