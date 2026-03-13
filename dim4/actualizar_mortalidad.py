# actualizar_mortalidad.py — Dimensión 4: Salud integral y autocuidado
# Script para procesar el CSV de mortalidad del OSB y generar
# el JSON de causas de muerte en jóvenes (15-29 años).
#
# Uso:
#   1. Descargar CSV de mortalidad de SaludData / OSB
#   2. Guardar en dim4/fuentes/mortalidad/
#   3. Correr: python dim4/actualizar_mortalidad.py

import os
import csv
import json

# ============================================================
# Configuración
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FUENTES_DIR = os.path.join(SCRIPT_DIR, 'fuentes', 'mortalidad')
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

# Grupos de edad de jóvenes
GRUPOS_JUVENTUD = {'15 a 19', '20 a 24', '25 a 29'}

# Solo datos desde 2018 (corte de la política)
ANIO_MIN = 2018


# ============================================================
# Funciones
# ============================================================

def encontrar_csv(carpeta):
    """Busca el CSV principal de mortalidad (no el de metadatos)."""
    archivos = [f for f in os.listdir(carpeta)
                if f.endswith('.csv') and 'metadato' not in f.lower()
                and not f.startswith('~$')]
    if not archivos:
        return None
    archivos.sort()
    return os.path.join(carpeta, archivos[-1])


def procesar(ruta_csv):
    """Lee el CSV y extrae datos de mortalidad de jóvenes."""
    # Por año: total, por sexo, por causa
    por_anio = {}
    # Por localidad (todos los años sumados para el último disponible)
    por_localidad_anio = {}

    with open(ruta_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            edad_q = row.get('EDAD_QUINQUENAL', '').strip()
            if edad_q not in GRUPOS_JUVENTUD:
                continue

            try:
                anio = int(row.get('ANO', '0'))
                casos = int(row.get('TOTAL_CASOS', '0'))
            except (ValueError, TypeError):
                continue

            if anio < ANIO_MIN:
                continue

            sexo = row.get('SEXO', '').strip()
            causa = row.get('CAUSAS_667', '').strip()
            localidad = row.get('LOCALIDAD', '').strip()

            # Inicializar año
            if anio not in por_anio:
                por_anio[anio] = {
                    'total': 0,
                    'hombres': 0,
                    'mujeres': 0,
                    'causas': {},
                    'localidades': {},
                }

            a = por_anio[anio]
            a['total'] += casos

            if sexo == 'Hombres':
                a['hombres'] += casos
            elif sexo == 'Mujeres':
                a['mujeres'] += casos

            if causa:
                a['causas'][causa] = a['causas'].get(causa, 0) + casos

            if localidad and localidad != 'Sin Dato':
                a['localidades'][localidad] = a['localidades'].get(localidad, 0) + casos

    return por_anio


def generar_json(por_anio):
    """Genera el JSON de mortalidad."""
    os.makedirs(DATA_DIR, exist_ok=True)

    anios = sorted(por_anio.keys())
    registros = []

    for anio in anios:
        a = por_anio[anio]

        # Top 10 causas
        causas_sorted = sorted(a['causas'].items(), key=lambda x: x[1], reverse=True)
        top_causas = [{'causa': c, 'casos': n} for c, n in causas_sorted[:10]]

        # Localidades ordenadas por casos
        locs_sorted = sorted(a['localidades'].items(), key=lambda x: x[1], reverse=True)
        por_localidad = [{'localidad': l, 'casos': n} for l, n in locs_sorted]

        registros.append({
            'anio': anio,
            'total': a['total'],
            'hombres': a['hombres'],
            'mujeres': a['mujeres'],
            'top_causas': top_causas,
            'por_localidad': por_localidad,
        })

    resultado = {
        'por_anio': registros,
        'nota': 'Defunciones de jóvenes 15-29 años residentes en Bogotá. Fuente: DANE-RUAF-ND / OSB SaludData.',
    }

    ruta = os.path.join(DATA_DIR, 'mortalidad.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f'  mortalidad.json generado')
    return ruta


def main():
    print('=' * 60)
    print('Actualización — Dimensión 4: Mortalidad')
    print('=' * 60)

    archivo = encontrar_csv(FUENTES_DIR)
    if not archivo:
        print('ERROR: No se encontró CSV de mortalidad')
        return
    print(f'  Archivo: {os.path.basename(archivo)}')

    print('\nProcesando...')
    por_anio = procesar(archivo)
    print(f'  Años: {sorted(por_anio.keys())}')

    print('\nGenerando JSON...')
    ruta = generar_json(por_anio)

    # Verificación
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    print(f'\n{"=" * 60}')
    print('VERIFICACIÓN:')
    print(f'{"=" * 60}')
    for r in datos['por_anio']:
        print(f'  {r["anio"]}: {r["total"]:,} muertes (H:{r["hombres"]:,} M:{r["mujeres"]:,})'.replace(',', '.'))
        if r['top_causas']:
            print(f'    #1: {r["top_causas"][0]["causa"]} ({r["top_causas"][0]["casos"]})')

    print(f'\nArchivo: {ruta}')


if __name__ == '__main__':
    main()
