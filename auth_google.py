"""import os
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

# Alcance necesario para acceder al archivo en Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    ""
    Autentica el acceso a Google Drive usando OAuth 2.0.
    Devuelve un servicio autenticado para hacer solicitudes a la API de Google Drive.
    ""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def download_excel_from_drive(file_id):
    ""
    Descarga un archivo Excel desde Google Drive usando el `file_id` especificado.
    Devuelve el archivo en formato binario.
    ""
    service = authenticate_google_drive()
    request = service.files().get_media(fileId=file_id)
    file = BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    file.seek(0)
    return file  # Devuelve el archivo binario (BytesIO) sin procesarlo

def upload_excel_to_drive(file_id, output_path='updated_file.xlsx'):
    ""
    Sube el archivo Excel actualizado a Google Drive utilizando el `file_id` del archivo original.
    ""
    service = authenticate_google_drive()
    media = MediaFileUpload(output_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    service.files().update(fileId=file_id, media_body=media).execute()"""
import pandas as pd

def download_public_google_sheet(sheet_id, sheet_name):
    """
    Descarga el contenido de una hoja pública de Google Sheets como un DataFrame de pandas.
    """
    # URL para descargar la hoja en formato CSV
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url)
    return df