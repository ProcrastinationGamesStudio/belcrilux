"""import os
import auth_google
import excel_parser
import html_generator
from datetime import datetime

# Configuración de variables
FILE_ID = '1qmi503F2TXXTJ4vXpvjHxMBuHqI4ynAf32XCAlXsB40'  # ID de tu archivo en Google Drive
RUTA_SALIDAS_PRUEBAS = './.venv/pruebas/salidas'
RUTA_PLANTILLA = f'./.venv/pruebas/origenes/plantilla_descripciones.html'
#RUTA_PLANTILLA = './.venv/pruebas/origenes/plantilla_descripciones-sf-xxxxD3.html'


def cargar_plantilla_html(ruta_plantilla):
    ""
    Carga el contenido HTML de la plantilla desde la ruta especificada.
    ""
    with open(ruta_plantilla,'r',encoding='utf-8') as archivoHtml:
        return archivoHtml.read()


def procesar_datos_excel(file_id):
    ""
    Descarga el archivo Excel desde Google Drive y lee todas sus hojas.
    Devuelve un diccionario con nombres de hojas como claves y datos de las hojas agrupados como valores.
    ""
    # Descargar el archivo Excel en formato binario
    file = auth_google.download_excel_from_drive(file_id)

    # Leer todas las hojas en un diccionario de DataFrames
    sheets_dict = excel_parser.read_excel_sheets(file)

    # Filtrar y agrupar datos por serie para cada hoja
    grouped_data = {sheet_name: excel_parser.filter_and_group_data(df)
                    for sheet_name, df in sheets_dict.items()}
    return sheets_dict, grouped_data


def insertar_tablas_en_html(html_bruto, series_groups):
    ""
    Inserta tablas HTML en el bloque 'listado_variables' de la plantilla HTML
    utilizando los datos agrupados por serie.
    ""
    return html_generator.insert_html_tables_into_template(html_bruto, series_groups)


def actualizar_excel_con_descripciones(df_dict, grouped_data, file_id):
    ""
    Actualiza el archivo Excel en Google Drive después de marcar "Descripción Creada" como "Si"
    en las filas procesadas de cada hoja.
    ""
    for sheet_name, df in df_dict.items():
        series_groups = grouped_data[sheet_name]
        indices = df[df['Series'].isin(series_groups.keys())].index
        df_dict[sheet_name] = excel_parser.mark_description_created(df, indices)

    # Guardar el archivo Excel actualizado en disco
    excel_parser.save_excel_file(df_dict)

    # Subir el archivo actualizado a Google Drive
    auth_google.upload_excel_to_drive(file_id)


def guardar_html(html_procesado, ruta_salida, proveedor):
    ""
    Guarda el HTML procesado en la ruta de salida especificada, utilizando el
    nombre del proveedor en el nombre del archivo.
    ""
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    nombre_archivo = f'descripción-{proveedor}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'
    with open(os.path.join(ruta_salida, nombre_archivo), 'w', encoding='utf-8') as archivoHtml:
        archivoHtml.write(str(html_procesado))
    print(f"\nArchivo {nombre_archivo} creado en la ruta {ruta_salida}")

# Ejecución del programa
html_bruto = cargar_plantilla_html(RUTA_PLANTILLA)
sheets_dict, grouped_data = procesar_datos_excel(FILE_ID)

# Procesar cada hoja como un proveedor independiente
for proveedor, series_groups in grouped_data.items():
    # Insertar tablas en la plantilla HTML para cada proveedor
    html_procesado = insertar_tablas_en_html(html_bruto, series_groups)

    # Insertar el nombre del proveedor en el HTML
    html_procesado.find(id='probeedor').string = proveedor

    # Guardar el HTML específico para cada proveedor
    guardar_html(html_procesado, RUTA_SALIDAS_PRUEBAS, proveedor)

# Actualizar el archivo Excel después de procesar todas las hojas
actualizar_excel_con_descripciones(sheets_dict, grouped_data, FILE_ID)
import os
import auth_google
import excel_parser
import html_generator
from datetime import datetime

# Configuración de variables
FILE_ID = '1qmi503F2TXXTJ4vXpvjHxMBuHqI4ynAf32XCAlXsB40'  # ID del archivo de Google Sheets público
RUTA_SALIDAS_PRUEBAS = './.venv/pruebas/salidas'
RUTA_PLANTILLA = './.venv/pruebas/origenes/plantilla_descripciones.html'


def cargar_plantilla_html(ruta_plantilla):
    ""
    Carga el contenido HTML de la plantilla desde la ruta especificada.
    ""
    with open(ruta_plantilla, 'r', encoding='utf-8') as archivoHtml:
        return archivoHtml.read()


def procesar_datos_excel(file_id, sheet_names):
    ""
    Descarga y procesa todas las hojas de un archivo público de Google Sheets.
    Devuelve un diccionario con nombres de hojas como claves y datos de las hojas agrupados como valores.
    ""
    sheets_dict = {}
    grouped_data = {}

    # Descargar y procesar cada hoja
    for sheet_name in sheet_names:
        df = auth_google.download_public_google_sheet(file_id, sheet_name)
        print(f"Columnas en la hoja '{sheet_name}': {df.columns.tolist()}")
        sheets_dict[sheet_name] = df
        grouped_data[sheet_name] = excel_parser.filter_and_group_data(df)

    return sheets_dict, grouped_data


def insertar_tablas_en_html(html_bruto, series_groups):
    ""
    Inserta tablas HTML en el bloque 'listado_variables' de la plantilla HTML
    utilizando los datos agrupados por serie.
    ""
    return html_generator.insert_html_tables_into_template(html_bruto, series_groups)


def guardar_html(html_procesado, ruta_salida, proveedor):
    ""
    Guarda el HTML procesado en la ruta de salida especificada, utilizando el
    nombre del proveedor en el nombre del archivo.
    ""
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    nombre_archivo = f'descripción-{proveedor}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'
    with open(os.path.join(ruta_salida, nombre_archivo), 'w', encoding='utf-8') as archivoHtml:
        archivoHtml.write(str(html_procesado))
    print(f"\nArchivo {nombre_archivo} creado en la ruta {ruta_salida}")


# Ejecución del programa
html_bruto = cargar_plantilla_html(RUTA_PLANTILLA)

# Define aquí los nombres de las hojas que deseas procesar
SHEET_NAMES = ['NombreDeLaHoja1', 'NombreDeLaHoja2']  # Modifica según los nombres de las hojas

# Descargar y procesar los datos del archivo de Google Sheets público
sheets_dict, grouped_data = procesar_datos_excel(FILE_ID, SHEET_NAMES)

# Procesar cada hoja como un proveedor independiente
for proveedor, series_groups in grouped_data.items():
    # Insertar tablas en la plantilla HTML para cada proveedor
    html_procesado = insertar_tablas_en_html(html_bruto, series_groups)

    # Insertar el nombre del proveedor en el HTML
    html_procesado.find(id='probeedor').string = proveedor

    # Guardar el HTML específico para cada proveedor
    guardar_html(html_procesado, RUTA_SALIDAS_PRUEBAS, proveedor)

# No se actualiza el archivo en Google Drive ya que estamos usando una hoja pública"""
import os
import auth_google
import excel_parser
import html_generator
from datetime import datetime

# Configuración de variables
FILE_ID = '1qmi503F2TXXTJ4vXpvjHxMBuHqI4ynAf32XCAlXsB40'  # ID del archivo de Google Sheets público
RUTA_SALIDAS_PRUEBAS = './.venv/pruebas/salidas'
RUTA_PLANTILLA = './.venv/pruebas/origenes/plantilla_descripciones-sf-xxxxD3.html'


def cargar_plantilla_html(ruta_plantilla):
    """
    Carga el contenido HTML de la plantilla desde la ruta especificada.
    """
    with open(ruta_plantilla, 'r', encoding='utf-8') as archivoHtml:
        return archivoHtml.read()


def procesar_datos_excel(file_id, sheet_names):
    """
    Descarga y procesa todas las hojas de un archivo público de Google Sheets.
    Devuelve un diccionario con nombres de hojas como claves y datos de las hojas agrupados como valores.
    """
    sheets_dict = {}
    grouped_data = {}

    # Descargar y procesar cada hoja
    for sheet_name in sheet_names:
        df = auth_google.download_public_google_sheet(file_id, sheet_name)
        sheets_dict[sheet_name] = df
        grouped_data[sheet_name] = excel_parser.filter_and_group_data(df)

    return sheets_dict, grouped_data


def insertar_tablas_en_html(html_bruto, series_groups):
    """
    Inserta tablas HTML en el bloque 'listado_variables' de la plantilla HTML
    utilizando los datos agrupados por serie.
    """
    return html_generator.insert_html_tables_into_template(html_bruto, series_groups)


def guardar_html(html_procesado, ruta_salida, serie, primer_modelo):
    """
    Guarda el HTML procesado en la ruta de salida especificada, utilizando el
    primer modelo de la serie y la fecha/hora en el nombre del archivo.
    """
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    nombre_archivo = f'descripción-{primer_modelo}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'
    with open(os.path.join(ruta_salida, nombre_archivo), 'w', encoding='utf-8') as archivoHtml:
        archivoHtml.write(str(html_procesado))
    print(f"\nArchivo {nombre_archivo} creado en la ruta {ruta_salida}")


# Ejecución del programa
html_bruto = cargar_plantilla_html(RUTA_PLANTILLA)

# Define aquí los nombres de las hojas que deseas procesar
SHEET_NAMES = ['NombreDeLaHoja1', 'NombreDeLaHoja2']  # Modifica según los nombres de las hojas

# Descargar y procesar los datos del archivo de Google Sheets público
sheets_dict, grouped_data = procesar_datos_excel(FILE_ID, SHEET_NAMES)

# Procesar cada serie por separado
for proveedor, series_groups in grouped_data.items():
    for serie, group in series_groups.items():
        # Insertar tablas en la plantilla HTML para la serie específica
        html_procesado = insertar_tablas_en_html(html_bruto, {serie: group})

        # Insertar el nombre del proveedor en el HTML
        html_procesado.find(id='probeedor').string = proveedor

        # Obtener el primer modelo de la serie para el nombre del archivo
        primer_modelo = group.iloc[0]["Nombre"]  # Ajusta "Nombre" según la columna correspondiente al modelo

        # Guardar el HTML específico para cada serie usando el primer modelo en el nombre del archivo
        guardar_html(html_procesado, RUTA_SALIDAS_PRUEBAS, serie, primer_modelo)

# No se actualiza el archivo en Google Drive ya que estamos usando una hoja pública