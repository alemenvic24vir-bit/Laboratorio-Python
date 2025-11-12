# Sistema de Análisis para Espectrofotometría 🧪📊

**Sistema integrado** para procesamiento de datos de espectrofotometría y análisis estadístico de calidad.

> **Ingeniero Químico** automatizando QC:  
> De **4 horas manuales** → **menos de 5 minutos automáticos**

---

## 📋 Proyectos Incluidos

### 🔬 `LaboratorioVirtual_Concentraciones.py`
**¿Qué hace?**  
Calcula concentraciones mediante espectrofotometría usando **regresión lineal**.

**Proceso:**
1. Lee archivo Excel `datos_laboratorio.xlsx` (hoja **"Calibracion"**)
2. Realiza regresión lineal con datos de absorbancia y concentración  
   ![Hoja Calibracion](https://github.com/user-attachments/assets/f3a41225-fca5-41bb-ab77-e5ff45a937da)

3. Genera ecuación de la recta: `A = m·C + b` (R² > 0.99)
4. Calcula concentraciones de muestras en hoja **"Muestras"** (matriz: filas = subgrupos, columnas = lotes)  
   ![Matriz Muestras](https://github.com/user-attachments/assets/f6d07423-aae1-4e0d-8e05-05a3a1e639c9)

5. Genera gráficas: curva de calibración, concentraciones por lote, CV por lote  
   ![Gráficas Concentraciones](https://github.com/user-attachments/assets/1d1586f8-dbd5-4be6-bddc-6d55c98be81f)

6. **Salida**: `matriz_concentraciones.xlsx`

---

### 📈 `AnalizadorEstadistico_Procesos.py`
**¿Qué hace?**  
Realiza análisis estadístico de **capacidad de procesos** para control de calidad.

![Gráficos Minitab](https://github.com/user-attachments/assets/25914e3c-52b3-441c-8a86-bfe1e15e62d8)

**Métricas calculadas:**
- **Cp / Cpk** → Capacidad del proceso
- **Pp / Ppk** → Desempeño del proceso
- 6 gráficos tipo Minitab (histograma, boxplot, control, Q-Q, etc.)
- PPM fuera de especificación
- Análisis de estabilidad

**Límites de especificación**: `0.08 M – 0.12 M`

---

## 🛠️ Instalación y Uso

### Prerrequisitos
- Python 3.8+
- pip

### Pasos:
```bash
# 1. Clona el repositorio
git clone https://github.com/alemenvic24vir-bit/Laboratorio-Python.git
cd Laboratorio-Python

# 2. Instala dependencias
pip install pandas numpy matplotlib scipy openpyxl

# 3. Ejecuta los scripts
python LaboratorioVirtual_Concentraciones.py
python AnalizadorEstadistico_Procesos.py
