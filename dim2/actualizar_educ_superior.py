# actualizar_educ_superior.py — Dimensión 2: Educación Superior
# Script para procesar el CSV del MEN (datos.gov.co) y generar
# el JSON de matrículas en educación superior.
#
# Uso:
#   1. Descargar el CSV de:
#      https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS-MATRICULA-POR-MUNICIPIOS_ES/y9ga-zwzy/about_data
#
#   2. Guardar el archivo en dim2/fuentes/Educ superior/
#
#   3. Correr este script:
#      python dim2/actualizar_educ_superior.py
#
#   4. Los archivos JSON en dim2/data/ se actualizan automáticamente.

import os
import csv
import json

# ============================================================
# Configuración
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FUENTES_DIR = os.path.join(SCRIPT_DIR, 'fuentes', 'Educ superior')
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

# Niveles de formación en el CSV
NIVELES = [
    'TECNICA PROFESIONAL',
    'TECNOLOGICA',
    'UNIVERSITARIA',
    'ESPECIALIZACION',
    'MAESTRIA',
    'DOCTORADO',
]

# Nombres amigables para el JSON
NOMBRES = {
    'TECNICA PROFESIONAL': 'tecnica_profesional',
    'TECNOLOGICA': 'tecnologica',
    'UNIVERSITARIA': 'universitaria',
    'ESPECIALIZACION': 'especializacion',
    'MAESTRIA': 'maestria',
    'DOCTORADO': 'doctorado',
}


# ============================================================
# Funciones
# ============================================================

def encontrar_archivo_csv(carpeta):
    """Busca el archivo CSV más reciente en la carpeta."""
    if not os.path.exists(carpeta):
        print(f'ERROR: No existe la carpeta {carpeta}')
        return None
    archivos = [f for f in os.listdir(carpeta)
                if f.endswith('.csv') and not f.startswith('~$')]
    if not archivos:
        print(f'ERROR: No se encontró ningún archivo CSV en {carpeta}')
        return None
    archivos.sort()
    return os.path.join(carpeta, archivos[-1])


def parsear_numero(valor):
    """Convierte un string con formato colombiano ('63.098' o '129.516,5') a float."""
    if not valor or valor.strip() == '':
        return 0.0
    # Quitar comillas y espacios
    valor = valor.strip().strip('"')
    # Formato colombiano: puntos son miles, coma es decimal
    valor = valor.replace('.', '').replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return 0.0


def es_bogota(municipio):
    """Detecta si la fila corresponde a Bogotá."""
    return 'BOGOT' in municipio.upper()


def extraer_datos(ruta_csv):
    """Lee el CSV y extrae matrículas por nivel para Bogotá y Colombia."""
    bogota = {}
    colombia = {}
    seen = set()

    with open(ruta_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            anio = row.get('AÑO', '').strip().strip('"')
            cod_mun = row.get('Código delMunicipio', '').strip().strip('"')
            municipio = row.get('Nombre del Municipio', '')

            if not anio.isdigit():
                continue
            anio = int(anio)

            # Deduplicar por año + código de municipio
            # (el CSV tiene filas duplicadas con variantes del nombre)
            key = (anio, cod_mun)
            if key in seen:
                continue
            seen.add(key)

            # Extraer valores por nivel
            vals = {}
            for nivel in NIVELES:
                vals[nivel] = parsear_numero(row.get(nivel, '0'))
            total = sum(vals.values())

            # Acumular totales Colombia
            if anio not in colombia:
                colombia[anio] = {n: 0.0 for n in NIVELES}
                colombia[anio]['total'] = 0.0
            for n in NIVELES:
                colombia[anio][n] += vals[n]
            colombia[anio]['total'] += total

            # Guardar Bogotá
            if es_bogota(municipio):
                bogota[anio] = {NOMBRES[n]: vals[n] for n in NIVELES}
                bogota[anio]['total'] = total
                ies = row.get('IES CON OFERTA', '0')
                bogota[anio]['ies_con_oferta'] = int(parsear_numero(ies))

    return bogota, colombia


def generar_json(bogota, colombia):
    """Genera los archivos JSON para el tablero web."""
    os.makedirs(DATA_DIR, exist_ok=True)
    anios = sorted(bogota.keys())

    # JSON principal: Bogotá con detalle por nivel + comparación Colombia
    registros = []
    for anio in anios:
        bg = bogota[anio]
        col = colombia.get(anio, {})
        registro = {
            'anio': anio,
            'tecnica_profesional': bg['tecnica_profesional'],
            'tecnologica': bg['tecnologica'],
            'universitaria': bg['universitaria'],
            'especializacion': bg['especializacion'],
            'maestria': bg['maestria'],
            'doctorado': bg['doctorado'],
            'total_bogota': bg['total'],
            'total_colombia': col.get('total', 0),
            'ies_con_oferta': bg.get('ies_con_oferta', 0),
        }
        # Porcentaje de Bogotá sobre Colombia
        if col.get('total', 0) > 0:
            registro['pct_bogota'] = round(bg['total'] / col['total'] * 100, 1)
        else:
            registro['pct_bogota'] = None
        registros.append(registro)

    ruta = os.path.join(DATA_DIR, 'educacion_superior.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    print(f'  educacion_superior.json: {len(registros)} años')

    return ruta


def main():
    print('=' * 60)
    print('Actualización de datos — Dimensión 2: Educación Superior')
    print('=' * 60)

    print(f'\nBuscando archivo CSV en: {FUENTES_DIR}')
    archivo = encontrar_archivo_csv(FUENTES_DIR)
    if not archivo:
        return
    print(f'  Archivo: {os.path.basename(archivo)}')

    print('\nLeyendo datos del MEN...')
    bogota, colombia = extraer_datos(archivo)
    print(f'  {len(bogota)} años con datos de Bogotá')

    if not bogota:
        print('ERROR: No se encontraron datos de Bogotá en el archivo.')
        return

    print('\nGenerando archivo JSON...')
    ruta = generar_json(bogota, colombia)

    # Verificación rápida
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    ultimo = datos[-1] if datos else None
    if ultimo:
        print(f'\n{"=" * 60}')
        print(f'VERIFICACIÓN — Año {ultimo["anio"]}:')
        print(f'{"=" * 60}')
        for clave, nombre in [('universitaria', 'Universitaria'),
                               ('tecnologica', 'Tecnológica'),
                               ('tecnica_profesional', 'Técnica profesional'),
                               ('especializacion', 'Especialización'),
                               ('maestria', 'Maestría'),
                               ('doctorado', 'Doctorado')]:
            val = ultimo.get(clave, 0)
            print(f'  {nombre}: {val:,.0f}'.replace(',', '.'))
        print(f'  ---')
        print(f'  Total Bogotá: {ultimo["total_bogota"]:,.0f}'.replace(',', '.'))
        print(f'  Total Colombia: {ultimo["total_colombia"]:,.0f}'.replace(',', '.'))
        print(f'  Participación Bogotá: {ultimo.get("pct_bogota", 0):.1f} %'.replace('.', ','))
        print(f'  IES con oferta: {ultimo.get("ies_con_oferta", 0)}')

    anios = [d['anio'] for d in datos]
    print(f'\nAños disponibles: {min(anios)} – {max(anios)}')
    print(f'\nArchivo actualizado:')
    print(f'  - {ruta}')
    print(f'\nEl tablero web se actualizará automáticamente al hacer push.')


if __name__ == '__main__':
    main()
