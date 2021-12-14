# EmailSendTool version 1.2
import smtplib
import pandas
import os, re
import AppSettings as aps
import Utilities as ut
import LogTool as log
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

rowHeaders = ['Email', 'password', 'SourceMail', 'host']

# Function to validate email
def isGivenEmailValid(givenEmail):
    return re.match(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", givenEmail)

# Function that create the folders to place the file (if doesn't exist)
def createFolders(mFilePath):    
    # if we didn't found path create it
    Path(ut.extractPath(mFilePath)).mkdir(parents=True, exist_ok=True)        

def createFileForEmails(mFilePath):    
    # Function to avoid script crashing for missing csv file
    # Check if file exists
    if not os.path.isfile(mFilePath):
        createFolders(mFilePath)
        pandas.DataFrame(columns=rowHeaders).to_csv(
            mFilePath, mode='a', header=True, index=False)

def createMessageFile(mFilePath):
    # Check if file exist    
    if not os.path.isfile(mFilePath):
        # Create the folders (if it needs)
        createFolders(mFilePath)
        # Just create the file
        os.mknod(mFilePath)

# Function to check if file exist and return the path of txt file with message for sending via email
def checkIfMessageToSendExist(msgFilePath):
    # Check if file exist on current path and it is not empty
    textMessagePath  = msgFilePath
    if os.path.isfile(textMessagePath):
        if os.stat(textMessagePath).st_size != 0:
            # Return the path
            return textMessagePath
        return ""
    else:
        log.Logger(log.LogProfile.P, log.LogStatus.E, "File message.txt not exist")
        print("File message.txt not exist")
        return "-1"

# main function that does all the email things
def main():
    # Create an instance of appsettings
    appsettings = aps.appsettings()
    
    # Set var for base path to check it later
    emailsBasePath = ut.checkOSSystem(appsettings.EMAIL_FILE_PATH)
    # Function to check if file exist
    createFileForEmails(emailsBasePath)
    # Read csv file
    df = pandas.read_csv(emailsBasePath)

    # Global values
    # Address of the source email
    emailSource = ""
    # Password of the source email
    passwordSource = ""
    # Email host of source email
    host = ""
    # Title of message to send on email
    emailSubject = ""
    # Message to send on email
    msgText = ""
    # Set port and email source and email host # For SSL
    port = 465

    # Check if source mail has beeen set
    # SourceMail = 1 mean that its not for sending but as source
    mSourceMail = df.loc[df['SourceMail'] == 1]    
    if len(mSourceMail) == 0:
        # When manual mode is OFF the it just raise an exception
        raise Exception("There is no csv file that containt source email !")
    else:
        emailSource = mSourceMail["Email"][0]
        passwordSource = mSourceMail["password"][0]
        host = mSourceMail["host"][0]

    # SourceMail = 0 means that this mail is a reciptent
    reciptentTosSendMsgs = df.loc[df['SourceMail'] == 0]
    if len(reciptentTosSendMsgs) == 0:
        # When manual mode is OFF the it just raise an exception
        raise Exception("The csv file with the emails doesn't contain any reciptent email")
    else:
        # Get again the emails to send the message
        reciptentTosSendMsgs = []
        for receiverMail in df.loc[df['SourceMail'] == 0]['Email']:
            reciptentTosSendMsgs.append(receiverMail)

    # Save path of message.txt (if exist) to set the title and the message of email
    pathOfMessageFile = checkIfMessageToSendExist(ut.checkOSSystem(appsettings.EMAIL_MESSAGE_PATH))

    if pathOfMessageFile != "" and pathOfMessageFile != "-1":

        # Open the file with message
        messageFile = open(pathOfMessageFile)

        for position, line in enumerate(messageFile):
            if position == 0:
                emailSubject = line
            else:
                msgText += line

        # Compination of Title and message of email
        message = MIMEMultipart("alternative")
        message["Subject"] = emailSubject

        htmlTxt = MIMEText(msgText, "html")
        message.attach(htmlTxt)
        # Start procedure of sending email
        try:
            server = smtplib.SMTP_SSL(host, port)        
            # Try to login on email witifh given crentetial3
            try:
                server.login(emailSource, passwordSource)
            except Exception:
                log.Logger(log.LogProfile.P, log.LogStatus.E, "Something went wrong with given crendetials !")
                print("\nSomething went wrong with given crendetials !\n")
                if server:
                    server.quit()
                    
        except smtplib.socket.gaierror:            
            log.Logger(log.LogProfile.P, log.LogStatus.E, "Something went wrong with SMTP_SSL (host or port) !")
            print("\nSomething went wrong with SMTP_SSL (host or port) !\n")            
        
        # For multiple emails
        try: 
            server.sendmail(emailSource, reciptentTosSendMsgs, message.as_string())
            server.quit()
            log.Logger(log.LogProfile.D, log.LogStatus.I, "Ok. All email(s) has been send")
            print("Ok. All email(s) has been send")
        except Exception:
            errorFailToSendMessage = "Script fail to send the message !"
            log.Logger(log.LogProfile.P, log.LogStatus.E, errorFailToSendMessage)
            print("\n" + errorFailToSendMessage + "\n")
        
    elif pathOfMessageFile == "-1":
        errorNoMessageFile = "It seems that there is no message.txt file in current path. \nAs result the email script abort the try of sending any message!!"
        log.Logger(log.LogProfile.P, log.LogStatus.E, errorNoMessageFile)
        print("\n" + errorNoMessageFile + "\n\n")
        # If procudes stopped because of missing message file. Just create it
        createMessageFile(ut.checkOSSystem(appsettings.EMAIL_MESSAGE_PATH))
        raise Exception("Message file missing !")

    else:
        messageForLogger = "The message you try to send is empty !"
        log.Logger(log.LogProfile.D, log.LogStatus.I, messageForLogger)
        print("\n" + messageForLogger + "\n\n")        
        

# main procedure of script
if __name__ == "__main__":
    main()