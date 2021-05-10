#!/usr/bin/env bash
#The path where script exist
parentFilePath=$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#Name of files used to specify the path to run the commands
nameOfWatchDog=$parentFilePath"/movieWatchDog.py"
nameOfEmailBase=$parentFilePath"/emailBase.py"
nameOfCreateMessage=$parentFilePath"/createMessage.py"
nameOfDirForSourceFiles=$parentFilePath"/flatFilesUtil"

#Movies WathcDog
pathForSourceFilesMV=$parentFilePath"/flatFilesUtil/MoviesProject"
pathForMessageMv=$parentFilePath"/flatFilesUtil/MoviesProject/message.txt"
pathForEmailAddrMv=$parentFilePath"/flatFilesUtil/MoviesProject/emailAddresses.csv"
pathForDBMv=$parentFilePath"/DBUtil/watchDogDB.sqlite"

#Function to get the status from last command excecuted
checkStatus(){
	if [ $1 != '0' ] && [ $1 != '33' ] 
	then
		echo "There was a problem with $2 script."
		echo "Please fix it before proceed"
	fi
}
#Function that used to run specific .py files with python3. It return the status of excecution
runSpecificPyFile(){
	#Get the path of bash shell script. We append the input argument to set the right path
	
	numberOfArg=$#
	mainProgram="python3"
	for mNum in $(seq 1 $numberOfArg)
	do
		mainProgram="${mainProgram} \$$mNum"
	done
	eval $mainProgram
	
	#Save on var the exit status
	runPyCommandStatus=$?
	#Call the function to check if status was not 0, to notify user
	checkStatus $runPyCommandStatus $1
	return $runPyCommandStatus
}

#If given dir doesn't exit script crash without any info. So this function will create the path/dir we need
checkAndCreateDirIfNeed(){
	if [ ! -d $1 ]
	then
		#If dir doesn't exit, create one
		mkdir $1
	fi
}

echo "Procedure started..."

#Check the necessary paths
checkAndCreateDirIfNeed $nameOfDirForSourceFiles
checkAndCreateDirIfNeed $pathForSourceFilesMV


#Run movieWatchDog
runSpecificPyFile $nameOfWatchDog
#Get status of previous execution
watchDogStatus=$?

#If the watchDogStatus exit with 0 then execute the bellow code
if [ $watchDogStatus = 0 ]
then
	#Run createMessage
	runSpecificPyFile $nameOfCreateMessage MoviesTb $pathForMessageMv
	#Get status of previous execution
	createMessageStatus=$?

	if [ $createMessageStatus = 0 ]
	then
		#Run emailBase
		runSpecificPyFile $nameOfEmailBase $pathForEmailAddrMv $pathForMessageMv
		#Get status of previous execution
		emailBaseStatus=$?
		
		if [ $emailBaseStatus = 0 ]
		then
			runSpecificPyFile $nameOfCreateMessage MoviesTb $pathForDBMv update
		fi

	elif [ $createMessageStatus = 33 ]
	then
		echo "Procedure ends successfully. There is nothing new to send !"
	else
		echo "Procedure stuck with createMessage script !!!"
	fi
else
	echo "Procedure stuck with watchDog script !!!"
fi
