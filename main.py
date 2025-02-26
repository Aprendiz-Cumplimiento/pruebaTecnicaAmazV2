import os
from extraccionAmazon.scraper import buscar_en_amazon, extraer_productos
from guardarDatos.guardar_datos import guardar_json, guardar_en_excel
from actualizar_excel.procesar_datos import actualizar_excel

def main():
    # Definir ruta relativa de trabajo de la Automatización
    path_root = os.path.dirname(os.path.abspath(__file__))

    termino_busqueda = "carro"#input("Ingrese el producto de su preferencia para buscar: ")

    #Extracción de información requerida de Amazon
    driver, total_resultados, total_paginas = buscar_en_amazon(termino_busqueda)
    productos = extraer_productos(driver,termino_busqueda, total_paginas)

    #Datos guardados en formato Json y Excel.
    guardar_json(productos, "productosAmazon-")
    nombre_archivo = guardar_en_excel(productos, total_paginas, path_root)

    #Hacer actualizacion de Excel
    actualizar_excel(nombre_archivo, termino_busqueda)


main()