import os
import json
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secret.json'

def authenticate_google_account():
    creds = None

    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
        except json.decoder.JSONDecodeError:
            logging.warning("Invalid token file. Starting fresh authentication.")
            os.remove(TOKEN_FILE)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

creds = authenticate_google_account()
service = build('calendar', 'v3', credentials=creds)

def add_event(event, cal_id):
    try:
        if cal_id == "":
            cid = "primary"
        else:
            cid = cal_id
        event_result = service.events().insert(calendarId=cid, body=event).execute()
        return event_result.get("htmlLink")
    
    except Exception as e:
        print(f'Error: {e}')
        return 'Error'