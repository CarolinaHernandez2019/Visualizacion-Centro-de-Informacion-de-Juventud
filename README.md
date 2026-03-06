# Visualización Centro de Información de Juventud

Tablero interactivo de indicadores de juventud para la Subdirección para la Juventud (SDIS Bogotá).

Muestra datos del mercado laboral juvenil (15-28 años) de Bogotá, con comparación contra el total nacional y las 13 ciudades principales, usando datos de la Gran Encuesta Integrada de Hogares (GEIH) del DANE.

**URL del tablero:** https://carolinahernandez2019.github.io/Visualizacion-Centro-de-Informacion-de-Juventud/

---

## Estructura del proyecto

```
├── index.html                 # Tablero web (HTML + JS + Chart.js)
├── actualizar_datos.py        # Script para actualizar datos automáticamente
├── data/
│   ├── mercado_laboral.json           # Bogotá - serie histórica desde 2014
│   └── mercado_laboral_ciudades.json  # Comparación 7 ciudades desde 2018
└── README.md
```

---

## Cómo actualizar los datos

Cada trimestre el DANE publica un nuevo anexo de mercado laboral juvenil. Para actualizar el tablero:

### Paso 1: Descargar el anexo del DANE

1. Ir a la página del DANE:
   https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/mercado-laboral-de-la-juventud
2. Descargar el archivo más reciente (tipo `anex-GEIHMLJ-xxx-xxx20XX.xlsx`)
3. Guardar en la carpeta de fuentes:
   ```
   240708_Fuentes/Actualizacion 2026/Mercado laboral/
   ```

### Paso 2: Correr el script de actualización

```bash
cd tablero-cij
python actualizar_datos.py
```

El script automáticamente:
- Encuentra el anexo DANE más reciente
- Extrae datos de Bogotá, Medellín, Cali, Barranquilla, Bucaramanga, total nacional y 13 ciudades
- Genera los archivos JSON en `data/`
- Actualiza el Excel del Power BI (si existe en la carpeta de fuentes)
- Muestra un resumen de los trimestres disponibles

### Paso 3: Verificar localmente

```bash
python -m http.server 8080
```

Abrir http://localhost:8080 y verificar que:
- Los años y trimestres nuevos aparecen en los filtros
- Los datos del diagrama de árbol se ven correctos
- Las gráficas de comparación muestran las ciudades

### Paso 4: Subir los cambios

```bash
git add data/
git commit -m "Actualizar datos mercado laboral [trimestre]"
git push
```

El tablero se actualiza automáticamente en GitHub Pages en unos minutos.

---

## Requisitos técnicos

- **Python 3.8+** con la librería `openpyxl`:
  ```bash
  pip install openpyxl
  ```
- **Git** para control de versiones
- Acceso a internet para descargar los anexos del DANE

---

## Datos y fuentes

| Archivo | Fuente | Cobertura | Actualización |
|---------|--------|-----------|---------------|
| `mercado_laboral.json` | DANE - GEIH Mercado laboral juvenil | Bogotá D.C., 2014-presente | Trimestral |
| `mercado_laboral_ciudades.json` | DANE - GEIH Mercado laboral juvenil | 7 entidades, 2018-presente | Trimestral |

### Indicadores incluidos

- **TGP** - Tasa global de participación
- **TO** - Tasa de ocupación
- **TD** - Tasa de desocupación
- **PET** - Población en edad de trabajar
- **PET 15-28** - Población en edad de trabajar de 15 a 28 años
- **Fuerza de trabajo** - Ocupados + Desocupados
- **Fuera de la fuerza de trabajo** - Población que no busca empleo

### Ciudades de comparación

- Bogotá D.C.
- Medellín A.M.
- Cali A.M.
- Barranquilla A.M.
- Bucaramanga A.M.
- Total 13 ciudades
- Total nacional

### Notas metodológicas

**Total nacional:** excluye de la cobertura de los departamentos de la Amazonía y Orinoquía las cabeceras municipales que no son capitales de departamento, así como los centros poblados y rural disperso. También se excluye la población de Providencia y el centro poblado y rural disperso de San Andrés.

**13 ciudades y áreas metropolitanas:** Bogotá D.C., Medellín A.M., Cali A.M., Barranquilla A.M., Bucaramanga A.M., Manizales A.M., Pereira A.M., Cúcuta A.M., Pasto, Ibagué, Montería, Cartagena y Villavicencio.

---

## Notas para el analista nuevo

### Sobre los trimestres

El DANE publica trimestres **móviles** (Ene-Mar, Feb-Abr, Mar-May...) y **fijos** (Ene-Mar, Abr-Jun, Jul-Sep, Oct-Dic). El tablero solo muestra los 4 trimestres fijos para simplificar la lectura.

### Sobre el script `actualizar_datos.py`

- Busca archivos que empiecen con `anex-GEIHMLJ` en la carpeta de fuentes
- Las filas de inicio de cada ciudad están hardcodeadas (líneas 50-58 del script). Si el DANE cambia el formato del anexo, hay que actualizar estos números
- Crea un backup del Excel del Power BI antes de modificarlo

### Si el DANE cambia el formato del anexo

1. Abrir el nuevo anexo en Excel
2. Buscar la hoja `23 ciudades trim móvil`
3. Encontrar la fila donde empieza la sección de Bogotá (buscar "Bogotá" o "% Población en edad de trabajar")
4. Actualizar la variable `CIUDADES_EXTRAER` en `actualizar_datos.py` con el nuevo número de fila

### Sobre el Power BI

Este tablero web complementa el tablero de Power BI. Ambos usan los mismos datos fuente del DANE. El script actualiza ambos al mismo tiempo.

---

## Contacto

Subdirección para la Juventud - SDIS Bogotá
