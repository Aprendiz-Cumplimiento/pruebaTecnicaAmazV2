from os.path import join
import json
import pandas as pd
from datetime import datetime

#Guardar en formato json
def guardar_json(datos, nombre_archivo):
    fecha = datetime.now().strftime("%d%m%Y")
    with open(f"{nombre_archivo}_{fecha}.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
        

#guardar en fomato excel
def guardar_en_excel(productos, total_paginas, path_root):
    df = pd.DataFrame(productos)
    print("Guardando los datos en archivo Excel...")
    path_excel = join(path_root, 'excel_creado')
    nombre_archivo = join(path_excel,"resultados_amazon.xlsx")

    registro_por_pagina = (len(productos)+ 20) // total_paginas
    df_ordenado = df.sort_values(by="precio", ascending= False)

    with pd.ExcelWriter(nombre_archivo, engine="openpyxl") as writer:
        for i in range(total_paginas):
            inicio = i *registro_por_pagina
            fin = inicio + registro_por_pagina
            df_ordenado.iloc[inicio:fin].to_excel(writer, sheet_name=f"Página {i+1}", index=False)
    print("Datos guardados con éxito")
    print("")
    return nombre_archivo
