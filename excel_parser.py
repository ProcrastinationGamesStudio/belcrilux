"""
import gspread
import pandas as pd
from difflib import SequenceMatcher

def read_excel_sheets(file):

   # Lee todas las hojas de un archivo Excel descargado y devuelve un diccionario
   # donde las claves son los nombres de las hojas y los valores son los DataFrames correspondientes.

    excel_data = pd.ExcelFile(file)
    sheets_dict = {sheet_name: pd.read_excel(excel_data, sheet_name=sheet_name, engine='openpyxl')
        for sheet_name in excel_data.sheet_names}
    return sheets_dict

def filter_and_group_data(df):

   # Filtra las filas donde la columna 'Descripción Creada' tiene 'No' o está vacía.
   # Agrupa los datos restantes por la columna 'Series' y devuelve un diccionario con los datos agrupados.

    # Filtrar filas con "Descripción Creada" en "No" o vacío
    df_filtered = df[df['Descripción Creada'].str.lower().fillna('no').eq('no')]
    ""
    # Agrupar por series similares
    series_groups = group_similar_series(df_filtered['Serie'].tolist(), threshold=threshold)
    
    grouped_data = {}
    for group_key, similar_series in series_groups.items():
        # Filtrar y agrupar por series similares en el DataFrame filtrado
        grouped_data[group_key] = df_filtered[df_filtered['Serie'].isin(similar_series)]
    ""
    # Agrupar por "Series" y devolver el grupo de series en un diccionario
    grouped_data = {series: group for series, group in df_filtered.groupby('Serie')}
    return grouped_data

def group_similar_series(series_list, threshold=0.8):

    # Agrupa series similares usando una comparación de similitud de texto (Levenshtein).

    groups = {}
    for serie in series_list:
        found_group = False
        for group_key in groups.keys():
            if SequenceMatcher(None, serie, group_key).ratio() > threshold:
                groups[group_key].append(serie)
                found_group = True
                break
        if not found_group:
            groups[serie] = [serie]
    return groups
def mark_description_created(df, indices):

   # Marca las filas especificadas en indices de la columna 'Descripción Creada' como "Si".
   # Devuelve el DataFrame actualizado.

    df.loc[indices, 'Descripción Creada'] = "Si"
    return df

def save_excel_file(df_dict, output_path='updated_file.xlsx'):

   # Guarda un diccionario de DataFrames en un archivo Excel, creando una hoja por cada entrada.

    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
"""
import pandas as pd
import html_generator
import traceback as trace
from difflib import SequenceMatcher

def mark_description_created(df, indices):

    # Marca las filas especificadas en `indices` de la columna 'Descripción Creada' como "Si".
    # Devuelve el DataFrame actualizado.

    df.loc[indices, 'Descripción Creada'] = "Si"
    return df

def actualizar_google_sheet(sheet, sheets_dict):

    # Actualiza únicamente la columna "Descripción Creada" en cada hoja de Google Sheets si es necesario.
    print()
    if sheet is not None:
        for sheet_name, df in sheets_dict.items():
            try:
                worksheet = sheet.worksheet(sheet_name)
                col_idx = df.columns.get_loc("Descripción Creada") + 1  # Índice de la columna "Descripción Creada"
                descripcion_col = df["Descripción Creada"].tolist()
                cell_range = f"{chr(64 + col_idx)}2:{chr(64 + col_idx)}{len(descripcion_col) + 1}"
                worksheet.update(values=[[cell] for cell in descripcion_col], range_name=cell_range)
                print(f"Hoja '{sheet_name}' actualizada en Google Sheets.")
            except Exception as e:
                print(f"Error al actualizar la hoja '{sheet_name}':")
                trace.print_exc()
    else:
        print("No se pudo autenticar, no se realizó la actualización de Google Sheets.")


def read_excel_sheets(file):
    # Lee todas las hojas de un archivo Excel descargado y devuelve un diccionario
    # donde las claves son los nombres de las hojas y los valores son los DataFrames correspondientes.

    excel_data = pd.ExcelFile(file)
    sheets_dict = {sheet_name: pd.read_excel(excel_data, sheet_name=sheet_name, engine='openpyxl')
                   for sheet_name in excel_data.sheet_names}
    return sheets_dict


def filter_and_group_data(df):
    # Filtra las filas donde la columna 'Descripción Creada' tiene 'No' o está vacía.
    # Agrupa los datos restantes por la columna 'Series' y devuelve un diccionario con los datos agrupados.

    # Filtrar filas con "Descripción Creada" en "No" o vacío
    df_filtered = df[df['Descripción Creada'].str.lower().fillna('no').eq('no')]
    ""
    # Agrupar por series similares
    #series_groups = group_similar_series(df_filtered['Serie'].tolist(), threshold=0.8)

    #grouped_data = {}
    #for group_key, similar_series in series_groups.items():
    #    # Filtrar y agrupar por series similares en el DataFrame filtrado
    #    grouped_data[group_key] = df_filtered[df_filtered['Serie'].isin(similar_series)]

    # Agrupar por "Series" y devolver el grupo de series en un diccionario
    return {series: group for series, group in df_filtered.groupby('Serie')}

"""
def group_similar_series(series_list, threshold=0.8):
    # Agrupa series similares usando una comparación de similitud de texto (Levenshtein).

    groups = {}
    for serie in series_list:
        found_group = False
        for group_key in groups.keys():
            if SequenceMatcher(None, serie, group_key).ratio() > threshold:
                groups[group_key].append(serie)
                found_group = True
                break
        if not found_group:
            groups[serie] = [serie]
    return groups
"""
"""
def mark_description_created(df, indices):
    # Marca las filas especificadas en indices de la columna 'Descripción Creada' como "Si".
    # Devuelve el DataFrame actualizado.

    df.loc[indices, 'Descripción Creada'] = "Si"
    return df
"""

def save_excel_file(df_dict, output_path='updated_file.xlsx'):
    # Guarda un diccionario de DataFrames en un archivo Excel, creando una hoja por cada entrada.

    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def process_and_mark_descriptions(sheets_dict, html_template):

    # Procesa cada hoja y verifica si se necesita actualización en 'Descripción Creada'.
    # Genera HTML y marca descripciones donde corresponda.

    hojas_a_actualizar = []
    for sheet_name, df in sheets_dict.items():
        # Verificar si la hoja necesita actualización
        if df["Descripción Creada"].eq("Si").all():
            print(f" Ya se ha creado la descripción de todas las series en la hoja '{sheet_name}', no se requiere actualización.")
            continue
    # Procesar cada serie que necesita actualización
        for serie, group in filter_and_group_data(df).items():
            # Generar el HTML solo si la descripción no ha sido creada para la serie
            if not group["Descripción Creada"].eq("Si").all():
                # Llamar a html_generator para crear el HTML
                html_generator.generate_and_save_html(html_template, group, sheet_name, serie)

                # Marcar filas como "Si" en "Descripción Creada"
                indices = group.index
                sheets_dict[sheet_name] = mark_description_created(sheets_dict[sheet_name], indices)

        # Agregar la hoja a la lista de actualizaciones pendientes
        hojas_a_actualizar.append(sheet_name)
    return hojas_a_actualizar