from config import EMAIL, PASSWORD
from email.message import EmailMessage
import smtplib
from utils.input_output import speak_or_print


def send_email(receiver_add, subject, message):
    """
    Sends an email to the specified receiver address with the given subject and message.

    Parameters:
    receiver_add (str): The email address of the receiver.
    subject (str): The subject of the email.
    message (str): The content of the email message.

    Returns:
    bool: True if the email is sent successfully, False if an exception occurs.
    """
    try:
        email = EmailMessage()
        email["To"] = receiver_add
        email["Subject"] = subject
        email["From"] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False


def send_email_command():
    """
    Function to send an email using user input for receiver address, subject, and message.
    """
    speak_or_print(
        "On what email address do you want to send sir?. Please enter in the terminal"
    )
    receiver_add = input("Email address:")
    speak_or_print("What should be the subject sir?")
    subject = input().capitalize()
    speak_or_print("What is the message ?")
    message = input().capitalize()
    if send_email(receiver_add, subject, message):
        speak_or_print("I have sent the email sir")
        print("I have sent the email sir")
    else:
        speak_or_print("something went wrong Please check the error log")
