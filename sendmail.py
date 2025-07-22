import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.config import config


def sendmail(to, subject, body,attachments:dict[str,str]=None):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = config.SMTP_FROM
    msg['To'] = to

    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.SMTP_FROM, config.SMTP_PSW)
    msg.attach(MIMEText(body,"html"))
    if attachments:
        for filename, filepath in attachments.items():
            with open(filepath, "rb") as attachment:
                part = MIMEImage(attachment.read())
                part.add_header("Content-ID", f"<{filename}>" )
                msg.attach(part)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    imgs = {"BR": "BR.jpg"}
    sendmail("sirrobinofc@gmail.com", "Test Subject", "<html><body><h1>Test Email</h1><p>This is a test email.<img src='cid:BR' alt='BR'></p></body></html>",imgs)
