import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/gmail.readonly']

TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secret.json'

def authenticate():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def add_event(event, cid, event_color):
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)

    try:
        if cid == "":
            cid = "primary"

        event['colorId'] = event_color

        event_result = service.events().insert(calendarId=cid, body=event).execute().get("htmlLink")
        print(event_result)
        return event_result
    
    except Exception as e:
        print(f'Error: {e}')
        return 'Error'
