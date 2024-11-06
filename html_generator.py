"""
import os
import traceback as trace
from bs4 import BeautifulSoup
from datetime import datetime

def generate_html_table(group):

    # Genera una tabla HTML para un grupo de datos de una serie, con formato de estilos y rowspan para valores repetidos en cada columna.
    # Devuelve la tabla HTML como un string.

    html_table = '<table style="border: 1px solid black; width: 100%;">\n'
    html_table += '<thead style="text-align: center;">\n<tr id="cabeceras" style="background-color: #f2f2f2;">\n'

    headers = ["Modelo", "Enfriamiento (kW)", "Calentamiento (kW)", "Dimensiones (mm [An x Al x Pr])", "Peso bruto (Kg)"]
    for header in headers:
        html_table += f'<th style="border: 1px solid black; width: 103px; height: 12px;"><strong>{header}</strong></th>\n'
    html_table += '</tr>\n</thead>\n<tbody style="text-align: center;">\n'

    prev_values = {}
    for _, row in group.iterrows():
        html_table += '<tr style="height: 12px;">\n'
        for col in headers:
            value = row[col] if col != "Modelo" else row["Nombre"]
            rowspan = group[col].tolist().count(value) if col != "Modelo" else 1
            if value != prev_values.get(col, None):
                td_attrs = f'style="border: 1px solid black; width: 103px; height: 12px;"'
                if rowspan > 1:
                    td_attrs += f' rowspan="{rowspan}"'
                html_table += f'<td {td_attrs}>{value}</td>\n'
                prev_values[col] = value
            else:
                html_table += ''  # Celda ya cubierta por rowspan
        html_table += '</tr>\n'
    html_table += '</tbody>\n</table>\n'
    return html_table

def insert_html_tables_into_template(html_content, series_groups):

    # Inserta las tablas HTML generadas en el div con class "listado_variables" del HTML base.
    # Devuelve el HTML modificado como objeto BeautifulSoup.

    soup = BeautifulSoup(html_content, 'html.parser')
    listado_variables_div = soup.find("div", class_="listado_variables")
    for series, group in series_groups.items():
        html_table = generate_html_table(group)
        table_soup = BeautifulSoup(html_table, 'html.parser')
        listado_variables_div.append(table_soup)
    return soup
"""
import os
import traceback as trace
from bs4 import BeautifulSoup
from datetime import datetime

RUTA_PLANTILLA= './.venv/pruebas/origenes/plantilla_descripciones.html'

def cargar_plantilla_html_sin_ruta():
    return cargar_plantilla_html(RUTA_PLANTILLA)

def cargar_plantilla_html(ruta_plantilla,mode='r+'):
    try:
        if mode not in ['r', 'w', 'rb', 'wb', 'r+', 'w+', 'rb+', 'wb+', 'leer', 'escribir', 'leerBits', 'escribirBits', 'leerEscribir', 'leerEscribirBits']:
            raise ValueError("Modo no válido. Indica si quieres leer ('r' ó 'r+', por defecto) ó escribir ('w' ó 'w+').")

        #with open(ruta_plantilla, mode, encoding='utf-8' if 'b' not in mode else None) as archivoHtml:
        if 'r' in mode:  # Si estamos leyendo
            return open(ruta_plantilla, mode, encoding="utf-8" if 'b' not in mode else None).read()
        elif 'w' in mode:  # Si estamos escribiendo
            return open(ruta_plantilla, mode, encoding="utf-8" if 'b' not in mode else None)
    except Exception as e:
        print(f"Error al cargar la plantilla: {str(e)}\n"+str(trace.print_exc()))
        return None

def generate_html_table(group):
    # Genera una tabla HTML para un grupo de datos de una serie, con formato de estilos y rowspan para valores repetidos en cada columna.
    # Devuelve la tabla HTML como un string.

    html_table = '<table style="border: 1px solid black; width: 100%;">\n'
    html_table += '<thead style="text-align: center;">\n<tr id="cabeceras" style="background-color: #f2f2f2;">\n'

    headers = ["Modelo", "Enfriamiento (kW)", "Calentamiento (kW)", "Dimensiones (mm [An x Al x Pr])", "Peso bruto (Kg)"]
    for header in headers:
        html_table += f'<th style="border: 1px solid black; width: 103px; height: 12px;"><strong>{header}</strong></th>\n'
    html_table += '</tr>\n</thead>\n<tbody style="text-align: center;">\n'

    prev_values = {}
    for _, row in group.iterrows():
        html_table += '<tr style="height: 12px;">\n'
        for col in headers:
            value = row[col]
            rowspan = group[col].tolist().count(value)
            if value != prev_values.get(col, None):
                td_attrs = f'style="border: 1px solid black; width: 103px; height: 12px;"'
                if rowspan > 1:
                    td_attrs += f' rowspan="{rowspan}"'
                html_table += f'<td {td_attrs}>{value}</td>\n'
                prev_values[col] = value
            else:
                html_table += ''  # Celda ya cubierta por rowspan
        html_table += '</tr>\n'
    html_table += '</tbody>\n</table>\n'
    return html_table

def insert_html_tables_into_template(html_content, series_groups):
    # Inserta las tablas HTML generadas en el div con class "listado_variables" del HTML base.
    # Devuelve el HTML modificado como objeto BeautifulSoup.

    soup = BeautifulSoup(html_content, 'html.parser')
    listado_variables_div = soup.find("div", class_="listado_variables")
    for series, group in series_groups.items():
        html_table = generate_html_table(group)
        table_soup = BeautifulSoup(html_table, 'html.parser')
        listado_variables_div.append(table_soup)
    return soup

def generate_and_save_html(html_template, group, provider_name, serie_name, output_path = './.venv/pruebas/salidas'):

    # Genera y guarda el HTML para una serie específica.

    html_procesado = insert_html_tables_into_template(html_template, {serie_name: group})
    html_procesado.find(id='probeedor').string = provider_name
    primer_modelo = group.iloc[0]["Modelo"]

    # Guardar HTML en el archivo
    file_name = f'descripción-{primer_modelo}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    archivo_html=cargar_plantilla_html(os.path.join(output_path, file_name), 'wb+')

    archivo_html.write((html_procesado.prettify()).encode('utf-8'))
    archivo_html.close()

    #archivo_html.write((html_procesado.prettify()).decode('utf8'))
    print(f" Archivo {file_name} creado en la ruta {output_path}")
""""""