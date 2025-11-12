# Sistema de Análisis para Espectrofotometría 🧪📊

Sistema integrado para procesamiento de datos de espectrofotometría y análisis estadístico de calidad.

## 📋 Proyectos Incluidos

### 🔬 LaboratorioVirtual_Concentraciones.py
**¿Qué hace?**  
Calcula concentraciones mediante espectrofotometría usando regresión lineal.

**Proceso:**
1. Lee archivo Excel `datos_laboratorio.xlsx` (hoja "calibración")
2. Realiza regresión lineal con datos de absorbancia y concentración
<img width="742" height="535" alt="Captura de pantalla 2025-11-12 144220" src="https://github.com/user-attachments/assets/f3a41225-fca5-41bb-ab77-e5ff45a937da" />

   
4. Genera ecuación de la recta (y = mx + b)
5. Calcula concentraciones de muestras en segunda hoja (los datos estan dispuestos en subgrupos ordenados en filas)
<img width="764" height="628" alt="Captura de pantalla 2025-11-12 144226" src="https://github.com/user-attachments/assets/f6d07423-aae1-4e0d-8e05-05a3a1e639c9" />

7. Genera gráficas de la curva de calibración, concentraciones por lote y CV por lote
<img width="1914" height="863" alt="Captura de pantalla 2025-11-12 143825" src="https://github.com/user-attachments/assets/1d1586f8-dbd5-4be6-bddc-6d55c98be81f" />

8. Exporta resultados a `matriz_concentraciones.xlsx`

### 📈 AnalizadorEstadistico_Procesos.py
**¿Qué hace?**  
Realiza análisis estadístico de capacidad de procesos para control de calidad.
<img width="1536" height="754" alt="Figure_1" src="https://github.com/user-attachments/assets/25914e3c-52b3-441c-8a86-bfe1e15e62d8" />


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
