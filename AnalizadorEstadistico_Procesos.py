import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import integrate

class AnalizadorEstadisticoProcesos:
    def __init__(self):
        self.LIMITE_INFERIOR = 0.08  # 0.08M
        self.LIMITE_SUPERIOR = 0.12  # 0.12M
        self.OBJETIVO = 0.10         # 0.10M
        
        print(f"📊 ANALIZADOR ESTADÍSTICO AVANZADO - CONTROL DE PROCESOS")
        print(f"🎯 Límites: {self.LIMITE_INFERIOR}M - {self.OBJETIVO}M - {self.LIMITE_SUPERIOR}M")
    
    def cargar_matriz_concentraciones(self, archivo="matriz_concentraciones.xlsx"):
        """Carga la matriz de concentraciones desde Excel"""
        try:
            df_matriz = pd.read_excel(archivo, index_col=0)
            self.matriz_concentraciones = df_matriz
            self.subgrupos = df_matriz.index.tolist()  # S1, S2, S3, etc.
            self.lotes = df_matriz.columns.tolist()    # Lote_A, Lote_B, etc.
            
            print(f"✅ Matriz de {len(self.subgrupos)}×{len(self.lotes)} concentraciones cargada desde {archivo}")
            print(f"📊 Subgrupos: {len(self.subgrupos)} | Lotes: {len(self.lotes)}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando matriz de concentraciones: {e}")
            print("⚠️  Asegúrate de ejecutar primero LaboratorioVirtual_Concentraciones.py")
            return False
    
    def calcular_desviacion_pooled(self):
        """Calcula la desviación estándar pooled entre subgrupos"""
        # Para cada subgrupo (fila), calcular desviación estándar
        desviaciones_subgrupos = []
        varianzas_subgrupos = []
        n_subgrupos = []
        
        for subgrupo in self.subgrupos:
            datos_subgrupo = self.matriz_concentraciones.loc[subgrupo].values
            datos_validos = datos_subgrupo[~np.isnan(datos_subgrupo)]
            
            if len(datos_validos) > 1:  # Necesitamos al menos 2 datos para calcular desviación
                n = len(datos_validos)
                s = np.std(datos_validos, ddof=1)  # Desviación muestral
                varianza = s ** 2
                
                desviaciones_subgrupos.append(s)
                varianzas_subgrupos.append(varianza)
                n_subgrupos.append(n)
        
        if len(varianzas_subgrupos) == 0:
            return 0
        
        # Calcular desviación pooled usando la fórmula correcta
        # s_pooled = √[∑((nᵢ - 1) * sᵢ²) / (N - k)]
        
        numerador = sum((n - 1) * varianza for n, varianza in zip(n_subgrupos, varianzas_subgrupos))
        N_total = sum(n_subgrupos)  # Total de datos
        k = len(n_subgrupos)        # Número de subgrupos
        
        if N_total - k <= 0:
            return np.mean(desviaciones_subgrupos) if desviaciones_subgrupos else 0
        
        varianza_pooled = numerador / (N_total - k)
        desviacion_pooled = np.sqrt(varianza_pooled)
        
        print(f"\n📐 CÁLCULO DESVIACIÓN POOLED:")
        print(f"   Número de subgrupos (k): {k}")
        print(f"   Total de datos (N): {N_total}")
        print(f"   Numerador ∑[(nᵢ-1)*sᵢ²]: {numerador:.6f}")
        print(f"   Varianza pooled: {varianza_pooled:.6f}")
        print(f"   Desviación pooled: {desviacion_pooled:.6f}")
        
        return desviacion_pooled
    
    def calcular_estadisticas_avanzadas(self):
        """Calcula estadísticas tipo Minitab con desviación pooled"""
        # Obtener todos los datos para estadísticas generales
        todos_datos = self.matriz_concentraciones.values.flatten()
        todos_datos = todos_datos[~np.isnan(todos_datos)]
        
        print(f"\n🧮 CALCULANDO ESTADÍSTICAS CON {len(todos_datos)} DATOS...")
        
        # Estadísticas básicas (con todos los datos)
        media = np.mean(todos_datos)
        mediana = np.median(todos_datos)
        desviacion_overall = np.std(todos_datos, ddof=1)  # Pp
        desviacion_pooled = self.calcular_desviacion_pooled()  # Cp
        varianza_overall = np.var(todos_datos, ddof=1)
        rango = np.ptp(todos_datos)
        minimo = np.min(todos_datos)
        maximo = np.max(todos_datos)
        
        # Estadísticas de posición
        q1 = np.percentile(todos_datos, 25)
        q3 = np.percentile(todos_datos, 75)
        iqr = q3 - q1
        
        # Capacidad del proceso - DIFERENCIAR ENTRE Cp/Cpk y Pp/Ppk
        # Cp/Pp - Capacidad potencial
        cp_potencial = (self.LIMITE_SUPERIOR - self.LIMITE_INFERIOR) / (6 * desviacion_pooled)
        pp_potencial = (self.LIMITE_SUPERIOR - self.LIMITE_INFERIOR) / (6 * desviacion_overall)
        
        # Cpk/Ppk - Capacidad real considerando centrado
        cpk, cpk_sup, cpk_inf = self.calcular_cpk(todos_datos, desviacion_pooled)
        ppk, ppk_sup, ppk_inf = self.calcular_cpk(todos_datos, desviacion_overall)
        
        ppm, fuera_inf, fuera_sup = self.calcular_ppm(todos_datos)
        
        # Prueba de normalidad
        stat_sw, p_value_sw = stats.shapiro(todos_datos)
        
        # Asimetría y Curtosis
        asimetria = stats.skew(todos_datos)
        curtosis = stats.kurtosis(todos_datos)
        
        return {
            'n_datos': len(todos_datos),
            'n_subgrupos': len(self.subgrupos),
            'n_lotes': len(self.lotes),
            'media': media,
            'mediana': mediana,
            'desviacion_overall': desviacion_overall,  # Para Pp
            'desviacion_pooled': desviacion_pooled,    # Para Cp
            'varianza': varianza_overall,
            'minimo': minimo,
            'maximo': maximo,
            'rango': rango,
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
            'asimetria': asimetria,
            'curtosis': curtosis,
            'cp': cp_potencial,        # Cp con desviación pooled
            'cpk': cpk,                # Cpk con desviación pooled
            'pp': pp_potencial,        # Pp con desviación overall
            'ppk': ppk,                # Ppk con desviación overall
            'ppm': ppm,
            'fuera_inferior': fuera_inf * 100,
            'fuera_superior': fuera_sup * 100,
            'normalidad_p_value': p_value_sw,
            'es_normal': p_value_sw > 0.05,
            'dentro_espec': (1 - (fuera_inf + fuera_sup)) * 100
        }
    
    def calcular_cpk(self, datos, desviacion):
        """Calcula índice de capacidad del proceso Cpk/Ppk"""
        media = np.mean(datos)
        
        cpk_superior = (self.LIMITE_SUPERIOR - media) / (3 * desviacion)
        cpk_inferior = (media - self.LIMITE_INFERIOR) / (3 * desviacion)
        cpk = min(cpk_superior, cpk_inferior)
        
        return cpk, cpk_superior, cpk_inferior
    
    def calcular_ppm(self, datos):
        """Calcula Partes Por Millón fuera de especificación"""
        fuera_inferior = np.sum(datos < self.LIMITE_INFERIOR) / len(datos)
        fuera_superior = np.sum(datos > self.LIMITE_SUPERIOR) / len(datos)
        total_fuera = fuera_inferior + fuera_superior
        ppm = total_fuera * 1_000_000
        
        return ppm, fuera_inferior, fuera_superior
    
    def generar_graficas_minitab(self, stats_dict):
        """Genera 6 gráficas profesionales tipo Minitab con indicadores de capacidad"""
        todos_datos = self.matriz_concentraciones.values.flatten()
        todos_datos = todos_datos[~np.isnan(todos_datos)]
        media = stats_dict['media']
        
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 18))
        
        # 1. HISTOGRAMA + CURVA NORMAL CON INDICADORES DE CAPACIDAD
        n, bins, patches = ax1.hist(todos_datos, bins=15, density=True, alpha=0.7, 
                                   color='skyblue', edgecolor='black', label='Datos')
        
        # Curva normal teórica
        x = np.linspace(media - 4*stats_dict['desviacion_overall'], media + 4*stats_dict['desviacion_overall'], 200)
        y = stats.norm.pdf(x, media, stats_dict['desviacion_overall'])
        ax1.plot(x, y, 'r-', linewidth=2, label='Distribución Normal')
        
        # Límites de especificación
        ax1.axvline(self.LIMITE_INFERIOR, color='red', linestyle='--', linewidth=2, label='Límites ESPEC')
        ax1.axvline(self.LIMITE_SUPERIOR, color='red', linestyle='--', linewidth=2)
        ax1.axvline(self.OBJETIVO, color='green', linestyle='-', linewidth=2, label='Objetivo')
        ax1.axvline(media, color='blue', linestyle=':', linewidth=2, label=f'Media: {media:.4f}')
        
        ax1.set_xlabel('Concentración (M)')
        ax1.set_ylabel('Densidad de Probabilidad')
        ax1.set_title('DISTRIBUCIÓN - Campana de Gauss con Límites')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Añadir indicadores de capacidad en el histograma
        capacidad_text = f"Capacidad del Proceso:\n"
        capacidad_text += f"Cp: {stats_dict['cp']:.2f} | Cpk: {stats_dict['cpk']:.2f}\n"
        capacidad_text += f"Pp: {stats_dict['pp']:.2f} | Ppk: {stats_dict['ppk']:.2f}\n"
        capacidad_text += f"Dentro ESPEC: {stats_dict['dentro_espec']:.1f}%"
        
        ax1.text(0.02, 0.98, capacidad_text, transform=ax1.transAxes, 
                bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8),
                verticalalignment='top', fontsize=10)

        # 2. GRÁFICO DE DISPERSIÓN con LÍMITES Y CAPACIDAD
        ax2.scatter(range(len(todos_datos)), todos_datos, alpha=0.6, s=20, color='blue')
        ax2.axhline(self.OBJETIVO, color='green', linestyle='-', linewidth=2, label='Objetivo (0.10M)')
        ax2.axhline(self.LIMITE_INFERIOR, color='red', linestyle='--', linewidth=2, label='Límites (0.08-0.12M)')
        ax2.axhline(self.LIMITE_SUPERIOR, color='red', linestyle='--', linewidth=2)
        ax2.axhline(media, color='blue', linestyle=':', linewidth=2, label=f'Media: {media:.4f}M')
        
        # Área entre límites
        ax2.fill_between(range(len(todos_datos)), self.LIMITE_INFERIOR, self.LIMITE_SUPERIOR, 
                        alpha=0.1, color='green', label='Zona de Aceptación')
        
        ax2.set_xlabel('Número de Medición Individual')
        ax2.set_ylabel('Concentración (M)')
        ax2.set_title('GRÁFICO DE DISPERSIÓN - Todas las Mediciones')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Añadir indicadores en gráfico de dispersión
        disp_text = f"Capacidad:\nCpk: {stats_dict['cpk']:.2f}\nPpk: {stats_dict['ppk']:.2f}"
        ax2.text(0.02, 0.98, disp_text, transform=ax2.transAxes,
                bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.8),
                verticalalignment='top', fontsize=10)

        # 3. ANÁLISIS DE CAPACIDAD DUAL (Cp vs Pp) CON INDICADORES
        x_capa = np.linspace(media - 4*stats_dict['desviacion_overall'], media + 4*stats_dict['desviacion_overall'], 200)
        y_capa = stats.norm.pdf(x_capa, media, stats_dict['desviacion_overall'])
        
        ax3.plot(x_capa, y_capa, 'b-', linewidth=2, label='Distribución Real')
        ax3.fill_between(x_capa, y_capa, where=(x_capa >= self.LIMITE_INFERIOR) & 
                        (x_capa <= self.LIMITE_SUPERIOR), color='lightgreen', alpha=0.5, 
                        label=f'Dentro ESPEC: {stats_dict["dentro_espec"]:.1f}%')
        
        if stats_dict['fuera_inferior'] > 0:
            ax3.fill_between(x_capa, y_capa, where=(x_capa < self.LIMITE_INFERIOR), 
                            color='red', alpha=0.5, label=f'Fuera LI: {stats_dict["fuera_inferior"]:.1f}%')
        
        if stats_dict['fuera_superior'] > 0:
            ax3.fill_between(x_capa, y_capa, where=(x_capa > self.LIMITE_SUPERIOR), 
                            color='red', alpha=0.5, label=f'Fuera LS: {stats_dict["fuera_superior"]:.1f}%')
        
        ax3.axvline(self.LIMITE_INFERIOR, color='red', linestyle='--', linewidth=2)
        ax3.axvline(self.LIMITE_SUPERIOR, color='red', linestyle='--', linewidth=2)
        ax3.axvline(media, color='blue', linestyle='-', linewidth=2, label=f'Media: {media:.4f}M')
        ax3.axvline(self.OBJETIVO, color='green', linestyle='-', linewidth=2, label='Objetivo')
        
        ax3.set_xlabel('Concentración (M)')
        ax3.set_ylabel('Densidad')
        ax3.set_title('ANÁLISIS DE CAPACIDAD - Áreas Fuera de Especificación')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Añadir indicadores de capacidad detallados
        capa_text = f"🔷 CAPACIDAD WITHIN (Cp):\n"
        capa_text += f"Cp: {stats_dict['cp']:.2f}\n"
        capa_text += f"Cpk: {stats_dict['cpk']:.2f}\n\n"
        capa_text += f"🔶 CAPACIDAD OVERALL (Pp):\n"
        capa_text += f"Pp: {stats_dict['pp']:.2f}\n"
        capa_text += f"Ppk: {stats_dict['ppk']:.2f}"
        
        ax3.text(0.02, 0.98, capa_text, transform=ax3.transAxes,
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
                verticalalignment='top', fontsize=9)

        # 4. GRÁFICO DE PROBABILIDAD NORMAL (Q-Q Plot) CON CAPACIDAD
        stats.probplot(todos_datos, dist="norm", plot=ax4)
        ax4.set_title('GRÁFICO DE PROBABILIDAD NORMAL - Prueba de Normalidad')
        ax4.grid(True, alpha=0.3)
        
        # Añadir resultado de prueba de normalidad y capacidad
        normalidad_text = f"Shapiro-Wilk: p = {stats_dict['normalidad_p_value']:.4f}\n"
        normalidad_text += f"¿Normal? {'SÍ' if stats_dict['es_normal'] else 'NO'}\n"
        normalidad_text += f"Asimetría: {stats_dict['asimetria']:.3f}\n"
        normalidad_text += f"Curtosis: {stats_dict['curtosis']:.3f}\n"
        normalidad_text += f"Cpk: {stats_dict['cpk']:.2f} | Ppk: {stats_dict['ppk']:.2f}"
        ax4.text(0.05, 0.95, normalidad_text, transform=ax4.transAxes, 
                bbox=dict(boxstyle="round", facecolor="wheat"), verticalalignment='top', fontsize=9)
        
        # 5. GRÁFICO DE CAJA POR LOTE CON CAPACIDAD
        datos_por_lote = [self.matriz_concentraciones[lote].dropna().values for lote in self.lotes]
        ax5.boxplot(datos_por_lote, vert=True, patch_artist=True, labels=self.lotes,
                   boxprops=dict(facecolor='lightblue', color='blue'),
                   medianprops=dict(color='red', linewidth=2))
        ax5.set_ylabel('Concentración (M)')
        ax5.set_title('GRÁFICO DE CAJA - Distribución por Lote')
        ax5.grid(True, alpha=0.3)
        
        # Añadir líneas de especificación al boxplot
        ax5.axhline(self.LIMITE_INFERIOR, color='red', linestyle='--', alpha=0.7, label='Límites')
        ax5.axhline(self.LIMITE_SUPERIOR, color='red', linestyle='--', alpha=0.7)
        ax5.legend()
        plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Añadir indicadores de capacidad en boxplot
        box_text = f"Capacidad Global:\n"
        box_text += f"Cp: {stats_dict['cp']:.2f} | Cpk: {stats_dict['cpk']:.2f}\n"
        box_text += f"PPM: {stats_dict['ppm']:,.0f}"
        ax5.text(0.02, 0.98, box_text, transform=ax5.transAxes,
                bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.8),
                verticalalignment='top', fontsize=9)
        
        # 6. GRÁFICO DE CONTROL (Media por subgrupo) CON CAPACIDAD
        medias_por_subgrupo = self.matriz_concentraciones.mean(axis=1)
        ax6.plot(medias_por_subgrupo.values, 'o-', color='purple', alpha=0.7, label='Media por subgrupo')
        ax6.axhline(self.OBJETIVO, color='green', linestyle='-', linewidth=2, label='Objetivo')
        ax6.axhline(self.LIMITE_INFERIOR, color='red', linestyle='--', linewidth=1, label='Límites')
        ax6.axhline(self.LIMITE_SUPERIOR, color='red', linestyle='--', linewidth=1)
        ax6.axhline(media, color='blue', linestyle=':', linewidth=2, label='Media global')
        
        ax6.set_xlabel('Subgrupo')
        ax6.set_ylabel('Concentración Promedio (M)')
        ax6.set_title('GRÁFICO DE CONTROL - Medias por Subgrupo')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Añadir indicadores en gráfico de control
        control_text = f"Variación:\n"
        control_text += f"Within (Cp): {stats_dict['cp']:.2f}\n"
        control_text += f"Overall (Pp): {stats_dict['pp']:.2f}\n"
        control_text += f"Diferencia: {stats_dict['pp'] - stats_dict['cp']:.2f}"
        ax6.text(0.02, 0.98, control_text, transform=ax6.transAxes,
                bbox=dict(boxstyle="round", facecolor="lightcoral", alpha=0.8),
                verticalalignment='top', fontsize=9)
        
        plt.tight_layout()
        plt.show()
    
    def generar_reporte_estadistico(self, stats_dict):
        """Genera reporte estadístico completo diferenciando Cp vs Pp"""
        print("\n" + "="*80)
        print("📊 REPORTE ESTADÍSTICO AVANZADO - Cp vs Pp CORRECTO")
        print("="*80)
        
        print(f"\n🎯 PARÁMETROS DE ESPECIFICACIÓN:")
        print(f"   Límite Inferior (LI): {self.LIMITE_INFERIOR:.3f} M")
        print(f"   Objetivo: {self.OBJETIVO:.3f} M")
        print(f"   Límite Superior (LS): {self.LIMITE_SUPERIOR:.3f} M")
        
        print(f"\n📈 ESTADÍSTICAS DESCRIPTIVAS:")
        print(f"   Total de datos: {stats_dict['n_datos']}")
        print(f"   Subgrupos: {stats_dict['n_subgrupos']} | Lotes: {stats_dict['n_lotes']}")
        print(f"   Media: {stats_dict['media']:.4f} M")
        print(f"   Mediana: {stats_dict['mediana']:.4f} M")
        print(f"   Desviación Overall (Pp): {stats_dict['desviacion_overall']:.4f} M")
        print(f"   Desviación Pooled (Cp): {stats_dict['desviacion_pooled']:.4f} M")
        print(f"   Mínimo: {stats_dict['minimo']:.4f} M | Máximo: {stats_dict['maximo']:.4f} M")
        
        print(f"\n📊 ANÁLISIS DE CAPACIDAD DEL PROCESO:")
        print(f"   🔷 CAPACIDAD POTENCIAL (Dentro de subgrupos):")
        print(f"      Cp: {stats_dict['cp']:.3f}  - Variación inherente del proceso")
        print(f"   🔶 CAPACIDAD REAL (Overall):")
        print(f"      Pp: {stats_dict['pp']:.3f}  - Variación total observada")
        
        print(f"\n   🔷 CAPACIDAD REAL AJUSTADA (Dentro de subgrupos):")
        print(f"      Cpk: {stats_dict['cpk']:.3f} - Considera centrado del proceso")
        print(f"   🔶 CAPACIDAD REAL AJUSTADA (Overall):")
        print(f"      Ppk: {stats_dict['ppk']:.3f} - Considera centrado del proceso")
        
        # Interpretación Cp/Cpk vs Pp/Ppk
        print(f"\n📋 INTERPRETACIÓN MINITAB:")
        diferencia = stats_dict['pp'] - stats_dict['cp']
        if diferencia > 0.2:
            print(f"   ⚠️  GRAN DIFERENCIA Cp vs Pp: Hay variación ENTRE subgrupos")
            print(f"   💡 Recomendación: Mejorar consistencia entre subgrupos")
        elif diferencia > 0.1:
            print(f"   📍 MODERADA DIFERENCIA Cp vs Pp: Alguna variación entre subgrupos")
        else:
            print(f"   ✅ PEQUEÑA DIFERENCIA Cp vs Pp: Proceso consistente entre subgrupos")
        
        # Interpretación Cpk
        cpk = stats_dict['cpk']
        if cpk >= 1.67:
            interpretacion = "✅ EXCELENTE - Proceso de clase mundial"
        elif cpk >= 1.33:
            interpretacion = "✅ BUENO - Proceso adecuado"
        elif cpk >= 1.00:
            interpretacion = "⚠️  MARGINAL - Requiere mejora"
        elif cpk >= 0.67:
            interpretacion = "❌ INADECUADO - Requiere acción inmediata"
        else:
            interpretacion = "💀 INACEPTABLE - Proceso fuera de control"
        
        print(f"   Interpretación Cpk: {interpretacion}")
        
        print(f"\n⚠️  ANÁLISIS DE DEFECTOS:")
        print(f"   Muestras fuera LI: {stats_dict['fuera_inferior']:.2f}%")
        print(f"   Muestras fuera LS: {stats_dict['fuera_superior']:.2f}%")
        print(f"   Total dentro especificación: {stats_dict['dentro_espec']:.2f}%")
        print(f"   PPM (Partes Por Millón): {stats_dict['ppm']:,.0f}")
        
        print(f"\n🎯 RECOMENDACIONES ESTRATÉGICAS:")
        if stats_dict['cp'] > stats_dict['pp']:
            print(f"   • 🔧 PRIORIDAD: Reducir variación ENTRE subgrupos")
        else:
            print(f"   • 🔧 PRIORIDAD: Reducir variación DENTRO de subgrupos")
        
        if stats_dict['cpk'] < stats_dict['cp']:
            print(f"   • 🎯 CENTRADO: Mejorar centrado del proceso (Cpk < Cp)")
        else:
            print(f"   • ✅ CENTRADO: Proceso bien centrado")
    
    def analizar_completo(self):
        """Ejecuta análisis completo con matriz de concentraciones"""
        if not self.cargar_matriz_concentraciones():
            return
        
        print("\n🧮 Calculando estadísticas avanzadas con desviación POOLED...")
        stats_dict = self.calcular_estadisticas_avanzadas()
        
        # Generar reporte
        self.generar_reporte_estadistico(stats_dict)
        
        # Generar gráficas
        print(f"\n📈 Generando 6 gráficas Minitab avanzadas...")
        self.generar_graficas_minitab(stats_dict)
        
        # Guardar reporte estadístico
        df_reporte = pd.DataFrame([stats_dict])
        df_reporte.to_excel('reporte_estadistico_avanzado.xlsx', index=False)
        print(f"\n💾 Reporte estadístico guardado en: 'reporte_estadistico_avanzado.xlsx'")
        
        return stats_dict

# 🎯 EJECUCIÓN DEL ANALIZADOR
if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISIS ESTADÍSTICO AVANZADO - VERSIÓN 2")
    print("📝 Nota: Este análisis usa la MATRIZ de concentraciones y calcula Cp/Pp correctamente")
    
    analizador = AnalizadorEstadisticoProcesos()
    resultados = analizador.analizar_completo()
    
    if resultados:
        print(f"\n{'='*80}")
        print("🎉 ANÁLISIS ESTADÍSTICO COMPLETADO CON ÉXITO!")
        print(f"{'='*80}")
        print("📊 6 Gráficas Minitab generadas")
        print("📋 Reporte Cp vs Pp diferenciado")
        print("💾 Todos los datos guardados para trazabilidad")
        print(f"📈 {resultados['n_datos']} datos analizados en {resultados['n_subgrupos']} subgrupos")
        print(f"🔷 Cp (Within): {resultados['cp']:.3f} | Cpk: {resultados['cpk']:.3f}")
        print(f"🔶 Pp (Overall): {resultados['pp']:.3f} | Ppk: {resultados['ppk']:.3f}")
        print(f"📊 Dentro de especificación: {resultados['dentro_espec']:.1f}%")
        print(f"{'='*80}")