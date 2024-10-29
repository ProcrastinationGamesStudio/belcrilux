""""""
import json
import gspread
import traceback
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENCIALES = "./JSONs/credentials.json"

def try_authenticate_and_get_sheet():

   # Autentica usando credenciales de servicio y devuelve el archivo de Google Sheets.
   # Si falla, muestra el error y devuelve None.

    try:
        with open(CREDENCIALES, "r") as file:
            credenciales_json = json.load(file)
        file_id = credenciales_json["file_id"]
        creds = Credentials.from_service_account_file(CREDENCIALES, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(file_id)
        return sheet
    except Exception as e:
        print("Error de autenticación para edición en Google Sheets: "+str(traceback.print_exc()))
        return None

def download_google_sheet_as_dict(sheet):

   # Descarga todas las hojas de un archivo de Google Sheets autenticado como DataFrames.
   # Devuelve un diccionario con los nombres de las hojas y los DataFrames correspondientes.

    sheets_dict = {}
    try:
        for worksheet in sheet.worksheets():
            df = pd.DataFrame(worksheet.get_all_records())
            sheets_dict[worksheet.title] = df
    except Exception as e:
        print("Error al descargar hojas de Google Sheets: "+str(traceback.print_exc()))
    return sheets_dict
""""""