# Dimensión 4: Salud integral y autocuidado — instrucciones de actualización

## Datos que usa esta dimensión

| Sección | Indicador | Fuente | Carpeta fuentes | Frecuencia |
|---------|-----------|--------|-----------------|------------|
| 4.1 SGSSS | Afiliación por régimen | Pendiente — datos no disponibles aún | – | – |
| 4.2 Discapacidad | Jóvenes con discapacidad certificada por tipo | OSB – SaludData | `fuentes/discapacidad/` | Por definir |
| 4.3 Natalidad | Tasa de natalidad por cada mil en jóvenes | OSB – SaludData + DANE proyecciones | `fuentes/natalidad/` | Anual |
| 4.4 Mortalidad | Defunciones de jóvenes 15-29 por causa y localidad | DANE-RUAF-ND / OSB SaludData | `fuentes/mortalidad/` | Anual |

---

## 4.2 Discapacidad

**Fuente:** Observatorio de Salud de Bogotá – SaludData (Discapacidad certificada)

**Nota:** Los datos no tienen columna de año. Es un corte único (acumulado). Se filtra por Grupo de Edad = Juventud + Adolescencia como proxy de 14-28 años.

### Cómo actualizar

1. Descargar el CSV actualizado de SaludData
2. Guardarlo en `dim4/fuentes/discapacidad/` (no borrar el anterior)
3. Ejecutar:
   ```bash
   python dim4/actualizar_discapacidad.py
   ```
4. Subir a GitHub:
   ```bash
   git add dim4/fuentes/ dim4/data/
   git commit -m "Actualizar datos de discapacidad"
   git push
   ```

### Nota sobre los datos

- El CSV usa separador `;` y codificación latin-1
- Las categorías de discapacidad NO son mutuamente excluyentes (una persona puede tener más de un tipo)
- El total de jóvenes es el número de personas, no la suma de categorías

---

## 4.3 Natalidad

**Fuente nacimientos:** Observatorio de Salud de Bogotá – SaludData (Natalidad)
**Fuente población:** DANE – Proyecciones CNPV 2018 por localidad y grupo quinquenal

**Nota:** La tasa se calcula como: nacidos vivos de madres 15-29 / mujeres 15-29 × 1.000. Los grupos quinquenales son 15-19, 20-24 y 25-29.

### Cómo actualizar

1. Descargar el CSV de natalidad actualizado de SaludData
2. Guardarlo en `dim4/fuentes/natalidad/` (no borrar el anterior)
3. El Excel de proyecciones DANE ya debe estar en la misma carpeta
4. Ejecutar:
   ```bash
   python dim4/actualizar_natalidad.py
   ```
5. Subir a GitHub:
   ```bash
   git add dim4/fuentes/ dim4/data/
   git commit -m "Actualizar datos de natalidad"
   git push
   ```

### Notas sobre los datos

- El CSV usa separador `;` y codificación UTF-8 con BOM
- La primera columna tiene un carácter BOM invisible (el script lo maneja con `utf-8-sig`)
- Hay filas para "00 - Bogotá" (total agregado) y para cada localidad individual. El script usa solo las localidades individuales para evitar doble conteo
- Datos disponibles: 2009-2024, pero se filtran desde 2018 (corte de la política)

### Dependencia

El script de natalidad requiere `openpyxl` para leer el Excel de proyecciones:
```bash
pip install openpyxl
```

---

## 4.4 Mortalidad

**Fuente:** DANE – RUAF-ND / Observatorio de Salud de Bogotá – SaludData

**Nota:** Defunciones de jóvenes residentes en Bogotá, edades 15-29 años (grupos quinquenales 15-19, 20-24, 25-29). Causas clasificadas según Lista 6/67.

### Cómo actualizar

1. Descargar el CSV de mortalidad actualizado de SaludData
2. Guardarlo en `dim4/fuentes/mortalidad/` (no borrar el anterior)
3. Ejecutar:
   ```bash
   python dim4/actualizar_mortalidad.py
   ```
4. Subir a GitHub:
   ```bash
   git add dim4/fuentes/ dim4/data/
   git commit -m "Actualizar datos de mortalidad"
   git push
   ```

### Notas sobre los datos

- El CSV usa separador `;` y codificación UTF-8 con BOM
- Columnas clave: `ANO`, `EDAD_QUINQUENAL`, `SEXO`, `CAUSAS_667`, `LOCALIDAD`, `TOTAL_CASOS`
- Se filtran datos desde 2018 (corte de la política)
- El script genera top 10 causas de muerte y desglose por localidad para cada año

---

## Verificar después de actualizar

- Ir a: https://sdis-juventud.github.io/tablero-cij/dim4/
- Revisar que las cuatro secciones (4.1 pendiente, 4.2, 4.3 y 4.4) muestren datos correctos
- Verificar que las tasas de natalidad sean coherentes (tendencia a la baja)
- Verificar que las causas de mortalidad y totales sean coherentes con años anteriores

## Archivos de esta dimensión

```
dim4/
├── index.html                    ← Página web (secciones 4.1, 4.2, 4.3 y 4.4)
├── actualizar_discapacidad.py    ← Script para discapacidad
├── actualizar_natalidad.py       ← Script para natalidad
├── actualizar_mortalidad.py      ← Script para mortalidad
├── fuentes/
│   ├── discapacidad/             ← CSV del OSB + PDF de referencia
│   ├── natalidad/                ← CSV del OSB + Excel proyecciones DANE
│   ├── mortalidad/               ← CSV del OSB (DANE-RUAF-ND)
│   └── localidades/              ← Shapefiles para mapa coroplético
├── data/                         ← JSONs generados automáticamente
│   ├── discapacidad.json
│   ├── natalidad.json
│   ├── mortalidad.json
│   └── localidades.geojson       ← GeoJSON de localidades para mapa
└── INSTRUCCIONES.md              ← Este archivo
```
