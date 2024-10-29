""""""
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
    """
    # Agrupar por series similares
    series_groups = group_similar_series(df_filtered['Serie'].tolist(), threshold=threshold)
    
    grouped_data = {}
    for group_key, similar_series in series_groups.items():
        # Filtrar y agrupar por series similares en el DataFrame filtrado
        grouped_data[group_key] = df_filtered[df_filtered['Serie'].isin(similar_series)]
    """
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
""""""