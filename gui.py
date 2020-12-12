import tkinter as tk
from datetime import timedelta
import MatchLoader
import Mail
import urllib.request
import GoogleCal
import AppleCal
import os
import re

def load():
    name = f"{txtName.get()} {txtVName.get()}"
    data = MatchLoader.LoadData(name)
    if googlevar.get():
        eventset = GoogleCal.get_events()
        userEvents = [event["summary"]+event["start"]["dateTime"][:-6] for event in eventset]
    else:
        userEvents = []

    if emailvar.get():
        message = "Hey " + name + "\n\nHier zijn je aanduidingen voor het moment:\n\n" + '\n'.join([str(match) for match in data]) + "\n\nDir bericht werd automatisch gegenereerd met MatchScript"
        Mail.sendMail(txtEmail.get(), message)

    for i, match in enumerate(data):
        if googlevar.get():
            if match.getmatch()+match.date.isoformat() not in userEvents: 
                GoogleCal.create_event(match.date , match.getmatch())
        
        if appleVar.get():
            if match.getmatch() in [event['title'] for event in AppleCal.get_events(txtAppleUsername.get(), txtApplePassword.get(), match.date.date - timedelta(days=1), match.date.date + timedelta(days=1))]:
                AppleCal.create_event(txtAppleUsername.get(), txtApplePassword.get(), match.date, match.getmatch())

        tk.Label(window, text = str(match)).grid(row = 5 + i, columnspan=20, sticky=tk.W)


def toggleEmail():
    if emailvar.get():
        txtEmail.grid(column=3, row=1, sticky=tk.W)
    else:
        txtEmail.grid_forget()

def toggleApple():
    if appleVar.get():
        txtAppleUsername.grid(column=3, row=2, sticky=tk.W)
        txtApplePassword.grid(column=4, row=2, sticky=tk.W)
    else:
        txtAppleUsername.grid_forget()
        txtApplePassword.grid_forget()

window = tk.Tk()
window.title("aanduidingenscript")
window.geometry("1000x800")
googlevar = tk.BooleanVar()
emailvar = tk.BooleanVar()
appleVar = tk.BooleanVar()
email = tk.StringVar()
email.set("email")
appleUsername = tk.StringVar()
appleUsername.set("username")
applePassword = tk.StringVar()
applePassword.set("password")

lblName = tk.Label(window, text="Last name")
txtName = tk.Entry(window, width=20)
lblVName = tk.Label(window, text="First name")
txtVName = tk.Entry(window, width=20)
lblwhitespace = tk.Label(window, text=" ")
btnLoad = tk.Button(window, text="load", command=load)
chkGoogle = tk.Checkbutton(window, text="add to google calendar", variable=googlevar)
chkEmail = tk.Checkbutton(window, text="send me in mail", variable=emailvar, command=toggleEmail)
txtEmail = tk.Entry(window, width=25, textvariable=email)
chkApple = tk.Checkbutton(window, text="add to Apple Calander", variable=appleVar, command=toggleApple)
txtAppleUsername = tk.Entry(window, width=25, textvariable=appleUsername)
txtApplePassword = tk.Entry(window, width=25, textvariable=applePassword)

lblName.grid(column=0, row=0)
lblVName.grid(column=0, row=1)
txtName.grid(column=1, row=0)
txtVName.grid(column=1, row=1)
btnLoad.grid(column=3, row=0, sticky=tk.W)
lblwhitespace.grid(column=0, row=4)
chkGoogle.grid(column=2, row=0, sticky=tk.W)
chkEmail.grid(column=2, row=1, sticky=tk.W)
chkApple.grid(column=2, row = 2, sticky=tk.W)

window.mainloop()