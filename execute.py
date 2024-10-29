""""""
import os
import traceback
import auth_google
import excel_parser
import html_generator
from datetime import datetime

# Configuración de variables
RUTA_SALIDAS_PRUEBAS = './.venv/pruebas/salidas'
RUTA_PLANTILLA = './.venv/pruebas/origenes/plantilla_descripciones.html'

def cargar_plantilla_html(ruta_plantilla):

   # Carga el contenido HTML de la plantilla desde la ruta especificada.

    with open(ruta_plantilla, 'r', encoding='utf-8') as archivoHtml:
        return archivoHtml.read()

def guardar_html(html_procesado, ruta_salida, serie, primer_modelo):

   # Guarda el HTML procesado en la ruta de salida especificada, usando el nombre del modelo.

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    nombre_archivo = f'descripción-{primer_modelo}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'
    with open(os.path.join(ruta_salida, nombre_archivo), 'w', encoding='utf-8') as archivoHtml:
        archivoHtml.write(str(html_procesado))
    print(f"Archivo {nombre_archivo} creado en la ruta {ruta_salida}")

def procesar_datos(sheet):
    sheets_dict = auth_google.download_google_sheet_as_dict(sheet)
    grouped_data = {sheet_name: excel_parser.filter_and_group_data(df) for sheet_name, df in sheets_dict.items()}
    return sheets_dict, grouped_data

def actualizar_google_sheet(sheet, sheets_dict):

    # Actualiza únicamente la columna "Descripción Creada" en cada hoja de Google Sheets.

    print() # Pequeño salto de linea para diferenciar mensajes

    if sheet is not None:
        for sheet_name, df in sheets_dict.items():
            try:
                worksheet = sheet.worksheet(sheet_name)
                #if df["Descripción Creada"].eq("Si").all():
                #    print(f"Ya se ha creado la descripción de la serie '{serie}' en la hoja '{proveedor}', no se generará nuevamente.")
                #    continue  # Saltar esta serie si ya tiene la descripción creada
                #else:
                # Actualizar solo la columna 'Descripción Creada' si se realizaron cambios
                col_idx = df.columns.get_loc("Descripción Creada") + 1  # +1 porque gspread usa índices 1-based
                descripcion_col = df["Descripción Creada"].tolist()
                cell_range = f"{chr(64 + col_idx)}2:{chr(64 + col_idx)}{len(descripcion_col) + 1}"  # Desde A2 hasta el final
                worksheet.update(values=[[cell] for cell in descripcion_col], range_name=cell_range)
                print(f"Hoja '{sheet_name}' actualizada en Google Sheets.")
            except Exception as e:
                print(f"Error al actualizar la hoja '{sheet_name}':")
                traceback.print_exc()
    else:
        print("No se pudo autenticar, no se realizó la actualización de Google Sheets.")

# Ejecución del programa

# Paso 1: Intentar autenticarse y descargar el archivo de Google Sheets
sheet = auth_google.try_authenticate_and_get_sheet()
if sheet is None:
    print("No se pudo autenticar. No se podrá actualizar Google Sheets.\n")
else:
    print("Autenticación exitosa.\n")

# Paso 2: Descargar y procesar los datos del archivo de Google Sheets
sheets_dict, grouped_data = procesar_datos(sheet)

# Paso 3: Cargar la plantilla HTML y
html_bruto = cargar_plantilla_html(RUTA_PLANTILLA)

# Paso 4: Procesar cada serie y crear los archivos HTML
for proveedor, series_groups in grouped_data.items():
    for serie, group in series_groups.items():
        # Verificar si ya se ha creado la descripción para esta serie
        if group["Descripción Creada"].eq("Si").all():
            print(f"Ya se ha creado la descripción de la serie '{serie}' en la hoja '{proveedor}', no se generará nuevamente.")
            continue  # Saltar esta serie si ya tiene la descripción creada
        else:
            # Generar el HTML si la descripción no ha sido creada
            html_procesado = html_generator.insert_html_tables_into_template(html_bruto, {serie: group})
            html_procesado.find(id='probeedor').string = proveedor
            primer_modelo = group.iloc[0]["Modelo"]
            guardar_html(html_procesado, RUTA_SALIDAS_PRUEBAS, serie, primer_modelo)

        # Marcar las filas procesadas como "Si" en "Descripción Creada"
        indices = group.index
        sheets_dict[proveedor] = excel_parser.mark_description_created(sheets_dict[proveedor], indices)

# Paso 5: Actualizar Google Sheets
try:
    actualizar_google_sheet(sheet, sheets_dict)
except Exception as e:
    print("Error durante la actualización de Google Sheets: "+str(traceback.print_exc()))
""""""