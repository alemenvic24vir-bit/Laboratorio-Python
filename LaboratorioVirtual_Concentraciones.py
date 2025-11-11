import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class LaboratorioVirtualConcentraciones:
    def __init__(self, archivo_datos="datos_laboratorio.xlsx"):
        self.archivo_datos = archivo_datos
        print(f"🔬 LABORATORIO VIRTUAL - ANALIZADOR DE CONCENTRACIONES")
        print(f"📁 Leyendo datos desde: {archivo_datos}")
    
    def cargar_calibracion(self):
        """Carga curva de calibración desde Excel"""
        try:
            df_calib = pd.read_excel(self.archivo_datos, sheet_name='Calibracion')
            self.concentraciones = df_calib['Concentracion'].values
            self.absorbancias = df_calib['Absorbancia'].values
            print("✅ Curva de calibración cargada")
            return True
        except Exception as e:
            print(f"❌ Error cargando calibración: {e}")
            return False
    
    def cargar_muestras_matricial(self):
        """Carga muestras en formato matricial desde Excel"""
        try:
            df_muestras = pd.read_excel(self.archivo_datos, sheet_name='Muestras')
            
            # La primera columna contiene los subgrupos (S1, S2, etc.)
            self.subgrupos = df_muestras.iloc[:, 0].values  # Primera columna
            self.lotes = df_muestras.columns[1:].tolist()   # Nombres de lotes (Lote_A, Lote_B, etc.)
            
            # Extraer matriz de absorbancias
            self.matriz_absorbancias = df_muestras.iloc[:, 1:].values
            
            print(f"✅ {len(self.subgrupos)} subgrupos y {len(self.lotes)} lotes cargados")
            print(f"📊 Estructura: {len(self.subgrupos)} filas × {len(self.lotes)} columnas")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando muestras matriciales: {e}")
            return False
    
    def calcular_concentracion_desde_absorbancia(self, absorbancia, pendiente, intercepto):
        """Calcula concentración usando la ecuación de calibración"""
        return (absorbancia - intercepto) / pendiente
    
    def analizar_todo_automatico(self):
        """Analiza TODO automáticamente desde Excel - MANTIENE ESTRUCTURA MATRICIAL"""
        if not self.cargar_calibracion() or not self.cargar_muestras_matricial():
            return None
        
        print("\n" + "="*60)
        print("🎯 INICIANDO ANÁLISIS AUTOMÁTICO COMPLETO - VERSION MATRICIAL")
        print("="*60)
        
        # 1. Calcular curva de calibración
        m, b = np.polyfit(self.concentraciones, self.absorbancias, 1)
        predicciones = m * self.concentraciones + b
        r_cuadrado = np.corrcoef(self.absorbancias, predicciones)[0,1]**2
        
        print(f"\n📈 CURVA DE CALIBRACIÓN:")
        print(f"   A = {m:.4f}C + {b:.4f}")
        print(f"   R² = {r_cuadrado:.4f}")
        
        # 2. Convertir TODA la matriz de absorbancias a concentraciones
        print(f"\n🔍 CONVIRTIENDO MATRIZ DE ABSORBANCIAS A CONCENTRACIONES...")
        matriz_concentraciones = np.zeros_like(self.matriz_absorbancias)
        
        for i in range(len(self.subgrupos)):
            for j in range(len(self.lotes)):
                absorbancias_str = self.matriz_absorbancias[i, j]
                
                # Procesar valor (puede ser string o número)
                if pd.isna(absorbancias_str):
                    concentracion = np.nan
                elif isinstance(absorbancias_str, str):
                    # Si es string, tomar el primer valor
                    try:
                        abs_val = float(absorbancias_str.split(",")[0].strip())
                        concentracion = self.calcular_concentracion_desde_absorbancia(abs_val, m, b)
                    except:
                        concentracion = np.nan
                else:
                    # Si es número directamente
                    concentracion = self.calcular_concentracion_desde_absorbancia(float(absorbancias_str), m, b)
                
                matriz_concentraciones[i, j] = concentracion
        
        # 3. Calcular estadísticas por lote
        print(f"\n📊 CALCULANDO ESTADÍSTICAS POR LOTE:")
        resultados_lotes = []
        todos_datos_individuales = []
        
        for j, lote in enumerate(self.lotes):
            concentraciones_lote = matriz_concentraciones[:, j]
            concentraciones_validas = concentraciones_lote[~np.isnan(concentraciones_lote)]
            
            if len(concentraciones_validas) > 0:
                promedio = np.mean(concentraciones_validas)
                desviacion = np.std(concentraciones_validas)
                cv = (desviacion / promedio) * 100 if promedio > 0 else 0
                
                print(f"\n   📦 {lote}:")
                print(f"      Concentraciones: {len(concentraciones_validas)} valores válidos")
                print(f"      Promedio: {promedio:.4f} ± {desviacion:.4f} M")
                print(f"      CV: {cv:.1f}%")
                
                resultados_lotes.append({
                    'Lote': lote,
                    'Concentracion_Promedio': promedio,
                    'Desviacion': desviacion,
                    'CV': cv,
                    'Numero_Muestras': len(concentraciones_validas),
                    'Estado': 'APROBADO' if cv < 5 else 'REVISAR'
                })
            
            # Guardar datos individuales para este lote
            for i, subgrupo in enumerate(self.subgrupos):
                if not np.isnan(matriz_concentraciones[i, j]):
                    todos_datos_individuales.append({
                        'Subgrupo': subgrupo,
                        'Lote': lote,
                        'Absorbancia': self.matriz_absorbancias[i, j],
                        'Concentracion_Individual': matriz_concentraciones[i, j]
                    })
        
        # 4. Guardar TODOS los datos en Excel manteniendo estructura matricial
        self.guardar_resultados_matriciales(matriz_concentraciones, resultados_lotes, todos_datos_individuales, m, b, r_cuadrado)
        
        # 5. Generar reporte y gráficos
        self.generar_reporte_final(resultados_lotes)
        self.graficar_resultados(resultados_lotes)
        
        return {
            'resultados_lotes': resultados_lotes,
            'matriz_concentraciones': matriz_concentraciones,
            'datos_individuales': todos_datos_individuales,
            'ecuacion_calibracion': {'pendiente': m, 'intercepto': b, 'r_cuadrado': r_cuadrado}
        }
    
    def guardar_resultados_matriciales(self, matriz_concentraciones, resultados_lotes, datos_individuales, m, b, r_cuadrado):
        """Guarda resultados manteniendo estructura matricial original"""
        
        # 1. MATRIZ DE CONCENTRACIONES (misma estructura que el Excel original)
        df_matriz_concentraciones = pd.DataFrame(
            matriz_concentraciones,
            index=self.subgrupos,
            columns=self.lotes
        )
        df_matriz_concentraciones.index.name = 'Subgrupo'
        df_matriz_concentraciones.to_excel('matriz_concentraciones.xlsx')
        
        # 2. DATOS INDIVIDUALES (formato largo para análisis estadístico)
        df_individual = pd.DataFrame(datos_individuales)
        df_individual.to_excel('datos_individuales_completos.xlsx', index=False)
        
        # 3. RESULTADOS POR LOTE (resumen estadístico)
        df_lotes = pd.DataFrame(resultados_lotes)
        df_lotes.to_excel('resultados_por_lote.xlsx', index=False)
        
        # 4. INFO CALIBRACIÓN
        info_calibracion = pd.DataFrame({
            'Parametro': ['Pendiente', 'Intercepto', 'R_cuadrado', 'Ecuacion'],
            'Valor': [m, b, r_cuadrado, f'A = {m:.4f}C + {b:.4f}']
        })
        info_calibracion.to_excel('info_calibracion.xlsx', index=False)
        
        print(f"\n💾 ARCHIVOS GUARDADOS (ESTRUCTURA MATRICIAL):")
        print(f"   • matriz_concentraciones.xlsx - MISMA ESTRUCTURA que tu Excel original")
        print(f"   • datos_individuales_completos.xlsx - Todos los datos en formato largo")
        print(f"   • resultados_por_lote.xlsx - Resumen estadístico por lote")
        print(f"   • info_calibracion.xlsx - Información de la curva de calibración")
    
    def generar_reporte_final(self, resultados):
        """Genera reporte ejecutivo"""
        print("\n" + "="*60)
        print("📋 REPORTE FINAL - CONTROL DE CALIDAD POR LOTE")
        print("="*60)
        
        aprobadas = sum(1 for r in resultados if r['Estado'] == 'APROBADO')
        eficiencia = (aprobadas / len(resultados)) * 100
        total_muestras = sum(r['Numero_Muestras'] for r in resultados)
        
        print(f"\n📊 ESTADÍSTICAS GLOBALES:")
        print(f"   Lotes analizados: {len(resultados)}")
        print(f"   Total de muestras: {total_muestras}")
        print(f"   Lotes APROBADOS: {aprobadas}")
        print(f"   Lotes a REVISAR: {len(resultados) - aprobadas}")
        print(f"   EFICIENCIA: {eficiencia:.1f}%")
        
        # Estadísticas de concentraciones
        concentraciones = [r['Concentracion_Promedio'] for r in resultados]
        print(f"   Concentración promedio global: {np.mean(concentraciones):.4f} M")
        print(f"   Rango de concentraciones: {min(concentraciones):.4f} - {max(concentraciones):.4f} M")
        
        # Mostrar matriz de concentraciones en consola
        print(f"\n📈 CONCENTRACIONES CALCULADAS:")
        print(f"   Revisa 'matriz_concentraciones.xlsx' para la tabla completa")
    
    def graficar_resultados(self, resultados):
        """Genera gráficos profesionales"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Gráfico 1: Curva de calibración
        m, b = np.polyfit(self.concentraciones, self.absorbancias, 1)
        x_line = np.linspace(min(self.concentraciones), max(self.concentraciones), 100)
        y_line = m * x_line + b
        
        ax1.scatter(self.concentraciones, self.absorbancias, color='red', s=60, label='Datos calibración')
        ax1.plot(x_line, y_line, 'b-', alpha=0.7, label=f'A = {m:.4f}C + {b:.4f}')
        ax1.set_xlabel('Concentración (M)')
        ax1.set_ylabel('Absorbancia')
        ax1.set_title('CURVA DE CALIBRACIÓN')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.text(0.05, 0.85, f'R² = {np.corrcoef(self.absorbancias, m*self.concentraciones+b)[0,1]**2:.4f}', 
                transform=ax1.transAxes, bbox=dict(boxstyle="round", facecolor="wheat"))
        
        # Gráfico 2: Resultados por lote (promedios)
        lotes = [r['Lote'] for r in resultados]
        concentraciones = [r['Concentracion_Promedio'] for r in resultados]
        colores = ['green' if r['Estado'] == 'APROBADO' else 'red' for r in resultados]
        
        bars = ax2.bar(lotes, concentraciones, color=colores, alpha=0.7)
        ax2.set_xlabel('Lotes')
        ax2.set_ylabel('Concentración Promedio (M)')
        ax2.set_title('CONCENTRACIONES POR LOTE')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        ax2.grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for bar, conc in zip(bars, concentraciones):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001, 
                    f'{conc:.3f}', ha='center', va='bottom', fontsize=8)
        
        # Gráfico 3: Control de calidad (CV por lote)
        cvs = [r['CV'] for r in resultados]
        colores_cv = ['green' if cv < 5 else 'red' for cv in cvs]
        
        bars_cv = ax3.bar(lotes, cvs, color=colores_cv, alpha=0.7)
        ax3.axhline(y=5, color='red', linestyle='--', label='Límite CV (5%)')
        ax3.set_xlabel('Lotes')
        ax3.set_ylabel('Coeficiente de Variación (%)')
        ax3.set_title('CONTROL DE CALIDAD - CV POR LOTE')
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Añadir valores en las barras CV
        for bar, cv in zip(bars_cv, cvs):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{cv:.1f}%', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.show()

# 🎯 EJECUCIÓN AUTOMÁTICA
if __name__ == "__main__":
    lab_virtual = LaboratorioVirtualConcentraciones("datos_laboratorio.xlsx")
    resultados_completos = lab_virtual.analizar_todo_automatico()
    
    if resultados_completos:
        print(f"\n🎉 ANÁLISIS COMPLETADO!")
        print(f"📊 Matriz de {len(lab_virtual.subgrupos)}×{len(lab_virtual.lotes)} concentraciones guardada")
        print(f"📋 {len(resultados_completos['resultados_lotes'])} lotes analizados")
        print(f"📈 Estructura matricial conservada en 'matriz_concentraciones.xlsx'")