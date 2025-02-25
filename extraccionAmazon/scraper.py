from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import re


def iniciar_driver():
    options = Options()
    options.set_preference("intl.accept_languages", "es-ES,es")

    driver = webdriver.Firefox(options=options)
    driver.get("https://www.amazon.com/")
    return driver

def buscar_en_amazon(termino_busqueda):
    driver = iniciar_driver()
    url = f"https://www.amazon.com/s?k={termino_busqueda}"
    driver.get(url)

    # Extraer cantidad de resultados
    resultados = driver.find_element(By.XPATH, '//div[@class="sg-col-inner"]/h2[@class="a-size-base a-spacing-small a-spacing-top-small a-text-normal"]' ).text
    print(resultados)
    match = re.search(r'de\s+([\d+]+)\s+resultados', resultados)
    if match:
        total_resultados = match.group(1)
        total_resultados = int(total_resultados)
    else:
        total_resultados = 0


    #Extraer total de paginas
    try:
        paginas = driver.find_element(By.XPATH, '//span[@class="s-pagination-item s-pagination-disabled"]')
        no_paginas = paginas.text
    except NoSuchElementException:
        try:
            paginas = driver.find_elements(By.XPATH, '//li[@class="s-list-item-margin-right-adjustment"]')
            no_paginas = None  
            contador = 0 
            for pagina in paginas:
                if contador == len(paginas) -2:
                    no_paginas = pagina.text.strip()
                    break
                contador += 1
        except:
            no_paginas = "No se encontraron paginas"

    total_paginas = int(no_paginas)
    print(f"Se encontraron {total_paginas} páginas, espera unos segundos mientras procesa los productos de cada página...")
    print("...")
    return driver,total_resultados, total_paginas


# Extraccion de las caracteristicas de los productos
def extraer_productos(driver, termino_busqueda, total_paginas):
    productos = []
    total_paginas = int(total_paginas)

    for pagina in range(1,total_paginas+1):
        url = f"https://www.amazon.com/s?k={termino_busqueda}&page={pagina}"
        driver.get(url)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]'))
            )
        except TimeoutException:
            print(f"No hay productos en la página {pagina}. Saltando a la siguiente...")
            continue  # Pasa a la siguiente página

        elementos = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        
        if not elementos:
            print(f"No se encontraron productos en la página {pagina}. Finalizando...")
            break  # Si ya no hay productos en esta página, salimos del bucle principal
        
        for elemento in driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]'):
            try:
                #Nombre del elemento
                try:
                    nombre = elemento.find_element(By.XPATH, './/h2[@class="a-size-base-plus a-spacing-none a-color-base a-text-normal"]').text
                   
                except NoSuchElementException:
                    try:
                         nombre = elemento.find_element(By.XPATH, './/h2[@class="a-size-medium a-spacing-none a-color-base a-text-normal"]').text
                    except NoSuchElementException:
                        nombre = "Sin nombre"

                #Calificación
                try:
                    calificacion = driver.execute_script("return arguments[0].textContent;", elemento.find_element(By.XPATH, './/span[@class="a-icon-alt"]'))
                except NoSuchElementException:
                    calificacion = "Sin calificación"

                #Precio
                try:
                    precio_entero = elemento.find_element(By.XPATH, './/span[@class="a-price-whole"]').text
                    precio_entero = precio_entero.replace(',', '')
                    try:
                        precio_decimal = elemento.find_element(By.XPATH, './/span[@class="a-price-fraction"]').text
                    except NoSuchElementException:
                        precio_decimal = "00"

                    precio = float(f"{precio_entero}.{precio_decimal}")
                except NoSuchElementException:  
                    precio = 0  

                #Descuento
                try:
                    buscar_original = elemento.find_element(By.XPATH, './/div[@class="a-section aok-inline-block"]').text
                    precio_encontrado = re.search(r"[\d,.]+", buscar_original)
                    if precio_encontrado is not None:  # Verifica si se encontró un valor válido
                        precio_normal = precio_encontrado.group().replace(",", "").strip()  
                        try:
                            precio_normal = float(precio_normal)  
                        except ValueError:
                            precio_normal = 0
                        if precio_normal > 0:
                            descuento = round(((precio_normal - precio) / precio_normal) * 100)
                        else:
                            descuento = 0
                    else:
                        descuento = 0
                except (NoSuchElementException, TimeoutException):
                    descuento = 0

                #Patrocinio
                patrocinado = "Patrocinado" if "Patrocinado" in elemento.text else "General"

                # Guardar producto en la lista
                productos.append({
                    "nombre": nombre,
                    "calificacion": calificacion,
                    "precio": precio,
                    "descuento": descuento,
                    "observacion": patrocinado
                })

            except StaleElementReferenceException:
                print("Se encontró un elemento obsoleto, volviendo a buscar...")
                continue  

        print(f"Página {pagina} procesada ({len(productos)} productos acumulados)")

    driver.quit()
    return productos
            