import smtplib
import base64

def sendMail(to, message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("aanduidingenscript@gmail.com", base64.b64decode("ampucWJkdWp6bGN2b21qcQ==").decode("utf-8"))
    server.sendmail(
    "aanduidingenscript@gmail.com", 
    to, 
    message)
    server.quit()