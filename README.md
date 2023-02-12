<h2><b>Info about WatchDog project.</b></h2>

_________________________________
<h3><b>Initialize</h3></b>

!!! To start on this project you need to install all necessary tools like python3, pip etc. To do that you need to go on folder and run the command bellow:
chmod 755 InstallLibs.sh
In case that you have everything installed and you only want the pip libs just use the /Install/requirements.txt with 'pip install -r requirements.txt'

@python vs python3
The app works with python3. If you use python and notthe python3, you will face issues !

@To add on infinite loop to execute every X mins we use linux's 'crontab -e' more specific we add the 
line bellow: (Before you enter script to crontab make sure that you have set rawFiles/emailConfig.csv)
\* \* \* \* \* python3 /path to file/Aggregator.py


@Before you run the process you have to update emailConfig.csv file, change the AppSettings.py paramaters and settings and to verify that every file in 'rawFiles' exists
_________________________________
<h3><b>Bash Shell Scripts</h3></b>

<h4><i> * InstallLibs.sh</h4></i>
It has been created to run only one time, to init and install any necessary tool that project needs
<br><br><br>

_________________________________
<h3><b>Directories</h3></b>

<h4><i> * rawFiles</h4></i>
It contains: 
The file <b>message.txt</b> that is the one that contains the email addresses to send the message. 
The file <b>emailConfig.csv</b> that containts the email receipts and all the Logs of process.
The file <b>movies.csv</b> that containts all the data about the movies that required to create a message when we have new data.
<br><br><br>

<h4><i> * Modules</h4></i>
All the .py files that user don't need to see on main path (to avoid any distraction)
<br><br><br>

_________________________________
<h3><b>Python files</h3></b>

<h4><i> * message.txt</h4></i>
The message that the emailBase.py will send through an email
<br><br><br>

<h4><i> * watchDogDB.sqlite</h4></i>
The Base of whole project
<br><br><br>

_________________________________
<h3><b>Python Files</h3></b>

<h4><i> * AppSetting.py</h4></i> 
This files contains all the settings and parameters needs to run the process
<br><br><br>

<h4><i> * MoviesWatchDog.py</h4></i> 
This script download the given (from AppSettings) site and extracts the data we need to store them in csv file
<br><br><br>

<h4><i> * CsvTool.py</h4></i> 
This file contains all the function needs to interact with the file where we save all the downloaded data
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

<h4><i> * Utilities.py</h4></i>
Common function we need in other files. Basically it contains functions for path of files
! The functions help on issues like validate path or file existance. Just support other classes !
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
