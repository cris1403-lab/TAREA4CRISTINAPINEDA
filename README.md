# Tarea 4 – Introducción a Series de Tiempo
Business Intelligence · UNIS · Cristina Pineda

## Requisitos
```
pip install numpy pandas matplotlib statsmodels openpyxl
```

## Cómo ejecutar
1. Descargar `Online Retail.xlsx` de https://archive.ics.uci.edu/dataset/352/online+retail y guardarlo en la carpeta raíz del repositorio.
2. Correr los scripts en orden desde la carpeta raíz:
```
python parte0.py
```
Cada script genera sus figuras (`.png`) y tablas (`.csv`) en la misma carpeta.

## Archivos
| Archivo | Contenido |
|---|---|
| `parte0.py` | Simulaciones AR(1) y procesos sin memoria (Parte 0) |
| `limpiar.py` | Función `limpiar(df)` (Parte 1) |

## Semillas
- Parte 0.2: 101, 102, 103, 104 (ϕ = 0, 0.5, 0.9, 1); realizaciones graficadas con semilla + 1000.
