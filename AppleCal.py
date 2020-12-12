from pyicloud import PyiCloudService
from datetime import datetime, timedelta
from apple_calendar_integration import ICloudCalendarAPI

def createGetBuild(username, passw):
    return PyiCloudService(username, passw)

def createCreateBuild(username, passw):
    return ICloudCalendarAPI(username, passw)

def get_events(username, passw, from_dt, to_dt):
    build = createGetBuild(username, passw)
    return build.calendar.events(from_dt, to_dt)

def create_event(username, passw, startDate, title):
    build = createCreateBuild(username, passw)
    build.create_event(title, startDate.timestamp(), startDate.timestamp() + timedelta(hours=2))