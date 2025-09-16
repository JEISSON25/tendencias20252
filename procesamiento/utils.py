import pandas as pd

MARCA_MAP = {
    '32': "ADORE", '25': 'AGRALBA-IVANAGRO', '46': 'AMALIAS',
    '20': 'BIOS', '14': 'CANAMOR', '44': 'CIPA',
    '18': 'CONTEGRAL GRANDES ESPECIES', '19': 'FINCA GRANDES ESPECIES',
    '21': 'GABRICA', '24': 'ITALCOL', '23': 'ITALCOL GRANDES ESPECIES',
    '27': 'JAULAS', '29': 'KITTY PAW', '30': 'LABORATORIOS ZOO',
    '36': 'MAXIPETS', '45': 'MONAMI', '47': 'FINOTRATO',
    '26': 'NUTRA NUGGETS', '38': 'PINOMININO',
    '12': 'POLAR', '00': 'PUNTO DE VENTA-OTROS',
    '02': 'PUNTO DE VENTA-OTROS','1': 'PUNTO DE VENTA-OTROS',
    '15': 'PUNTO DE VENTA-OTROS','17': 'PUNTO DE VENTA-OTROS',
    '28': 'PUNTO DE VENTA-OTROS','35': 'PUNTO DE VENTA-OTROS',
    '39': 'PUNTO DE VENTA-OTROS','CR': 'PUNTO DE VENTA-OTROS',
    '10': 'PUNTOMERCA', '37': 'PANDAPAN', '40': 'PURINA',
    '41': 'SEMILLAS', '42': 'SOLLA', '43': 'SOLLA MASCOTAS',
    '34': 'TETRACOLOR'
}

def limpiar_y_preparar_detalle(path_file: str) -> pd.DataFrame:
    data = pd.read_excel(path_file)
    data = data.fillna(method='ffill')

    # Fecha normalizada
    data['Fecha'] = pd.to_datetime(data['Fecha Programada']).dt.date

    # Calcular producto negado
    data['Producto negado'] = (
        data['Movimientos de Existencias/Cantidad Real']
        - data['Movimientos de Existencias/Cantidad Reservada']
    )

    # Extraer marca
    data['marca'] = data['Movimientos de Existencias/Descripción'].str.slice(1, 3)
    data['marca'] = data['marca'].replace(MARCA_MAP)

    # Filas necesarias para guardar
    detalle = data[[
        'Fecha',
        'Movimientos de Existencias/Descripción',
        'Movimientos de Existencias/Cantidad Real',
        'Movimientos de Existencias/Cantidad Reservada',
        'Producto negado',
        'marca',
        'Documento Origen',
        'Referencia'
    ]].copy()

    return detalle
