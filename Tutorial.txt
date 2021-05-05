_________________________________
***Info about WatchDog project
_________________________________

!!! To start on this project you need to install all necessary tools like python3, sqlite3, pip etc. To do that you need to go on folder and run the command bellow:
chmod 755 UtilitiesInstall 


@python vs python3
The app works with python3. If you use python and not the python3, you will face issues !

@To add on infinite loop to execute every X mins we use linux's 'crontab -e' more specific we add the 
line bellow: (Before you enter script to crontab make sure that you have set data.csv)
* * * * * /path to file/shellScriptAggregator.sh
* * * * * /path to file/BackupProcess.sh

	
	Python Files
_________________________________

--movieWatchDog.py
This script download the given page and extracts the data we need to store them in database

--CustomeModels.py
Classes with the models we need on scripts

--createMessage.py
This script BASED ON input argument either fetch all the data we want to send through an email, either mark all unread rows as sended to avoid sending any duplication of data. The project on which will make the changes
depend on the arguments user will impliment.
The script works only with this arguments:
	- 'tableName'
    - 'tableName' update
    - 'tableName' 'pathForMessage'
    - 'tableName' 'pathForDb' update
    - 'tableName' 'pathForMessage' 'pathForDb'
    - 'tableName' 'pathForMessage' 'pathForDb' update


	Bash Shell Scripts
_________________________________

--shellScriptAggregator.sh
It the bash script that execute every py script we want on right order. If something go wrong, it notify the user with error message

--storageConfigure.sh
It init the tables we need in db from .sql files in sqlCommands

--UtilitiesInstall.sh
It has been created to run only one time, to init and install any necessary tool that project needs


	Directories
_________________________________

--flatFilesUtil
It contains all the data files project needs to run 	

--DBUtil
All about SQLite3 (files and folders)

--sqlCommads
The folder with all the .sql command (in file). Basically its the 'create table' and stuff like that


	Other files
_________________________________

--data.csv
The csv file that contain the destinations emails and the source email with its credentials. The first line contains the source email and the others is the destination emails

--message.txt 
The message that the emailBase.py will send through an email
	
--watchDogDB.sqlite
The Base of whole project


	emailBase.py
_________________________________

--emailBase.py
The script that takes the message.txt file from flatFilesUtil/ and send the text through an email. It need the data.csv file that contains an email address (with credentials) 
to use it as source and destinations addresses. If data.csv doesn't exist then it ask from user to insert these info. At this point on 'crontab -e' command, already exist this file 
to works automated.

- (no arguments) 
It works with the classic way. 
The program search on 'flatFilesUtil/data.csv' path for the email file and on 'flatFilesUtil/message.txt' path for the message file. 
If the file with source/target emails doesn't exist the program asks from user to enter it.
If the file with the message doesn't exist the app stops working.

-(argument_1='Path for source/target emails csv file' && argument_2='Path for message txt file')
It works same with previous one, but it doesn't asks from user to write anything. If program doesn't find any file, it raise an exception.
Before do anything script check that paths for files are valid. If they don't an exception will raise


	SqliteQueryTools.py
_________________________________

It's a python file that contains all functions needed to manipulate SQLite database.
! The functions help other scripts to manipulate the database !

- (no arguments) 
It works with the current given command. The most times it will excecute a SELECT query on a specific db table.

-(argument_1='Path for .sqlite file you want to interact')
It contains a full remote control to manual manipulate a specific database. Just follow the instructions that app give



	WatchDogUtilities.py
_________________________________

Common function we need in other files. Basically it contains functions for path of files
! The functions help on issues like validate path or file existance. Just support other classes !


	BackupToolSqlite.py
_________________________________

Its a script that create the necessary directories per project/database and create a copy of db whenever you call it.

- (argument_1='Path of .sqlite or .db file you want to backup')
It takes the path and extract the name of file from path. It checks if directories exists (if doesn't exist it create a new one). If directory already exist, it check if it contains more than 50 files in there and 
remove the oldest if exceed that limit. After that it copies the db in that directory with the name "'current Timestamp'_'name of db'"

- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Limit of files each directory can contains')
It takes the path and extract the name of file from path. It checks if directories exists (if doesn't exist it create a new one). If directory already exist, it check if it contains more than 'Given number' files in 
there and remove the oldest if exceed that limit. After that it copies the db in that directory with the name "'current Timestamp'_'name of db'"

	
	BackupProcedure.sh
_________________________________

This script calls the BackupToolSqlite.py and if exit without status 0, then send email to user with simple error message
- (argument_1='Path of .sqlite or .db file you want to backup')
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Limit of files each directory can contains')
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Path for data.csv which contains the source email to send to user')
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Path for data.csv which contains the source email to send to user' && argument_3='Limit of files each directory can contains')
For backup process only.

		
	LogTool.py
_________________________________

The python file that needs to support the custom Logger on any python program. To use it on any other file you just need to import the file on project and just write 
Base on profile and status, code decide to create and append logs.
Inside the code, we have the 'maxSizeOfEachFile' where the value sets the limit on Maximum size of log file (if this var is equal to -1 then there is no limit)
Also, we have the 'pathForFolderWithLoggers' where the value sets a diffrent path (than default) to save the folder with logs
* Log(LogProfile, LogStatus, Text, Dictionary)

-- LogProfile
    
    LogProfile.D = For DEVELOPMENT profile
    LogProfile.P = For PRODUCTION profile
    
-- LogStatus
    
    LogStatus.D = For DEBUG status    
    LogStatus.I = For INFO status
    LogStatus.W = For WARNING status
    LogStatus.E = For ERROR status
    
-- Text: Just a simple text to append on log

-- Dictionary: Dictionary where key is the name of variable and the value is the value of this variable 

ex. Log(LogProfile.P, LogStatus.E, "The variables is :", {"varA":1, "varB":2, "varC":3, "varD":4})
