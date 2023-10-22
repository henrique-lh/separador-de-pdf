from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os
from dotenv import load_dotenv
import glob


load_dotenv()

SCOPES = [os.getenv('URL')]


def create_folder(folder):
    creds = None
    path_to_secret_json = os.getenv('PATH_TO_SECRET_JSON')
    if os.path.exists(path_to_secret_json):
        creds = Credentials.from_authorized_user_file(path_to_secret_json, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('PATH_TO_CREDENTIALS_JSON'), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(path_to_secret_json, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        folder_metadata = {
            'name': folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [os.getenv('PARENT_ID')]
        }
        create_folder = service.files().create(body=folder_metadata, fields='id'
                                      ).execute()
        folder_id = create_folder.get('id')
        return folder_id, folder
    except HttpError as error:
        print(f'Ocorreu um erro: {error}')


def upload_files(folder_id, folder, specific_file: str = None):
    creds = None
    
    path_to_secret_json = os.getenv('PATH_TO_SECRET_JSON')
    if os.path.exists(path_to_secret_json):
        creds = Credentials.from_authorized_user_file(path_to_secret_json, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('PATH_TO_CREDENTIALS_JSON'), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(path_to_secret_json, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        for file in glob.glob(f'{folder}/*.pdf'):
            if file != specific_file:
                continue
            file_metadata = {
                'name': os.path.basename(file),
                'parents': [folder_id],
            }
            media = MediaFileUpload(file, mimetype='application/pdf')
            _file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
            print(f'Arquivo {file} salvo com sucesso -> ID: {_file.get("id")}')
    except HttpError as error:
        print(f'Ocorreu um erro: {error}')
