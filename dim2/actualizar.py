# actualizar.py — Dimensión 2: Educación (Media)
# Script para procesar el CSV del MEN (datos.gov.co) y generar
# el JSON que usa la página web.
#
# Uso:
#   1. Descargar el CSV de:
#      https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/ji8i-4anb/about_data
#
#   2. Guardar el archivo en dim2/fuentes/
#
#   3. Correr este script:
#      python dim2/actualizar.py
#
#   4. Los archivos JSON en dim2/data/ se actualizan automáticamente.

import os
import csv
import json
import re

# ============================================================
# Configuración
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FUENTES_DIR = os.path.join(SCRIPT_DIR, 'fuentes')
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

# Indicadores de educación media que extraemos del CSV
INDICADORES = [
    'COBERTURA_BRUTA_MEDIA',
    'COBERTURA_NETA_MEDIA',
    'APROBACIÓN_MEDIA',
    'REPROBACIÓN_MEDIA',
    'REPITENCIA_MEDIA',
    'DESERCIÓN_MEDIA',
]

# Nombres amigables para el JSON
NOMBRES = {
    'COBERTURA_BRUTA_MEDIA': 'cobertura_bruta',
    'COBERTURA_NETA_MEDIA': 'cobertura_neta',
    'APROBACIÓN_MEDIA': 'aprobacion',
    'REPROBACIÓN_MEDIA': 'reprobacion',
    'REPITENCIA_MEDIA': 'repitencia',
    'DESERCIÓN_MEDIA': 'desercion',
}


# ============================================================
# Funciones
# ============================================================

def encontrar_archivo_csv(carpeta):
    """Busca el archivo CSV más reciente en la carpeta."""
    archivos = [f for f in os.listdir(carpeta)
                if f.endswith('.csv') and not f.startswith('~$')
                and 'MEN' in f.upper()]
    if not archivos:
        print(f'ERROR: No se encontró ningún archivo CSV del MEN en {carpeta}')
        return None
    archivos.sort()
    return os.path.join(carpeta, archivos[-1])


def parsear_porcentaje(valor):
    """Convierte un string como '93,85%' o '93.85%' a float."""
    if not valor or valor.strip() == '':
        return None
    # Quitar el signo %
    valor = valor.strip().replace('%', '').strip()
    # Reemplazar coma decimal por punto
    valor = valor.replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return None


def es_bogota(departamento):
    """Detecta si la fila corresponde a Bogotá (el nombre varía entre años)."""
    dep = departamento.upper().strip()
    return 'BOGOT' in dep


def extraer_datos(ruta_csv):
    """Lee el CSV y extrae los indicadores de educación media para Bogotá."""
    registros = []

    with open(ruta_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Filtrar solo Bogotá
            dep = row.get('DEPARTAMENTO', '')
            if not es_bogota(dep):
                continue

            anio = row.get('AÑO', '').strip().replace('"', '')
            if not anio.isdigit():
                continue

            registro = {'anio': int(anio)}

            for col in INDICADORES:
                valor = row.get(col, '')
                registro[NOMBRES[col]] = parsear_porcentaje(valor)

            registros.append(registro)

    return registros


def generar_json(registros):
    """Genera el archivo JSON para el tablero web."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # Ordenar por año
    registros.sort(key=lambda r: r['anio'])

    ruta = os.path.join(DATA_DIR, 'educacion_media.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    print(f'  educacion_media.json: {len(registros)} años')

    return ruta


def main():
    print('=' * 60)
    print('Actualización de datos — Dimensión 2: Educación')
    print('=' * 60)

    print(f'\nBuscando archivo CSV del MEN en: {FUENTES_DIR}')
    archivo = encontrar_archivo_csv(FUENTES_DIR)
    if not archivo:
        return
    print(f'  Archivo: {os.path.basename(archivo)}')

    print('\nLeyendo datos del MEN...')
    registros = extraer_datos(archivo)
    print(f'  {len(registros)} registros de Bogotá extraídos')

    if not registros:
        print('ERROR: No se encontraron datos de Bogotá en el archivo.')
        return

    print('\nGenerando archivo JSON...')
    ruta = generar_json(registros)

    # Verificación rápida
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    ultimo = datos[-1] if datos else None
    if ultimo:
        print(f'\n{"=" * 60}')
        print(f'VERIFICACIÓN — Año {ultimo["anio"]}:')
        print(f'{"=" * 60}')
        for clave, nombre in [('cobertura_bruta', 'Cobertura bruta'),
                               ('cobertura_neta', 'Cobertura neta'),
                               ('aprobacion', 'Aprobación'),
                               ('reprobacion', 'Reprobación'),
                               ('repitencia', 'Repitencia'),
                               ('desercion', 'Deserción')]:
            val = ultimo.get(clave)
            if val is not None:
                print(f'  {nombre}: {val:.2f} %'.replace('.', ','))
            else:
                print(f'  {nombre}: sin dato')

    anios = [d['anio'] for d in datos]
    print(f'\nAños disponibles: {min(anios)} – {max(anios)}')
    print(f'\nArchivo actualizado:')
    print(f'  - {ruta}')
    print(f'\nEl tablero web se actualizará automáticamente al hacer push.')


if __name__ == '__main__':
    main()
