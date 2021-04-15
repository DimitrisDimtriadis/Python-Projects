#!/usr/bin/env bash

checkStatus(){
	if [ $1 != '0' ]
	then
		echo "There was a problem with movieWatchDog.py script."
		echo "Please fix it before precedure"
	fi
}

echo "Procedure started..."

#Execute the script to access site and get the info we want
python3 /home/pi/FTP/Transfered_Files/movieWatchDog.py;
#Save on var the exit status
movieWatchDogStatus=$?
#Call the function to check if status was not 0, to notify user
checkStatus $movieWatchDogStatus

#If the movieWatchDogStatu exit with 0 then execute the bellow code
if [ $movieWatchDogStatus == '0' ]
then
	#Execute the script to send the email with info
	python3 /home/pi/FTP/Transfered_Files/emailBase.py
	#Save on var the exit status
	emailScriptStatus=$?
	#Check if we had issues to notify user
	checkStatus $emailScriptStatus
fi
