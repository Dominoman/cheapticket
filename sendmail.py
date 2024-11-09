import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


class SMTP:
    def __init__(self,server:str,port:int,login:str,psw:str="")->None:
        self.server=server
        self.port=port
        self.login=login
        self.psw=psw

    def send_mail(self, send_to:str, subject:str, html_content:str, images: list[str] = None) -> None:
        if images is None:
            images = []
        msg = MIMEMultipart("related")
        msg["Subject"]=subject
        msg["From"]=self.login
        msg["To"]=send_to
        msg.attach(MIMEText(html_content,"html"))

        for image in images:
            basename=Path(image).stem
            with open(image,"rb") as img_file:
                img_data=img_file.read()
                image=MIMEImage(img_data)
                image.add_header("Content-ID",f"<{basename}>")
                msg.attach(image)

        with smtplib.SMTP(self.server,self.port) as server:
            server.starttls()
            if self.psw!="":
                server.login(self.login,self.psw)
            server.send_message(msg)
