import pandas as pd
def cargar_excel(nombre_archivo):
    return pd.read_excel(nombre_archivo, sheet_name= None)

def ajustar_precios(df):
    df["precio"] = df["precio"].apply(lambda x: round(x) if (x % 1) >= 0.5 else int(x))
    return df

def calcular_precio_inicial(df):
    df["precio_Inicial"] = df.apply(lambda row: round(row["precio"] / (1-row["descuento"] / 100)) if row["descuento"] > 0 else row["precio"], axis= 1)
    return df

def filtrar_productos(df,termino_busqueda):
    df = df[df["nombre"].str.contains(termino_busqueda, case=False, na=False)]
    return df

def actualizar_excel(nombre_archivo, termino_busqueda):
    print(f"Actualizando archivo Excel...")
    print("...")
    hojas = cargar_excel(nombre_archivo)
    with pd.ExcelWriter(nombre_archivo, engine="openpyxl", mode="w") as writer:
        for nombre_hoja, df in hojas.items():
            df = ajustar_precios(df)
            df = calcular_precio_inicial(df)
            df = filtrar_productos(df, termino_busqueda)
            
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)
    print("Archivo Excel actualizado con éxito:")
    print(f"Ruta del archivo: ({nombre_archivo})")
    print("")
        
