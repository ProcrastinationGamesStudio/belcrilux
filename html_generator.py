""""""
from bs4 import BeautifulSoup

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
""""""