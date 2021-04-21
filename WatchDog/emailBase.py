# EmailSendTool version 1.0
import smtplib
import pandas
import os, re, sys
import watchDogUtilities as ut

rowHeaders = ['Email', 'password', 'SourceMail', 'host']
basePath = 'flatFilesUtil/data.csv'
messagePath = 'flatFilesUtil/message.txt'

# Function to validate email
def isGivenEmailValid(givenEmail):
    return re.match(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$", givenEmail)

def deleteRows(pandasReadFile, rowsToDelete, mFilePath):
    # Function to delete rows base on given list with rows
    # For loop to delete and instant save the changes on file
    pandasReadFile.drop(rowsToDelete.index).to_csv(mFilePath, index=False)

def insertEntry(mEmail, mPass, mSource, mHost, mFilePath):
    # Function to write entry on csv file
    mEntry = pandas.DataFrame([[mEmail, mPass, mSource, mHost]],
                              columns=rowHeaders)
    mEntry.to_csv(mFilePath, mode='a', header=False, index=False)


def checkIfNeedToInitDataFile(mFilePath):
    # Function to avoid script crashing for missing csv file
    # Check if file exists
    if not os.path.isfile(mFilePath):
        with open(mFilePath, 'w'):
            pass
        pandas.DataFrame(columns=rowHeaders).to_csv(
            mFilePath, mode='a', header=True, index=False)


# Function to check if file exist and return the path of txt file with message for sending via email
def checkIfMessageToSendExist(msgFilePath):

    # Check if file exist on current path and it is not empty
    textMessagePath  = ut.findParentPath(msgFilePath)
    if os.path.isfile(textMessagePath) and os.stat(textMessagePath).st_size != 0:
        # print("The path for message.txt is: " + textMessagePath)
        return textMessagePath
    else:
        print("Something went wrong with message.txt")
        return ""

# main function that does all the email things
def main(pathForEmailFile='', pathForMessageFile=''):

    # A triger that affects the functionality of the script
    manualModeOn = (pathForEmailFile == '' or pathForMessageFile == '')
    
    # Set var for base path to check it later
    if not manualModeOn:
        emailsBasePath = pathForEmailFile
    else:
        emailsBasePath = ut.findParentPath(basePath)

    checkIfNeedToInitDataFile(emailsBasePath)

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
    if len(mSourceMail) != 1 and manualModeOn:        
        # If script doesn't find the file create a new one with source Email to init the functionality
        mRes = addNewSourceEmail(emailsBasePath)
        emailSource, passwordSource, host = mRes        
    elif len(mSourceMail) != 1 and not manualModeOn:
        # When manual mode is OFF the it just raise an exception
        raise Exception("There is no csv file that containt source email !")
    else:
        emailSource = mSourceMail["Email"][0]
        passwordSource = mSourceMail["password"][0]
        host = mSourceMail["host"][0]

    # SourceMail = 0 means that this mail is a reciptent
    reciptentTosSendMsgs = df.loc[df['SourceMail'] == 0]
    if len(reciptentTosSendMsgs) == 0 and manualModeOn:
        # If script doesn't find any reciptent script asks to add new ones
        reciptentTosSendMsgs = addNewTargetEmails(emailsBasePath)
    elif len(reciptentTosSendMsgs) == 0 and not manualModeOn:
        # When manual mode is OFF the it just raise an exception
        raise Exception("The csv file with the emails doesn't contain any reciptent email")
    else:
        # Get again the emails to send the message
        reciptentTosSendMsgs = []
        for receiverMail in df.loc[df['SourceMail'] == 0]['Email']:
            reciptentTosSendMsgs.append(receiverMail)

    # Save path of message.txt (if exist) to set the title and the message of email
    if not manualModeOn:
        pathOfMessageFile = pathForMessageFile
    else:
        pathOfMessageFile = checkIfMessageToSendExist(messagePath)

    if pathOfMessageFile != "":

        # Open the file with message
        messageFile = open(pathOfMessageFile)

        for position, line in enumerate(messageFile):
            if position == 0:
                emailSubject = line
            else:
                msgText += line

        # Compination of Title and message of email
        message = 'Subject: {}\n\n{}'.format(emailSubject, msgText)

        # Start procedure of sending email
        try:
            server = smtplib.SMTP_SSL(host, port)        
            # Try to login on email witifh given crentetial3
            try:
                server.login(emailSource, passwordSource)
            except Exception:
                print("\nSomething went wrong with given crendetials !\n")
                deleteRows(df, df.loc[df['SourceMail'] == 0], emailsBasePath)
                if server:
                    server.quit()
                    
        except smtplib.socket.gaierror:
            deleteRows(df, df.loc[df['SourceMail'] == 0], emailsBasePath)
            print("\nSomething went wrong with SMTP_SSL (host or port) !\n")            
        
        # For multiple emails
        try: 
            server.sendmail(emailSource, reciptentTosSendMsgs, message)
            server.quit()
            print("Ok. All email(s) has been send")
        except Exception:
            print("\nScript fail to send the message !\n")
        
    else:
        print("\nIt seems that there is no message.txt file in current path. \nAs result the email script abort the try of sending any message!!\n\n")
        raise Exception("Message file missing !")

# Function that called when user want to add new source email
def addNewSourceEmail(emailFilePath):
    # If mSource contains more than 1 source mail. Then delete all source mails to set a new one
    # deleteRows(df, mSourceMail)

    print("\n\nIt seems that you haven't set an email as source to send emails:\n")

    # Trigger to start the while-loop to get a valid email and password
    isSourceMailInvalid = True

    # var to act like trigger to prevent user re-enter email if its valid
    setValidMail = False

    emailS = None
    passwordS = None
    mHost = None

    while isSourceMailInvalid:
        # Ask for source email and its password
        if not setValidMail:
            emailS = input("Please add a valid email address: ")
            if not isGivenEmailValid(emailS):
                continue
            else:
                # Activate trigger to not re-enter the email
                setValidMail = True

        passwordS = input(
            "You need to add also the password of this email: ")

        # Check length of the password user submit
        if len(passwordS) < 4:

            print("\nThe password was too short. Please try again\n")
            # To avoid ending of loop
            continue

        mHost = input(
            "You need to add also the host of this email: ")

        if mHost == "":
            print("\nYou must add a host to be able to send emails ")
            # To avoid ending without host
            continue

        isSourceMailInvalid = False
        # To insert source email on csv
        insertEntry(emailS, passwordS, 1, mHost, emailFilePath)
    return (emailS, passwordS, mHost)

# Function that called when user want to add new recipient emails
def addNewTargetEmails(emailFilePath):
    reciptentTosSendMsgs = []
        
    print("\n\nIt seems that you haven't set reciptents.\n")

    # Loop to add a or multiple destination emails
    resultOfAddAnotherEmail = "Y"

    while (resultOfAddAnotherEmail.lower() == "y"):

        emailToSend = input("Set email address to send messsages: ")

        # Check if mail is valid
        if isGivenEmailValid(emailToSend):
            # Add it on csv
            insertEntry(emailToSend, 0, 0, "", emailFilePath)
            reciptentTosSendMsgs.append(emailToSend)
            resultOfAddAnotherEmail = input(
                "Do you need to add another one ? (Y/N) : ")
        else:
            print("The given email is invalid. Please try again")
    return reciptentTosSendMsgs


if __name__ == "__main__":
    # The case that user give path for data.csv and message.txt
    if len(sys.argv) == 3:
        # Turn off 'manualMode' and add the paths for email and message file
        emailPath = sys.argv[1]
        messagePath = sys.argv[2]
        ut.checkIfFileExists(emailPath)
        ut.checkIfFileExists(messagePath)
        main(emailPath, messagePath) 
    elif len(sys.argv) == 1:
        main()
    else:
        print("Something went wrong with arguments. You must add first the path for the file with emails (csv file) and then the path for message (txt file)")