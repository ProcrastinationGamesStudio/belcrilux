import os
import platform
#import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

#print('\nDirectorio actual: '+os.getcwd()+'\n')

# Ruta origenes plantillas de prueba:
ruta_prueba=f'./.venv/pruebas/origenes/plantilla_descripciones-sf-xxxxD3.html'
with open(ruta_prueba,'r',encoding='utf-8') as archivoHtml:
    html_bruto=archivoHtml.read()
##################################################################################################################
"""
if platform.system()=='Windows':
    ruta_excel=os.path.join(os.path.expanduser("~"),"Documents","./venv/tu_archivo.xlsx")  # Cambia "tu_archivo.xlsx"
elif platform.system()=='Linux' or platform.system()=='Darwin':  # Darwin es para MacOS
    ruta_excel=os.path.join(os.path.expanduser("~"),"Documentos","./venv/tu_archivo.xlsx")  # Cambia "tu_archivo.xlsx"
else:
    raise Exception("Sistema operativo no soportado")
"""
##################################################################################################################
# Codigo para excel: EN DESARROLLO
"""
ruta_prueba=f'./.venv/pruebas/origenes/plantilla_descripciones'
# Comprobar la extensión del archivo
if os.path.exists(ruta_prueba+'.xlsx'):
    ruta_prueba=ruta_prueba+'.xlsx'
elif os.path.exists(ruta_prueba+'.xlsm'):
    ruta_prueba=ruta_prueba+'.xlsm'
else:
    raise Exception("El archivo no es un archivo Excel válido (.xlsx o .xlsm)")

# Leer el archivo Excel usando un DataFrame (Marco de Datos) de Pandas
marcoDatos=pd.read_excel(ruta_prueba,sheet_name='Nombre_de_la_hoja',engine='openpyxl')

# Inicializar el índice de la fila del marco de datos de Panda
i_fila_mD=0

# Iterar hasta que la celda de la primera columna esté vacía
while not pd.isna(marcoDatos.iloc[i_fila_mD,0]) and marcoDatos.iloc[i_fila_mD,0] != '':
# Obtener y convertir los datos de la fila en una lista
    lista_datos=marcoDatos.iloc[i_fila_mD].tolist()
    
# Mostrar los datos de la lista (o hacer lo que necesites con la lista)
    print(f"Fila {i_fila_mD+1}: {lista_datos}")
    
# Incrementar el índice de la fila para pasar a la siguiente
    i_fila_mD+=1
"""
##################################################################################################################
# HTML de plantilla hardcodeado ¡¡¡NO ELIMINAR!!!
"""
html_bruto='''<div style="font-family: 'Times New Roman';">
    <img alt="" class="img-rounded" height="50" src="https://staging.materialelectricoyclimatizacion.com/img/cms/logos/sinclair-logo-2024.png" width="235" /><br/><br/>

    <h2><strong><span id="modelo"></span> - <span id="probeedor"></span></strong></h2>
    <div id="curiosidades" style="padding-left: 30px">
        - <span id="curiosidad_x"><!--Caracteristica (La x del id se sustituye por un numero,empezando por 1)--></span><br/>
    </div><br/>
    <div id="accesorios">
        <h2>Accesorios:</h2>
        <div id="elementos_accesorios" style="padding-left: 30px">
            <span><!--Tipo de accesorio--><strong><!--Modelo del accesorio--></strong></span>
        </div>
    </div><br/>
    <h2><span>Características:</span></h2>
    <div class="listado_variables" style="padding-left: 30px">
        <strong>Enfriamiento </strong>(kW): <span id="potfri"></span><br/>
        <strong>Calentamiento </strong>(kW): <span id="potcal"></span><br/>
        <strong>Dimensiones </strong>(mm [An x Al x Pr]): <span id="dim"></span><br/>
        <strong>Peso bruto </strong>(Kg): <span id="peso"></span>
    </div>
</div>'''
"""
##################################################################################################################
# Cargar el HTML en BeautifulSoup
html_procesado=BeautifulSoup(html_bruto,'html.parser')

# Pedir al usuario que introduzca nuevos valores para los campos
nuevo_modelo=input('¿Cual es el modelo de la maquina?: ')
nuevo_probeedor=input('¿Cual es el probeedor de la maquina?: ').strip().lower()
nuevo_potfri=input('Introduce la nueva potencia de enfriamiento (ej. 3,00): ')
nuevo_potcal=input('Introduce la nueva potencia de calentamiento (ej. 3,50): ')
dim_anch=input('Introduzca la anchura (ej. 700): ')
dim_alt=input('Introduzca la altura (ej. 250): ')
dim_long=input('Introduzca la longitud (ej. 500): ')
nuevo_peso=input('Introduce el nuevo peso (ej. 18,0): ')

# Preguntar cuántas curiosidades tiene
num_curiosidades=int(input("¿Cuántas curiosidades tiene el producto?: "))

# Buscar el contenedor de curiosidades
contenedor_curiosidades=html_procesado.find(id="curiosidades")

# Eliminar el ejemplo que estaba en la plantilla
contenedor_curiosidades.clear()

# Añadir las curiosidades que haya indicado el usuario
for i in range(0,num_curiosidades):
    curiosidad=input(f"Introduce la curiosidad {i+1}/{num_curiosidades}: ")
    nuevo_elemento=html_procesado.new_tag('span')
    nuevo_elemento.string=f"- {curiosidad}"
    if i<num_curiosidades:
        contenedor_curiosidades.append(html_procesado.new_tag('br'))

    contenedor_curiosidades.append(html_procesado.new_string("\n"))
    contenedor_curiosidades.append(nuevo_elemento)

# Preguntar si tiene accesorios
tiene_accesorios=input("¿Tiene accesorios? (sí/no): ").strip().lower()

# Si la respuesta es 'no',eliminar la sección de accesorios
if tiene_accesorios in ['sí','si','s']:
# Preguntar cuántos accesorios tiene
    num_accesorios=int(input("¿Cuántos accesorios tiene el producto?: "))

# Buscar el contenedor de accesorios
    contenedor_accesorios=html_procesado.find(id="elementos_accesorios")

# Limpiar el contenedor para añadir los accesorios del usuario
    contenedor_accesorios.clear()

# Añadir los accesorios que haya indicado el usuario
    for i in range(0,num_accesorios):
        tipo_accesorio=input(f"Introduce el tipo del accesorio {i+1}/{num_accesorios}: ")
        modelo_accesorio=input(f"Introduce el modelo del accesorio {i+1}/{num_accesorios}: ")

    # Crear el span para el tipo de accesorio
        nuevo_accesorio=html_procesado.new_tag('span')
        nuevo_accesorio.string=f"{tipo_accesorio} - "

    # Crear el strong para el modelo del accesorio
        strong_modelo=html_procesado.new_tag('strong')
        strong_modelo.string=modelo_accesorio

    # Añadir el strong dentro del span
        nuevo_accesorio.append(strong_modelo)

    # Si no es el último accesorio, añadir un <br> y un salto de línea
        if i<num_accesorios:
            contenedor_curiosidades.append(html_procesado.new_tag('br'))

        contenedor_accesorios.append(html_procesado.new_string("\n"))
        contenedor_accesorios.append(nuevo_accesorio)
elif tiene_accesorios not in ['no', 'n']:
    # Mensaje solo para el else, en caso de opción no válida
    print("No es una opción válida, por defecto se elegirá 'No'")

# Código común que se ejecuta tanto en elif como en else
if tiene_accesorios not in ['sí','si','s']:
    accesorios=html_procesado.find(id="accesorios")
    if accesorios:
        accesorios.decompose()

# Buscar los elementos por su ID y actualizar su contenido
html_procesado.find(id='modelo').string=f'{nuevo_modelo}'
html_procesado.find(id='probeedor').string=nuevo_probeedor.strip().upper()
html_procesado.find(id='potfri').string=nuevo_potfri.replace(".",",")
html_procesado.find(id='potcal').string=nuevo_potcal.replace(".",",")
html_procesado.find(id='dim').string=f'{dim_anch} x {dim_alt} x {dim_long}'
html_procesado.find(id='peso').string=nuevo_peso.replace(".",",")
##################################################################################################################

# Determinar el sistema operativo y establecer la ruta
sistema_operativo=platform.system()

ruta_salidas_pruebas=os.path.join("./.venv/","pruebas")

if not os.path.exists(os.path.join(ruta_salidas_pruebas,"salidas")):
    os.makedirs(os.path.join(ruta_salidas_pruebas,"salidas"))

ruta_salidas_pruebas=os.path.join(ruta_salidas_pruebas,"salidas")

##################################################################################################################
#ruta_salidas_pruebas='./.venv/pruebas/salidas'
fecha_hora=datetime.now().strftime("%Y-%m-%d_%H:%M:%S")  # Formato: YYYYMMDD_HHMMSS

# Crear el nombre del archivo sustituyendo caracteres no permitidos
nombre_archivo=f'descripción-{html_procesado.find(id="modelo").string.replace("<",":-::").replace(">","::-:").replace("/","_")}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'

with open(os.path.join(ruta_salidas_pruebas,nombre_archivo),'w') as archivoHtml:
    archivoHtml.write(str(html_procesado))

print("\nArchivo "+nombre_archivo+" creado en la ruta "+ruta_salidas_pruebas)