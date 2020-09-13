import ssl
import csv
import smtplib
import pandas
import os

filepath = 'data.csv'
rowHeaders = ['Email', 'password', 'SourceMail', 'host']
currentPath = os.path.dirname(__file__)
parrentOfCurrentPath = os.path.dirname(currentPath)
dirNameWithWatchdogs = "Site_Watchdog"


def isGivenEmailValid(givenEmail):
    # Function to validate email
    partsOfSourceMail = givenEmail.split('@')

    # Check the first substring of email address
    if len(partsOfSourceMail) >= 2 and len(partsOfSourceMail) <= 3 and partsOfSourceMail[1].count(".") == 1 and len(partsOfSourceMail[0]) > 0:

        hostOfSourceMail = partsOfSourceMail[1].split(".")

        # Check the second substring of email address
        if len(hostOfSourceMail) == 2 and len(hostOfSourceMail[0]) > 0 and len(hostOfSourceMail[1]) > 0:
            print("\n\nEmail address, set !\n")
            return True

    print("\nYou try to set an invalid email address. Please try again\n")
    return False


def deleteRows(pandasReadFile, rowsToDelete):
    # Function to delete rows base on given list with rows
    # For loop to delete and instant save the changes on file
    pandasReadFile.drop(rowsToDelete.index).to_csv(filepath, index=False)


def insertEntry(mEmail, mPass, mSource, mHost):
    # Function to write entry on csv file
    mEntry = pandas.DataFrame([[mEmail, mPass, mSource, mHost]],
                              columns=rowHeaders)
    mEntry.to_csv(filepath, mode='a', header=False, index=False)


def checkIfNeedToInitDataFile():
    # Function to avoid script crashing for missing csv file
    # Check if file exists
    if not os.path.isfile("./"+filepath):
        with open('./'+filepath, 'w'):
            pass
        pandas.DataFrame(columns=rowHeaders).to_csv(
            filepath, mode='a', header=True, index=False)


def checkIfMessageToSendExist():
    # Function to check if file exist and return the path of txt file with message for sending via email

    # Check if file exist on current path and it is not empty
    if os.path.isfile(currentPath + "/message.txt") and os.stat(currentPath + "/message.txt").st_size != 0:
        return currentPath + "/message.txt"
    # Check if file exist on watchdog dir path and it is not empty
    elif os.path.isfile(parrentOfCurrentPath + "/" + dirNameWithWatchdogs + "/message.txt") and os.stat(parrentOfCurrentPath + "/" + dirNameWithWatchdogs + "/message.txt").st_size != 0:
        return parrentOfCurrentPath + "/" + dirNameWithWatchdogs + "/message.txt"
    else:
        return ""

# main function that do all the email things
def main():
    checkIfNeedToInitDataFile()

    # Read csv file
    df = pandas.read_csv(filepath)

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

    if len(mSourceMail) != 1:

        # If mSource contains more than 1 source mail. Then delete all source mails to set a new one
        deleteRows(df, mSourceMail)

        print("\n\nIt seems that you haven't set an email as source to send emails:\n")

        # Trigger to start the while-loop to get a valid email and password
        isSourceMailInvalid = True

        # var to act like trigger to prevent user re-enter email if its valid
        setValidMail = False

        while isSourceMailInvalid:
            # Ask for source email and its password
            if not setValidMail:
                emailSource = input("Please add a valid email address: ")
                if not isGivenEmailValid(emailSource):
                    continue
                else:
                    # Activate trigger to not re-enter the email
                    setValidMail = True

            passwordSource = input(
                "You need to add also the password of this email: ")

            # Check length of the password user submit
            if len(passwordSource) < 4:

                print("\nThe password was too short. Please try again\n")
                # To avoid ending of loop
                continue

            host = input(
                "You need to add also the host of this email: ")

            if host == "":
                print("\nYou must add a host to be able to send emails ")
                # To avoid ending without host
                continue

            isSourceMailInvalid = False
            # To insert source email on csv
            insertEntry(emailSource, passwordSource, 1, host)

    else:
        emailSource = mSourceMail["Email"][0]
        passwordSource = mSourceMail["password"][0]
        host = mSourceMail["host"][0]

    # SourceMail = 0 means that this mail is a reciptent
    reciptentTosSendMsgs = df.loc[df['SourceMail'] == 0]

    if len(reciptentTosSendMsgs) == 0:
        
        reciptentTosSendMsgs = []
        
        print("\n\nIt seems that you haven't set reciptents.\n")

        # Loop to add a or multiple destination emails
        resultOfAddAnotherEmail = "Y"

        while (resultOfAddAnotherEmail.lower() == "y"):

            emailToSend = input("Set email address to send messsages: ")

            # Check if mail is valid
            if isGivenEmailValid(emailToSend):
                # Add it on csv
                insertEntry(emailToSend, 0, 0, "")
                reciptentTosSendMsgs.append(emailToSend)
                resultOfAddAnotherEmail = input(
                    "Do you need to add another one ? (Y/N) : ")
            else:
                print("The given email is invalid. Please try again")
    else:
        # Get again the emails to send the message
        reciptentTosSendMsgs = []
        for receiverMail in df.loc[df['SourceMail'] == 0]['Email']:
            reciptentTosSendMsgs.append(receiverMail)

    # Save path of message.txt (if exist) to set the title and the message of email
    pathOfMessageFile = checkIfMessageToSendExist()

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
        except smtplib.socket.gaierror:
            print("\nSomething went wrong with SMTP_SSL (host or port) !\n")
            server.quit()
        
        # Try to login on email with given crentetial
        try:
            server.login(emailSource, passwordSource)
        except Exception:
            print("\nSomething went wrong with given crendetials !\n")
            deleteRows(df)
            server.quit()
        
        # For multiple emails
        try: 
            server.sendmail(emailSource, reciptentTosSendMsgs, message)
            server.quit()
            print("Ok. All email(s) has been send")
        except Exception:
            print("\nScript fail to send the message !\n")
        
    else:
        print("\nIt seems that there is no message.txt file in current path or in: " +
              parrentOfCurrentPath+". As result the email script abort the try of sending any message")

if __name__ == "__main__":
    main()