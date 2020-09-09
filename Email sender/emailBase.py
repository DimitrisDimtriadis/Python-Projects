import ssl
import csv
import smtplib
import pandas
import os

filepath = 'data.csv'
rowHeaders = ['Email', 'password', 'SourceMail']


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


def deleteRows(rowsToDelete):
    # Function to delete rows base on given list with rows
    # For loop to delete and instant save the changes on file
    df.drop(rowsToDelete.index).to_csv(filepath, index=False)


def insertEntry(mEmail, mPass, mSource):
    # Function to write entry on csv file
    mEntry = pandas.DataFrame([[mEmail, mPass, mSource]],
                              columns=rowHeaders)
    mEntry.to_csv(filepath, mode='a', header=False, index=False)

def checkIfNeedToInitDataFile():
    # Function to avoid script crashing for missing csv file 
    # Check if file exists
    if not os.path.isfile("./"+filepath):
        with open('./'+filepath, 'w'): pass
        pandas.DataFrame(columns=rowHeaders).to_csv(filepath, mode = 'a', header = True, index = False)


        

if __name__ == "__main__":
    
    checkIfNeedToInitDataFile()

    # Read csv file
    df = pandas.read_csv(filepath)

    # Address of the source email
    emailSource = ""
    # Password of the source email
    passwordSource = ""

    # Check if source mail has beeen set
    # SourceMail = 1 mean that its not for sending but as source
    mSourceMail = df.loc[df['SourceMail'] == 1]

    if len(mSourceMail) != 1:

        # If mSource contains more than 1 source mail. Then delete all source mails to set a new one
        deleteRows(mSourceMail)

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

            isSourceMailInvalid = False
            # To insert source email on csv
            insertEntry(emailSource, passwordSource, 1)

    else:
        emailSource = mSourceMail["Email"]
        passwordSource = mSourceMail["password"]

    # SourceMail = 0 means that this mail is a reciptent
    reciptentTosSendMsgs = df.loc[df['SourceMail'] == 0]

    if len(reciptentTosSendMsgs) == 0:

        print("\n\nIt seems that you haven't set reciptents.\n")

        # Loop to add a or multiple destination emails
        resultOfAddAnotherEmail = "Y"

        while (resultOfAddAnotherEmail.lower() == "y"):

            emailToSend = input("Set email address to send messsages: ")

            # Check if mail is valid
            if isGivenEmailValid(emailToSend):
                # Add it on csv
                insertEntry(emailToSend, 0, 0)
                resultOfAddAnotherEmail = input(
                    "Do you need to add another one ? (Y/N) : ")
            else:
                print("The given email is invalid. Please try again")

    else:
        # Set list with reciptents to send them the message
        reciptentTosSendMsgs = reciptentTosSendMsgs["Email"]

    # Set port and email source and email host # For SSL
    port = 465

    # Email host of source email
    host = "smtp.gmail.com"

    receiverEmail = "dimitris.dimtriadis@gmail.com"

    input("Press any key to continue: $$$$ ")
    # Title of message to send on email
    emailSubject = "Test subject"
    # Message to send on email
    msgText = "Hello world"
    # Compination of Title and message of email
    message = 'Subject: {}\n\n{}'.format(emailSubject, msgText)

    # Need add loop if

    # Start procedure of sending email
    server = smtplib.SMTP_SSL(host, port)
    server.login(emailSource, passwordSource)

    # For multiple emails
    # recipients = ['john.doe@example.com', 'john.smith@example.co.uk']
    server.sendmail(emailSource, receiverEmail, message)
    server.quit()

    print("Ok. All email(s) has been send")

 # Read text file as message
 # Upload it on github
