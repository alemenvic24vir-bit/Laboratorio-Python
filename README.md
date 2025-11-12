# Sistema de Análisis para Espectrofotometría 🧪📊

Sistema integrado para procesamiento de datos de espectrofotometría y análisis estadístico de calidad.

## 📋 Proyectos Incluidos

### 🔬 LaboratorioVirtual_Concentraciones.py
**¿Qué hace?**  
Calcula concentraciones mediante espectrofotometría usando regresión lineal.

**Proceso:**
1. Lee archivo Excel `datos_laboratorio.xlsx` (hoja "calibración")
2. Realiza regresión lineal con datos de absorbancia y concentración
3. Genera ecuación de la recta (y = mx + b)
4. Calcula concentraciones de muestras en segunda hoja (los datos estan dispuestos en subgrupos ordenados en filas)
5. Exporta resultados a `matriz_concentraciones.xlsx`

### 📈 AnalizadorEstadistico_Procesos.py
**¿Qué hace?**  
Realiza análisis estadístico de capacidad de procesos para control de calidad.

**Métricas calculadas:**
- Cp, Cpk (Capacidad del proceso)
- Pp, Ppk (Desempeño del proceso)
- Gráficas de control y tendencias
- Análisis de estabilidad del proceso

## 🔄 Flujo de Trabajo
```bash
# 1. Calcular concentraciones
python LaboratorioVirtual_Concentraciones.py

# 2. Análisis estadístico
python AnalizadorEstadistico_Procesos.py
