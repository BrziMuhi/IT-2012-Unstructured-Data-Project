import os
import pickle
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

load_dotenv()

CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
FOLDER_ID = os.getenv("FOLDER_ID")
SCOPES = [os.getenv("SCOPES")]


def authenticate_drive():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)


def upload_file(file_path):
    service = authenticate_drive()

    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [FOLDER_ID]  # 👈 THIS PUTS FILE INTO YOUR FOLDER
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"Uploaded: {file_path} (ID: {file.get('id')})")