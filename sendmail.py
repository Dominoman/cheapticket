import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def sendmail(to, subject, body):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = config.SMTP_FROM
    msg['To'] = to

    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.SMTP_FROM, config.SMTP_PSW)
    msg.attach(MIMEText(body,"html"))
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    sendmail("sirrobinofc@gmail.com", "Test Subject", "<html><body><h1>Test Email</h1><p>This is a test email.</p></body></html>")