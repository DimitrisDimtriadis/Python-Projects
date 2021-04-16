#!/usr/bin/env bash

#Name of files used to specify the path to run the commands
nameOfWatchDog="/movieWatchDog.py"
nameOfEmailBase="/emailBase.py"
nameOfCreateMessage="/createMessage.py"
nameOfDirForSourceFiles="/flatFilesUtil"
#The path where script exist
parentFilePath=$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#Function to get the status from last command excecuted
checkStatus(){
	if [ $1 != '0' ] && [ $1 != '33' ] 
	then
		echo "There was a problem with $2 script."
		echo "Please fix it before precedure"
	fi
}
#Function that used to run specific .py files with python3. It return the status of excecution
runSpecificPyFile(){
	#Get the path of bash shell script. We append the input argument to set the right path
	filePath=$parentFilePath$1	
	if [ $# -le 1 ]
	then
		#Execute the script to access site and get the info we want
		python3 $filePath
	else
		#Execute the script to access site and get the info we want
		python3 $filePath $2
	fi
	#Save on var the exit status
	runPyCommandStatus=$?
	#Call the function to check if status was not 0, to notify user
	checkStatus $runPyCommandStatus $1
	return $runPyCommandStatus
}

echo "Procedure started..."

#If flatFilesUtil dir doesn't exit script crash without any info.
if [ ! -d $parentFilePath$nameOfDirForSourceFiles ]
then
	#If dir doesn't exit, create one
	mkdir $parentFilePath$nameOfDirForSourceFiles
fi

#Run movieWatchDog
runSpecificPyFile $nameOfWatchDog
#Get status of previous execution
watchDogStatus=$?

#If the watchDogStatus exit with 0 then execute the bellow code
if [ $watchDogStatus == '0' ]
then
	#Run createMessage
	runSpecificPyFile $nameOfCreateMessage
	#Get status of previous execution
	createMessageStatus=$?

	if [ $createMessageStatus == '0' ]
	then
		#Run emailBase
		runSpecificPyFile $nameOfEmailBase
		#Get status of previous execution
		emailBaseStatus=$?
		
		if [ $emailBaseStatus == '0' ]
		then
			runSpecificPyFile $nameOfCreateMessage "update"
		fi

	elif [ $createMessageStatus == '33' ]
	then
		echo "Procedure ends successfully. There is nothing new to send !"
	else
		echo "Procedure stuck with createMessage script !!!"
	fi
else
	echo "Procedure stuck with watchDog script !!!"
fi