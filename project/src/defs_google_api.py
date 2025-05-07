import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def authenticate_google_api(scopes, type, token_path, credentials_path):

    creds = None

    if os.path.exists(token_path):
        print(f"Loading token from {token_path}")
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            try:
                print(f"Authenticating using credentials from {credentials_path}")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error during authentication: {e}")
                return None
        with open(token_path, "w") as token:
            print(f"Saving new token to {token_path}")
            token.write(creds.to_json())

    if type == "gmail":
        try:
            print("Creating Gmail service...")
            return build("gmail", "v1", credentials=creds)
        except Exception as e:
            print(f"Error creating Gmail service: {e}")
            return None
        
    if type == "drive":
        try:
            return build("drive", "v3", credentials=creds)
        except Exception as e:
            print(f"Error creating Drive service: {e}")
            return None
        
    return None