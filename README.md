# QC Automatización con Python  
**Análisis Espectrofotométrico + Cp/Cpk tipo Minitab**

> **Ingeniero Químico** automatizando control de calidad:  
> De **4 horas manuales** → **menos de 5 minutos automáticos**

---

## ¿Qué hace este proyecto?

| Módulo | Funcionalidad clave |
|--------|---------------------|
| `Calculadora_de_concentracionesV2.py` | • Curva de calibración (regresión lineal)<br>• Convierte absorbancias → concentraciones<br>• Estadísticas por lote (promedio, CV, aprobación) |
| `Analizador_EstadisticoV2.py` | • **Cp/Cpk con desviación pooled** (exacto como Minitab)<br>• 6 gráficos profesionales<br>• PPM fuera de especificación |

**Límites de especificación**: `0.08 M – 0.12 M`  
**R² promedio**: `> 0.99`  
**Salidas generadas**:  
- `matriz_concentraciones.xlsx`  
- `reporte_estadistico_avanzado.xlsx`  
- 3 gráficos tipo Minitab

---

## Cómo ejecutarlo

```bash
pip install pandas numpy matplotlib scipy openpyxl
python Calculadora_de_concentracionesV2.py
python Analizador_EstadisticoV2.py
