import pandas as pd
import numpy as np

NAN_PLACEHOLDER = "__NAN_PLACEHOLDER__" 
MARCA_MAP = {
    "32": "ADORE",
    "25": "AGRALBA-IVANAGRO",
    "46": "AMALIAS",
    "20": "BIOS",
    "14": "CANAMOR",
    "44": "CIPA",
    "18": "CONTEGRAL GRANDES ESPECIES",
    "19": "FINCA GRANDES ESPECIES",
    "21": "GABRICA",
    "24": "ITALCOL",
    "23": "ITALCOL GRANDES ESPECIES",
    "27": "JAULAS",
    "29": "KITTY PAW",
    "30": "LABORATORIOS ZOO",
    "36": "MAXIPETS",
    "45": "MONAMI",
    "47": "FINOTRATO",
    "26": "NUTRA NUGGETS",
    "38": "PINOMININO",
    "12": "POLAR",
    "00": "PUNTO DE VENTA-OTROS",
    "02": "PUNTO DE VENTA-OTROS",
    "1": "PUNTO DE VENTA-OTROS",
    "15": "PUNTO DE VENTA-OTROS",
    "17": "PUNTO DE VENTA-OTROS",
    "28": "PUNTO DE VENTA-OTROS",
    "35": "PUNTO DE VENTA-OTROS",
    "39": "PUNTO DE VENTA-OTROS",
    "CR": "PUNTO DE VENTA-OTROS",
    "10": "PUNTOMERCA",
    "37": "PANDAPAN",
    "40": "PURINA",
    "41": "SEMILLAS",
    "42": "SOLLA",
    "43": "SOLLA MASCOTAS",
    "34": "TETRACOLOR",
}


############ Código de producto negado - para importación masiva #######################################

def limpiar_y_preparar_detalle(datos_recibidos):
    
    df = pd.DataFrame(datos_recibidos)
    df = df.replace(NAN_PLACEHOLDER, np.nan) 

    # Rellenar valores faltantes
    data = df.fillna(method="ffill").fillna(method="bfill")

    # Fecha normalizada
    if "Fecha Programada" in data.columns:
        data["Fecha"] = pd.to_datetime(
            data["Fecha Programada"], errors="coerce"
        ).dt.date
    else:
        # Si no hay columna, poner fecha de hoy
        data["Fecha"] = pd.Timestamp.today().date()

    # Calcular producto negado
    data["Producto negado"] = data.get(
        "Movimientos de Existencias/Cantidad Real", 0
    ) - data.get("Movimientos de Existencias/Cantidad Reservada", 0)

    # Extraer marca
    if "Movimientos de Existencias/Descripción" in data.columns:
        data["marca"] = data["Movimientos de Existencias/Descripción"].str.slice(1, 3)
        data["marca"] = data["marca"].replace(MARCA_MAP)
    else:
        data["marca"] = "OTROS"

    # Filas necesarias para guardar
    detalle = data[
        [
            "Fecha",
            "Movimientos de Existencias/Descripción",
            "Producto negado",
            "marca",
            "Documento Origen",
            "Referencia",
        ]
    ].copy()

    detalle = detalle.rename(
        columns={
            "Fecha": "fecha",
            "Movimientos de Existencias/Descripción": "producto",
            "Producto negado": "cantidad_negada",
            "Documento Origen": "origen",
            "Referencia": "referencia",
        }
    )

    # Filtramos solo los registros con cantidad_negada > 0
    detalle = detalle[detalle["cantidad_negada"] > 0]

    return detalle



############ Código de picking and packing #######################################

############ Transformaciones ##############


#### Esta función me permite dividir la estructura la columna

def dividir_zona(zona):

    if pd.isna(zona):  # Maneja valores NaN (Not a Number) o None si los hubiera
        return [None, None]
    try:
        partes = str(zona).split(".", 1)  # Divide solo por el primer punto
        if len(partes) == 1:
            return [
                partes[0],
                None,
            ]  # Si no hay punto, 'Cod zona' es la zona, 'zona' es None
        else:
            return partes
    except:
        return [None, None]  # En caso de cualquier otro error, devuelve [None, None]

#### Esta función me permite completar datos nulos en zona
def zona_blanco(row):
    # Verificar si 'codigoZona' es nulo o igual al string 'nan'
    if pd.isna(row["codigoZona"]) or str(row["codigoZona"]).lower() == "nan":
        row["codigoZona"] = row["cuidad"]
    # Verificar si 'zona' es nulo o igual al string 'nan'
    if pd.isna(row["zona"]) or str(row["zona"]).lower() == "nan":
        row["zona"] = row["cuidad"]
    return row

def quitar_tildes(texto):
    """Reemplaza vocales acentuadas y eñes por sus equivalentes sin acento."""
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    for acentuada, normal in reemplazos.items():
        # Asegúrate de trabajar con strings para evitar errores
        if isinstance(texto, str):
            texto = texto.replace(acentuada, normal)
    return texto

# --- Constantes ---
# Este diccionario DEBE estar fuera de la función.
COLUMNAS_FINALES_MAPEO = {
    # Claves SIN tildes (gracias a quitar_tildes) : Valores (Nombres del Modelo de Django)
    "nombre_de_la_empresa_a_mostrar_en_la_factura": "nombreAsociado",
    "fecha_de_factura_recibo": "fechaFactura",
    "asociado_documento_de_identificacion": "identificacionAsociado",
    "vendedor": "vendedor",
    "lineas_de_factura_cantidad": "cantidad",
    "lineas_de_factura_producto": "producto",
    "lineas_de_factura_producto_peso": "pesoUnitario",
    "asociado_ciudad": "cuidad", 
    "asociado_zona": "zonaAsociadoOriginal", # Columna temporal para procesamiento
    "origen": "origen",
    "id": "idOdoo",
    "movimientos_de_existencias_descripcion": "descripcionExistencias", 
    "nombrecorte" : "nombrecorte"
}

# --------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# --------------------------------------------------------------------------

def pickingPacking(data_or_path) -> pd.DataFrame:
    """Limpia y transforma los datos, estandarizando nombres de columnas para Django."""
    
    # ----------------------------------------------------
    # 1. Lógica de Carga Inicial
    # ----------------------------------------------------
    if isinstance(data_or_path, pd.DataFrame):
        pick = data_or_path.copy()
    else:
        try:
            # Entrada de JSON desde DRF (lista de dicts)
            pick = pd.DataFrame(data_or_path) 
        except Exception:
            # Caso de fallback (si no es JSON, asume ruta de archivo)
            pick = pd.read_excel(data_or_path)

    pickzona = pick.copy()

    # ----------------------------------------------------
    # 2. Normalización de Nombres de Columnas (¡CORREGIDO: Tildes, / y espacios!)
    # ----------------------------------------------------
    pickzona.columns = pickzona.columns.str.strip()
    
    # Paso 1: Quitar tildes (soluciona 'líneas' -> 'lineas', etc.)
    pickzona.columns = pickzona.columns.map(quitar_tildes) 
    
    # Paso 2: Reemplazar caracteres especiales y espacios
    pickzona.columns = pickzona.columns.str.replace('/', '_', regex=False)
    pickzona.columns = pickzona.columns.str.replace(r'[\s]+', '_', regex=True)
    
    # Paso 3: Todo a minúsculas
    pickzona.columns = pickzona.columns.str.lower()
    
    # ----------------------------------------------------
    # 3. Renombrado y Selección
    # ----------------------------------------------------
    # Renombra el DF usando el mapeo (Nombres limpios -> Nombres del Modelo)
    pickzona.rename(columns=COLUMNAS_FINALES_MAPEO, inplace=True)
    
    # Selecciona solo las columnas que se renombraron y existen en el DF
    columnas_base_modelo = [
        col for col in COLUMNAS_FINALES_MAPEO.values() 
        if col in pickzona.columns
    ]
    pickzona = pickzona[columnas_base_modelo]

    # ----------------------------------------------------
    # 4. Lógica de Transformación
    # ----------------------------------------------------
    
    # Crea las nuevas columnas temporales ('Cod zona' y 'zona')
    # Nota: El nombre 'zonaAsociadoOriginal' es el renombrado final de 'asociado_zona'
    pickzona[["Cod zona", "zona"]] = (
        pickzona["zonaAsociadoOriginal"]
        .apply(dividir_zona)
        .apply(pd.Series)
    )

    # Renombra 'Cod zona' a 'codigoZona' (¡Fija el KeyError de 'Cod zona'!)
    pickzona.rename(columns={"Cod zona": "codigoZona"}, inplace=True)

    # El campo 'zonaAsociadoOriginal' ya no es necesario
    del pickzona["zonaAsociadoOriginal"]

    # Aplicar la función de relleno de zona
    # (Asume que zona_blanco usa los nombres finales 'codigoZona' y 'cuidad')
    pickzona = pickzona.apply(zona_blanco, axis=1)

    # Rellenar valores faltantes (usando el método moderno)
    pickzona = pickzona.ffill()

    # Extraer marca
    if "producto" in pickzona.columns:
        pickzona["marca"] = pickzona["producto"].str.slice(1, 3)
        pickzona["marca"] = pickzona["marca"].replace(MARCA_MAP)
        
    else:
        pickzona["marca"] = "OTROS"
        
    # ----------------------------------------------------
    # 5. Selección Final y Orden del Modelo
    # ----------------------------------------------------
    
    # Esta es la lista FINAL de campos que espera tu modelo de Django
    columnas_modelo_final_orden = [
        "nombreAsociado", "fechaFactura", "identificacionAsociado", "vendedor",
        "cantidad", "producto", "pesoUnitario", "cuidad", 
        "codigoZona", "zona", "origen", "marca", "idOdoo", "nombrecorte" 
    ]
    
    pickzona = pickzona[columnas_modelo_final_orden]
    
    return pickzona