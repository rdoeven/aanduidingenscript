#!/bin/env python3
import sys
import GoogleCal
import MatchLoader

#params
name = "Doeven Robbe"

#main script

if __name__ == "__main__":
	if len(sys.argv) > 0:
		name = str(sys.argv)

matches = MatchLoader.LoadData(name)
matchEvents = [event["summary"]+event["start"]["dateTime"][:-6] for event in GoogleCal.get_events()]

for match in matches:
	if match.getmatch() + match.date.isoformat() not in matchEvents: 
		GoogleCal.create_event(match.date , match.getmatch())