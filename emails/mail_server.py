import smtplib, ssl
from smtplib import SMTPException, SMTPAuthenticationError
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.singleton import SingletonMeta
import os
import logging
logger = logging.getLogger(__name__)
class MailServer(metaclass=SingletonMeta):
    """
    A singleton patterned class to represent connection and sending an email.

    ...

    Methods
    -------
    send_mail(subject,body,attachment,receiver_email):
        Sends an email with attachment to desired receivers.
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the mail server object.

        """
        self.port = os.getenv("smtp_port")
        self.sender_email = os.getenv("sender_email")
        self.smtp_server = os.getenv("smtp_server")
        self.sender_password = os.getenv("sender_password")
        logger.info("SSL connection to SMTP server is initialized")
        self.server = smtplib.SMTP_SSL(self.smtp_server, self.port, context=ssl.create_default_context())
        try:
            self.server.login(self.sender_email, self.sender_password)
        except SMTPAuthenticationError:
            logger.exception("Failed to authenticate with current credentials")
        except Exception:
            logger.exception("Unexpected error")


    def send_mail(self,subject,body,attachment,receiver_email):
        '''
        Sends an email with attachment to desired receivers.

                Parameters:
                        subject (str) : Subject of email.
                        body (str) : Body content of email.
                        attachment (str) : Absolute or relative path of the attachment to be sent.
                        receiver_email (list) : List of receiver mail addresses.

        '''
        logger.info("Preparing to send an email with transcription from {} as attachment".format(attachment))
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with open(attachment, "rb") as att:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(att.read())  # Encode file in ASCII characters to send by email
        except IOError:
            logger.exception("I/O error")
        except FileNotFoundError:
            logger.exception("FileNotFoundError")
        except Exception:
            logger.exception("Unexpected error")

        encoders.encode_base64(part)
        part.add_header( "Content-Disposition",f"attachment; filename= meeting_transcription.txt",)
        message.attach(part)
        for receiver in receiver_email:
            try:
                logger.info("Sending an email to {}".format(receiver))
                message["To"] = receiver
                text = message.as_string()
                self.server.sendmail(self.sender_email,receiver,text)
                logger.info("Email has been successfully sent to {}".format(receiver))
            except SMTPException:
                logger.exception("An error occured while sending mail.")
            except Exception:
                logger.exception("Unexpected error")




