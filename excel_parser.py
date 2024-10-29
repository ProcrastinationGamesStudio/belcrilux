#import gspread
import pandas as pd

def read_excel_sheets(file):
    """
    Lee todas las hojas de un archivo Excel descargado y devuelve un diccionario
    donde las claves son los nombres de las hojas y los valores son los DataFrames correspondientes.
    """
    excel_data = pd.ExcelFile(file)
    sheets_dict = {sheet_name: pd.read_excel(excel_data, sheet_name=sheet_name, engine='openpyxl')
                   for sheet_name in excel_data.sheet_names}
    return sheets_dict

def filter_and_group_data(df):
    """
    Filtra las filas donde la columna 'Descripción Creada' tiene 'No' o está vacía.
    Agrupa los datos restantes por la columna 'Series' y devuelve un diccionario
    con los datos agrupados.
    """
    # Filtrar filas con "Descripción Creada" en "No" o vacío
    df_filtered = df[df['Descripción Creada'].str.lower().fillna('no').eq('no')]
    # Agrupar por "Series" y devolver el grupo de series en un diccionario
    return {series: group for series, group in df_filtered.groupby('Series')}

def mark_description_created(df, indices):
    """
    Marca las filas especificadas en `indices` de la columna 'Descripción Creada' como "Si".
    Devuelve el DataFrame actualizado.
    """
    df.loc[indices, 'Descripción Creada'] = "Si"
    return df

def save_excel_file(df_dict, output_path='updated_file.xlsx'):
    """
    Guarda un diccionario de DataFrames en un archivo Excel, creando una hoja por cada entrada.
    """
    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)