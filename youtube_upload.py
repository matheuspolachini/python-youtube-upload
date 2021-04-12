import sys
import os.path
import pickle
import pyperclip
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

API_SERVICE_NAME = "youtube"
API_SERVICE_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CREDENTIALS_FILE = f"{API_SERVICE_NAME}_{API_SERVICE_VERSION}_credentials.pickle"


def build_youtube_service():
    if credentials_file_exists():
        print("Using existing credentials")
        credentials = read_credentials()
    else:
        credentials = auth_user()
        save_credentials(credentials)

    return build(API_SERVICE_NAME, API_SERVICE_VERSION, credentials=credentials)


def auth_user():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes=SCOPES)

    return flow.run_local_server()


def credentials_file_exists():
    return os.path.exists(CREDENTIALS_FILE)


def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "wb") as credentials_file:
        pickle.dump(credentials, credentials_file)


def read_credentials():
    with open(CREDENTIALS_FILE, "rb") as credentials_file:
        return pickle.load(credentials_file)


def upload_video(youtube, file):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": file
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        },
        media_body=MediaFileUpload(file)
    )

    response = request.execute()

    return response['id']


if __name__ == "__main__":
    youtube = build_youtube_service()
    print("Uploading video")
    video_id = upload_video(youtube, sys.argv[1])

    video_link = f"https://www.youtube.com/watch?v={video_id}"
    pyperclip.copy(video_link)

    print(f"Link copied to clipboard: {video_link}")
