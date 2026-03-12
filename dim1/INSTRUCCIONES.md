# Dimensión 1: Ser joven — instrucciones de actualización

## Datos que usa esta dimensión

| Indicador | Fuente | Frecuencia |
|-----------|--------|------------|
| Población joven (14-28) por localidad, zona, edad y sexo | DANE — Proyecciones CNPV 2018, desagregación Bogotá | Cuando el DANE publique nuevas proyecciones |

**Nota:** Estas proyecciones se basan en el Censo 2018. El archivo actual cubre 2018-2035. No se actualiza trimestralmente como la dimensión 3 — solo cuando el DANE publique nuevas proyecciones (probablemente con el próximo censo).

## Cómo actualizar (cuando salgan nuevas proyecciones)

### 1. Descargar las nuevas proyecciones del DANE

- Ir a: https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion/proyecciones-de-poblacion-bogota
- Descargar el archivo de proyecciones por localidad.
- El nombre actual es `anexo-proyecciones-poblacion-bogota-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx` pero puede cambiar.

### 2. Verificar el formato del nuevo archivo

**Importante:** si el DANE publica un archivo con formato diferente, hay que revisar:

- ¿La hoja se sigue llamando `Localidades`? Si no, actualizar `HOJA_PRINCIPAL` en `actualizar.py`.
- ¿Los headers siguen en la fila 12? Si no, actualizar `FILA_HEADERS`.
- ¿Las columnas siguen siendo `COD_LOC`, `NOM_LOC`, `AREA`, `AÑO`, `Hombres_0`...`Hombres_100+`, `Mujeres_0`...`Mujeres_100+`? Si cambiaron los nombres, hay que ajustar el script.

### 3. Copiar el archivo a `dim1/fuentes/`

Pegar el nuevo archivo en `dim1/fuentes/`. **No borrar el anterior.**

### 4. Probar localmente (opcional)

```bash
python dim1/actualizar.py
```

El script busca automáticamente el archivo más reciente que contenga "proyecciones" en el nombre.

### 5. Subir a GitHub

```bash
git add dim1/fuentes/
git commit -m "Nuevas proyecciones de población Bogotá"
git push
```

O subir directamente por GitHub.com a la carpeta `dim1/fuentes/`.

### 6. Verificar

- Ir a: https://sdis-juventud.github.io/tablero-cij/dim1/
- Revisar que los datos se vean bien.

## Qué hacer si el formato cambió

Si el script falla porque el DANE cambió el formato del Excel:

1. Abrir el nuevo archivo en Excel.
2. Buscar la hoja con datos por localidad.
3. Identificar en qué fila están los headers (columnas como COD_LOC, NOM_LOC, etc.).
4. Avisar a Carolina para ajustar el script.

## Archivos de esta dimensión

```
dim1/
├── index.html          ← Página web de la dimensión
├── actualizar.py       ← Script que procesa el Excel del DANE
├── fuentes/            ← Aquí se guarda el archivo de proyecciones
├── data/               ← JSONs generados automáticamente
│   ├── resumen_bogota.json
│   └── localidades.json
└── INSTRUCCIONES.md    ← Este archivo
```
