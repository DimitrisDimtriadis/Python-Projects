<h2><b>Info about WatchDog project.</b></h2>

_________________________________
<h3><b>Initialize</h3></b>

!!! To start on this project you need to install all necessary tools like python3, sqlite3, pip etc. To do that you need to go on folder and run the command bellow:
chmod 755 UtilitiesInstall 

@python vs python3
The app works with python3. If you use python and not the python3, you ;oxiwill face issues !

@To add on infinite loop to execute every X mins we use linux's 'crontab -e' more specific we add the 
line bellow: (Before you enter script to crontab make sure that you have set data.csv)
\* \* \* \* \* /path to file/shellScriptAggregator.sh
\* \* \* \* \* /path to file/BackupProcess.sh

_________________________________
<h3><b>Bash Shell Scripts</h3></b>

<h4><i> * UtilitiesInstall.sh</h4></i>
It has been created to run only one time, to init and install any necessary tool that project needs
<br><br><br>

_________________________________
<h3><b>Directories</h3></b>

<h4><i> * rawFiles</h4></i>
It contains message.txt (that is the contain of the email to send). The file data.csv that containts the email receipts and all the Logs of process
<br><br><br>


<h4><i> * DBUtil</h4></i>
All about SQLite3 (files and folders)
<br><br><br>


<h4><i> * Modules</h4></i>
All the .py and .sh files that user don't need to see on main path (to avoid any distraction)
<br><br><br>

_________________________________
<h3><b>Other files</h3></b>

<h4><i> * data.csv</h4></i>
The csv file that contain the destinations emails. The first line contains the source email and the others is the destination emails
<br><br><br>


<h4><i> * message.txt</h4></i>
The message that the emailBase.py will send through an email
<br><br><br>


<h4><i> * watchDogDB.sqlite</h4></i>
The Base of whole project
<br><br><br>

_________________________________
<h3><b>Python Files</h3></b>

<h4><i> * MoviesWatchDog.py</h4></i> 
This script download the given (from AppSettings) site and extracts the data we need to store them in database
<br><br><br>


<h4><i> * Models.py</h4></i> 
Contain all the Classes that are the models to create objects whenever we need them to manipulate data easier
<br><br><br>


<h4><i> * createMessage.py</h4></i>
This script BASED ON input argument either fetch all the data we want to send through an email, either mark all unread rows as sended to avoid sending any duplication of data. The project on which will make the changes
depend on the arguments user will impliment.
The script works only with this arguments:
	- 'tableName'
    - 'tableName' update
    - 'tableName' 'pathForMessage'
    - 'tableName' 'pathForDb' update
    - 'tableName' 'pathForMessage' 'pathForDb'
    - 'tableName' 'pathForMessage' 'pathForDb' update
<br><br><br>


<h4><i> * EmailTool.py</h4></i> 
The main function for this tool is to sent emails with custom message. This script need path for data.csv (which contains all the recipients) from Appsettings to get the destinations of the email. Also we need the path of message.txt (which contain the content of the email) from AppSettings and containts all the information want to sent to user

- (no arguments) 
The program search on path we set on appSettings for data.csv and for message.txt path. 
If the file with receiptents emails doesn't exist app stops.
If the file with the message doesn't exist the app stops working.
<br><br><br>


<h4><i> * ManualDB.py</h4></i>
This script help us to manipulate the given DB (as parameter)!

\*(argument_1='Path for .sqlite file you want to interact')
It contains a full remote control to manual manipulate a specific database. Just follow the instructions that app give
<br><br><br>


<h4><i> * SQLiteTools.py</h4></i>
It's a python file that contains all functions needed to manipulate/create SQLite database.
<br><br><br>


<h4><i> * Utilities.py</h4></i>
Common function we need in other files. Basically it contains functions for path of files
! The functions help on issues like validate path or file existance. Just support other classes !
<br><br><br>


<h4><i> * BackupToolSqlite.py</h4></i>
NEED REWORK !!!
Its a script that create the necessary directories per project/database and create a copy of db whenever you call it.

- (argument_1='Path of .sqlite or .db file you want to backup')
It takes the path and extract the name of file from path. It checks if directories exists (if doesn't exist it create a new one). If directory already exist, it check if it contains more than 50 files in there and 
remove the oldest if exceed that limit. After that it copies the db in that directory with the name "'current Timestamp'_'name of db'"
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Limit of files each directory can contains')
It takes the path and extract the name of file from path. It checks if directories exists (if doesn't exist it create a new one). If directory already exist, it check if it contains more than 'Given number' files in 
there and remove the oldest if exceed that limit. After that it copies the db in that directory with the name "'current Timestamp'_'name of db'"
<br><br><br>


<h4><i> * BackupProcedure.sh</h4></i>
This script calls the BackupToolSqlite.py and if exit without status 0, then send email to user with simple error message

- (argument_1='Path of .sqlite or .db file you want to backup')
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Limit of files each directory can contains')
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Path for data.csv which contains the source email to send to user')
- (argument_1='Path of .sqlite or .db file you want to backup' && argument_2='Path for data.csv which contains the source email to send to user' && argument_3='Limit of files each directory can contains')
For backup process only.
<br><br><br>


<h4><i> * LogTool.py</h4></i> 
The python file that needs to support the custom Logger on any python program. To use it on any other file you just need to import the file on project and just write 
Base on profile and status, code decide to create and append logs.
Inside the AppSettings.py, we have the 'LOGGER_FILE_MAX_SIZE' where the value sets the limit on Maximum size of log file (if this var is equal to -1 then there is no limit)
Also, we have the 'LOGGER_FILES_PATH' where the value sets a diffrent path (than default) to save the folder with logs

* Logger(LogProfile, LogStatus, Text, Dictionary)

- LogProfile
    LogProfile.D = For DEVELOPMENT profile
    LogProfile.P = For PRODUCTION profile
    
- LogStatus
    LogStatus.D = For DEBUG status    
    LogStatus.I = For INFO status
    LogStatus.W = For WARNING status
    LogStatus.E = For ERROR status
    LogStatus.L = For LOADING status (We use it to support a increasing loading number)
    
- Text: Just a simple text to append on log

- Dictionary: Dictionary where key is the name of variable and the value is the value of this variable 

ex. Logger(LogProfile.P, LogStatus.E, "The variables is :", {"varA":1, "varB":2, "varC":3, "varD":4})