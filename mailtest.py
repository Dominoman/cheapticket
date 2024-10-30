#!/usr/bin/env python3
import config
from sendmail import SMTP

if __name__=="__main__":
    server=SMTP(config.SMTP_SERVER,config.SMTP_PORT,config.SMTP_FROM,config.SMTP_PSW)
    with open("templates/template.html","r") as fo:
        template=fo.read()
    server.send_mail("oraveczl@asz.hu","Hello",template,["templates/down.png","templates/up.png","templates/repcsi.jpg","templates/vonal.png"])
    print("Ok")