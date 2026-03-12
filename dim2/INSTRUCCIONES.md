# Dimensión 2: Educación — instrucciones de actualización

## Datos que usa esta dimensión

| Indicador | Fuente | Archivo | Frecuencia |
|-----------|--------|---------|------------|
| Cobertura, deserción, aprobación, reprobación y repitencia en preescolar, básica y media | MEN – Estadísticas en educación por departamento (datos.gov.co) | CSV descargado de datos abiertos | Anual (cuando el MEN publique nuevos datos) |

**Nota:** Este dataset cubre indicadores de educación en preescolar, básica y media por departamento. Se filtra por Bogotá D.C. Los datos disponibles actualmente van de 2011 a 2024.

## Indicadores disponibles en el CSV

- **Cobertura neta:** total, transición, primaria, secundaria, media
- **Cobertura bruta:** total, transición, primaria, secundaria, media
- **Deserción:** total, transición, primaria, secundaria, media
- **Aprobación:** total, transición, primaria, secundaria, media
- **Reprobación:** total, transición, primaria, secundaria, media
- **Repitencia:** total, transición, primaria, secundaria, media
- **Otros:** población 5-16, tasa de matriculación, tamaño promedio de grupo, sedes conectadas a internet

## Cómo actualizar

### 1. Descargar el CSV actualizado

- Ir a: https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/ji8i-4anb/about_data
- Clic en **Exportar** → **CSV**
- El archivo se descarga con un nombre como `MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR,_BÁSICA_Y_MEDIA_POR_DEPARTAMENTO_YYYYMMDD.csv`

### 2. Copiar el archivo a `dim2/fuentes/`

Pegar el nuevo archivo en `dim2/fuentes/`. **No borrar el anterior** (sirve de respaldo).

### 3. Ejecutar el script de actualización

```bash
python dim2/actualizar.py
```

El script busca automáticamente el archivo CSV más reciente en la carpeta.

### 4. Subir a GitHub

```bash
git add dim2/fuentes/ dim2/data/
git commit -m "Actualizar datos de educación básica y media"
git push
```

### 5. Verificar

- Ir a: https://sdis-juventud.github.io/tablero-cij/dim2/
- Revisar que los datos se vean bien y que el último año disponible aparezca.

## Qué hacer si el formato cambió

Si el script falla porque el MEN cambió el formato del CSV:

1. Abrir el nuevo archivo en Excel o un editor de texto.
2. Verificar que las columnas sigan teniendo los mismos nombres (COBERTURA_NETA, DESERCIÓN, etc.).
3. Verificar que Bogotá siga apareciendo como "Bogotá, D.C." en la columna DEPARTAMENTO.
4. Avisar a Carolina para ajustar el script.

## Archivos de esta dimensión

```
dim2/
├── index.html          ← Página web de la dimensión
├── actualizar.py       ← Script que procesa el CSV del MEN
├── fuentes/            ← Aquí se guarda el CSV descargado
├── data/               ← JSONs generados automáticamente
│   └── educacion_media.json
└── INSTRUCCIONES.md    ← Este archivo
```
