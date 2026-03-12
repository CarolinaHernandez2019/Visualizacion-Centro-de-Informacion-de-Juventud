# Dimensión 2: Educación — instrucciones de actualización

## Datos que usa esta dimensión

| Sección | Indicador | Fuente | Archivo | Frecuencia |
|---------|-----------|--------|---------|------------|
| 2.1 Educación media | Cobertura, deserción, aprobación, reprobación y repitencia | MEN – Estadísticas en educación por departamento (datos.gov.co) | CSV en `fuentes/` | Anual |
| 2.2 Educación superior | Matrículas por nivel de formación (técnica, tecnológica, universitaria, posgrado) | MEN – Estadísticas de matrícula por municipio (datos.gov.co) | CSV en `fuentes/Educ superior/` | Anual |

---

## 2.1 Educación media

**Dataset:** [MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-BÁSICA_Y_MEDIA_POR_DEPARTAMENTO](https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/ji8i-4anb/about_data)

**Nota:** Se filtra por Bogotá D.C. Los datos disponibles actualmente van de 2011 a 2024.

### Indicadores disponibles

- **Cobertura neta y bruta:** total, transición, primaria, secundaria, media
- **Deserción, aprobación, reprobación, repitencia:** total, transición, primaria, secundaria, media

### Cómo actualizar

1. Ir al dataset → **Exportar** → **CSV**
2. Pegar el archivo en `dim2/fuentes/` (no borrar el anterior)
3. Ejecutar:
   ```bash
   python dim2/actualizar.py
   ```
4. Subir a GitHub:
   ```bash
   git add dim2/fuentes/ dim2/data/
   git commit -m "Actualizar datos de educación media"
   git push
   ```

---

## 2.2 Educación superior

**Dataset:** [MEN_ESTADISTICAS-MATRICULA-POR-MUNICIPIOS_ES](https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS-MATRICULA-POR-MUNICIPIOS_ES/y9ga-zwzy/about_data)

**Nota:** Este dataset tiene ~19.600 filas (todos los municipios de Colombia). El script filtra por Bogotá (código municipio 11001) y calcula totales nacionales. Datos disponibles: 2005 a 2021.

**Importante:** No usar la API de datos.gov.co para descargar (tiene límite de 1.000 filas). Usar el botón **"Descargar archivo"** → **CSV**.

### Indicadores que se extraen

- **Matrículas por nivel:** técnica profesional, tecnológica, universitaria, especialización, maestría, doctorado
- **Total Bogotá vs. total Colombia** (con porcentaje de participación)
- **IES con oferta** en Bogotá

### Cómo actualizar

1. Ir al dataset → **Descargar archivo** → **CSV** (no usar "Exportar" ni la API)
2. Pegar el archivo en `dim2/fuentes/Educ superior/` (no borrar el anterior)
3. Ejecutar:
   ```bash
   python dim2/actualizar_educ_superior.py
   ```
4. Subir a GitHub:
   ```bash
   git add dim2/fuentes/ dim2/data/
   git commit -m "Actualizar datos de educación superior"
   git push
   ```

### Notas sobre el CSV

- Los números usan formato colombiano (puntos como miles: "63.098" = 63.098 matrículas)
- El nombre de Bogotá varía entre años ("BOGOTÁ D.C.", "BOGOTA D.C.", "Bogotá, D.C."). El script los detecta todos.
- Hay filas duplicadas por variantes del nombre. El script deduplica por código de municipio.

---

## Verificar después de actualizar

- Ir a: https://sdis-juventud.github.io/tablero-cij/dim2/
- Revisar que las dos secciones (2.1 y 2.2) muestren datos correctos
- Verificar que el último año disponible aparezca en cada selector

## Qué hacer si el formato cambió

Si algún script falla porque el MEN cambió el formato del CSV:

1. Abrir el nuevo archivo en Excel o un editor de texto
2. Verificar que las columnas sigan teniendo los mismos nombres
3. Verificar que Bogotá aparezca (buscar "BOGOT" en el archivo)
4. Avisar a Carolina para ajustar el script

## Archivos de esta dimensión

```
dim2/
├── index.html                    ← Página web (secciones 2.1 y 2.2)
├── actualizar.py                 ← Script para educación media
├── actualizar_educ_superior.py   ← Script para educación superior
├── fuentes/                      ← CSVs de educación media
│   └── Educ superior/            ← CSVs de educación superior
├── data/                         ← JSONs generados automáticamente
│   ├── educacion_media.json
│   └── educacion_superior.json
└── INSTRUCCIONES.md              ← Este archivo
```
