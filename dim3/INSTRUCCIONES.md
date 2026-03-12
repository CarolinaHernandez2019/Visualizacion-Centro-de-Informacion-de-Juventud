# Dimensión 3: Inclusión productiva — instrucciones de actualización

## Datos que usa esta dimensión

| Indicador | Fuente | Frecuencia |
|-----------|--------|------------|
| TGP, TO, TD, PET, ocupados, desocupados | DANE — GEIH Mercado laboral de la juventud | Trimestral |

## Cómo actualizar

### 1. Descargar el nuevo anexo del DANE

- Ir a: https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/mercado-laboral-de-la-juventud
- En "Anexos", descargar el archivo más reciente.
- El nombre es algo como `anex-GEIHMLJ-oct-dic2025.xlsx`.

### 2. Copiar el archivo a `dim3/fuentes/`

Pegar el archivo Excel en esta carpeta (`dim3/fuentes/`). **No borrar los anteriores.**

### 3. Subir a GitHub

**Opción A — desde GitHub.com (más fácil):**

1. Ir al repo → carpeta `dim3/fuentes/`
2. "Add file" → "Upload files"
3. Arrastrar el archivo Excel
4. Mensaje de commit: "Nuevo anexo DANE oct-dic 2025"
5. Click en "Commit changes"

**Opción B — desde terminal:**

```bash
git add dim3/fuentes/
git commit -m "Nuevo anexo DANE oct-dic 2025"
git push
```

### 4. Esperar (~2 minutos)

GitHub Actions ejecuta `dim3/actualizar.py` automáticamente, genera los JSONs en `dim3/data/` y publica el tablero.

### 5. Verificar

- Ir a: https://sdis-juventud.github.io/tablero-cij/dim3/
- Revisar que los datos del último trimestre aparezcan.
- Si no se ve el cambio: Ctrl+Shift+R (limpia caché).

## Qué hacer si algo sale mal

| Problema | Solución |
|----------|----------|
| No se actualizó después de 5 min | Ir al repo en GitHub → pestaña "Actions" → revisar el último workflow |
| Los datos se ven raros | El DANE pudo cambiar el formato del Excel. Avisar a Carolina. |
| No tengo acceso al repo | Pedirle a Carolina que te agregue como colaborador. |

## Lo que NO hacer

- **No editar** los archivos HTML a mano (salvo instrucción de Carolina).
- **No borrar** archivos anteriores de `dim3/fuentes/`.
- **No modificar** los JSONs en `dim3/data/` — se generan automáticamente.

## Archivos de esta dimensión

```
dim3/
├── index.html          ← Página web de la dimensión
├── actualizar.py       ← Script que procesa el Excel del DANE
├── fuentes/            ← Aquí se suben los archivos Excel
├── data/               ← JSONs generados automáticamente
│   ├── mercado_laboral.json
│   └── mercado_laboral_ciudades.json
└── INSTRUCCIONES.md    ← Este archivo
```
