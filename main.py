import os
#import platform
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

print('\nDirectorio actual: '+os.getcwd()+'\n')

# Ruta origenes plantillas de prueba:
ruta_prueba=f'./.venv/pruebas/origenes/plantilla_descripciones.html'
with open(ruta_prueba, 'r', encoding='utf-8') as archivoHtml:
    html_bruto=archivoHtml.read()
##################################################################################################################
"""
if platform.system()=='Windows':
    ruta_excel=os.path.join(os.path.expanduser("~"), "Documents", "./venv/tu_archivo.xlsx")  # Cambia "tu_archivo.xlsx"
elif platform.system()=='Linux' or platform.system()=='Darwin':  # Darwin es para MacOS
    ruta_excel=os.path.join(os.path.expanduser("~"), "Documentos", "./venv/tu_archivo.xlsx")  # Cambia "tu_archivo.xlsx"
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
marcoDatos=pd.read_excel(ruta_prueba, sheet_name='Nombre_de_la_hoja', engine='openpyxl')

# Inicializar el índice de la fila del marco de datos de Panda
i_fila_mD=0

# Iterar hasta que la celda de la primera columna esté vacía
while not pd.isna(marcoDatos.iloc[i_fila_mD, 0]) and marcoDatos.iloc[i_fila_mD, 0] != '':
# Obtener y convertir los datos de la fila en una lista
    lista_datos=marcoDatos.iloc[i_fila_mD].tolist()
    
# Mostrar los datos de la lista (o hacer lo que necesites con la lista)
    print(f"Fila {i_fila_mD+1}: {lista_datos}")
    
# Incrementar el índice de la fila para pasar a la siguiente
    i_fila_mD+=1
"""
##################################################################################################################
# HTML de plantilla hardcodeado ¡¡¡ NO ELIMINAR!!!
"""
html_bruto='''<div style="font-family: 'Times New Roman';">
    <img
      src="https://staging.materialelectricoyclimatizacion.com/img/cms/logos/sinclair-logo-2024.png"
      alt=""
      width="164"
      height="36"
      class="img-thumbnail"
    /><br/>
    <h2>
      <strong><span id="modelo">&lt;modelo&gt;</span> - <span id="probeedor">SINCLAIR</span></strong>
    </h2>
    <div style="padding-left: 30px">
        <p>
          -Unidad interior - medio agua.<br/>
          -Alta eficiencia del intercambiador de calor.<br/>
          -Bandeja de condensado en forma de V más larga.<br/>
          -Motor del ventilador de CC económico.<br/>
          -Posibilidad de conectar el mando central <strong>SCM-30.</strong><br/>
          -Soporta MODBUS RTU.</span><br/>
          -Mando mural <strong>SWC-61</strong> opcional.<br/>
          -El <strong>SF2-DTK</strong> soporta opcionalmente control a la tensión de <strong>230 V</strong>:<strong>velocidad alta, media y baja.</strong><br/>
          -Opcionalmente, SF2-EC apoya el control del ventilador mediante una tensión de 0 a 10 V (requiere SF2-DTK).<br/>
          -Recomendamos conectar una válvula NC 230 V externa de 3 o 2 vías.
        </p>
    </div>
    <br/>
    <div id="accesorios">
        <h2>
            Accesorios:
        </h2>
        <div id="elementos_accesorios" style="padding-left: 30px">
            <span>Mando mural - <strong>SWC-61</strong></span><br/>
            <span>Mando mural central por cable - <strong>SCM-30</strong></span>
        </div>
    </div>
    <h2><span>Características:</span></h2>
    <div class="listado_variables" style="padding-left: 30px">
        <strong>Enfriamiento</strong>(kW): <span id="potfri"></span><br/>
        <strong>Calentamiento</strong>(kW): <span id="potcal"></span><br/>
        <strong>Dimensiones</strong>(mm): <span id="dim"></span><br/>
        <strong>Peso bruto</strong>(Kg): <span id="peso"></span>
    </div>
</div>'''
"""
##################################################################################################################
# Cargar el HTML en BeautifulSoup
html_procesado=BeautifulSoup(html_bruto, 'html.parser')

# Pedir al usuario que introduzca nuevos valores para los campos
nuevo_modelo=input('¿Cual es el modelo de la maquina?: ')
nuevo_potfri=input('Introduce la nueva potencia de enfriamiento (ej. 3,00): ')
nuevo_potcal=input('Introduce la nueva potencia de calentamiento (ej. 3,50): ')
dim_anch=input('Introduzca la anchura (ej. 700): ')
dim_alt=input('Introduzca la altura (ej. 250): ')
dim_long=input('Introduzca la longitud (ej. 500): ')
nuevo_peso=input('Introduce el nuevo peso (ej. 18,0): ')

# Preguntar si tiene accesorios
tiene_accesorios=input("¿Tiene accesorios? (sí/no): ").strip().lower()

# Si la respuesta es 'no', eliminar la sección de accesorios
if tiene_accesorios in ['sí', 'si', 's']:
# Mantener la sección de accesorios
    pass
else:
# Eliminar la sección de accesorios
    accesorios=html_procesado.find(id="accesorios")
    if accesorios:
        accesorios.decompose()

# Buscar los elementos por su ID y actualizar su contenido
html_procesado.find(id='modelo').string=f'SF2-{nuevo_modelo}D3'
html_procesado.find(id='potfri').string=nuevo_potfri.replace(".", ",")
html_procesado.find(id='potcal').string=nuevo_potcal.replace(".", ",")
html_procesado.find(id='dim').string=f'{dim_anch} x {dim_alt} x {dim_long}'
html_procesado.find(id='peso').string=nuevo_peso.replace(".", ",")
##################################################################################################################
"""
# Determinar el sistema operativo y establecer la ruta
sistema_operativo=platform.system()
if sistema_operativo=='Windows':
    ruta_salidas_pruebas=os.path.join(os.path.expanduser("~"), "Documents")
elif sistema_operativo=='Linux' or sistema_operativo=='Darwin':  # Darwin es para MacOS
    ruta_salidas_pruebas=os.path.join(os.path.expanduser("~"), "Documentos")
else:
    raise Exception("Sistema operativo no soportado")

if not os.path.exists(os.path.join(ruta_salidas_pruebas, "salidas")):
    os.makedirs(os.path.join(ruta_salidas_pruebas, "salidas"))
"""
##################################################################################################################
ruta_salidas_pruebas='./.venv/pruebas/salidas'
fecha_hora=datetime.now().strftime("%Y-%m-%d_%H:%M:%S")  # Formato: YYYYMMDD_HHMMSS

# Crear el nombre del archivo
nombre_archivo=f'descripción-{html_procesado.find(id="modelo").string.replace("<", ":-::").replace(">", "::-:").replace("/", "_")}-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.html'

with open(os.path.join(ruta_salidas_pruebas, nombre_archivo), 'w') as archivoHtml:
    archivoHtml.write(str(html_procesado))