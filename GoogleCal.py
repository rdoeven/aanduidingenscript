#imports
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import MatchLoader
import datetime
from datetime import timedelta
import pickle
import os

#params
scopes = ['https://www.googleapis.com/auth/calendar']
credsfolder = "creds"

def createBuild():
    if os.path.exists(credsfolder + "/token.pkl"):
        credentials = pickle.load(open(credsfolder + "/token.pkl", "rb"))
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credsfolder + "/" +'credentials.json', scopes)
        credentials = flow.run_local_server(port=0)
        with open(credsfolder + "/token.pkl", 'wb') as token:
            pickle.dump(credentials, token)
    
    try:
        return build("calendar", "v3", credentials=credentials)
    except:
        print("could not establisch connection with google servers")

def create_event(time, summary, duration=2, description=None, location=None):
    service = createBuild()
    end_time = time + timedelta(hours=duration)
    event = {
	    'summary': summary,
	    'location': location,
	    'description': description,
	    'colorId': 5,
	    'start': {
	        'dateTime': time.isoformat(),
	        'timeZone': "Europe/Brussels",
	    },
	    'end': {
	        'dateTime': end_time.isoformat(),
	        'timeZone': "Europe/Brussels",
	    },
	}
    return service.events().insert(calendarId='primary', body=event).execute()

def get_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    service = createBuild()
    return service.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute().get('items', [])

def del_events(events):
    service = createBuild()
    for event in events:
        service.events().delete(calendarId='primary', eventId=event)