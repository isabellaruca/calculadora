import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import statistics
import sympy as sp
import json
import pandas as pd
from datetime import datetime
from matplotlib.patches import Rectangle

# Configuración de la página
st.set_page_config(
    page_title="Calculadora Científica Avanzada",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B9D;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #FF9EC0;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .calc-button {
        height: 70px;
        border-radius: 15px;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 5px 0;
        background-color: #FFD1DC;
        color: #D94A7A;
        border: 2px solid #FF9EC0;
    }
    .calc-button:hover {
        background-color: #FF9EC0;
        color: white;
    }
    .result-display {
        background-color: #FFF5F7;
        border: 2px solid #FFD1DC;
        border-radius: 10px;
        padding: 15px;
        font-size: 1.5rem;
        color: #D94A7A;
        margin-bottom: 15px;
        min-height: 80px;
    }
    .history-item {
        background-color: #FFF5F7;
        border-left: 5px solid #FF9EC0;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .stButton>button {
        width: 100%;
        height: 70px;
        border-radius: 15px;
        font-size: 1.5rem;
        font-weight: bold;
        background-color: #FFD1DC;
        color: #D94A7A;
        border: 2px solid #FF9EC0;
    }
    .stButton>button:hover {
        background-color: #FF9EC0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización del estado de la sesión
if 'current_expression' not in st.session_state:
    st.session_state.current_expression = "0"
if 'history' not in st.session_state:
    st.session_state.history = []
if 'precision' not in st.session_state:
    st.session_state.precision = 10

# Funciones de la calculadora
def add_to_expression(value):
    """Añade un valor a la expresión actual"""
    if st.session_state.current_expression == "0" and value not in "().":
        st.session_state.current_expression = value
    else:
        st.session_state.current_expression += value

def clear_expression():
    """Limpia la expresión actual"""
    st.session_state.current_expression = "0"

def calculate_result():
    """Calcula el resultado de la expresión actual"""
    try:
        expression = st.session_state.current_expression
        
        # Preparar el entorno de evaluación seguro
        safe_dict = {
            "__builtins__": {},
            "abs": abs, "round": round, "min": min, "max": max,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "log": math.log, "log10": math.log10, "log2": math.log2,
            "exp": math.exp, "sqrt": math.sqrt, "cbrt": lambda x: x**(1/3),
            "pi": math.pi, "e": math.e, "factorial": math.factorial
        }
        
        # Procesar factoriales
        if '!' in expression:
            import re
            pattern = r'(\d+)!'
            expression = re.sub(pattern, r'factorial(\1)', expression)
        
        # Evaluar la expresión
        result = eval(expression, safe_dict)
        
        # Formatear resultado según precisión
        if isinstance(result, float):
            result = round(result, st.session_state.precision)
        
        # Añadir al historial
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.insert(0, f"[{timestamp}] {st.session_state.current_expression} = {result}")
        
        # Limitar el historial a 20 entradas
        if len(st.session_state.history) > 20:
            st.session_state.history = st.session_state.history[:20]
        
        # Actualizar la expresión con el resultado
        st.session_state.current_expression = str(result)
        
    except Exception as e:
        st.error(f"Error en el cálculo: {str(e)}")

def toggle_sign():
    """Cambia el signo de la expresión actual"""
    current = st.session_state.current_expression
    if current.startswith('-'):
        st.session_state.current_expression = current[1:]
    else:
        st.session_state.current_expression = '-' + current

# Interfaz principal
st.markdown('<div class="main-header">🧮 Calculadora Científica Avanzada</div>', unsafe_allow_html=True)

# Sidebar para configuración e historial
with st.sidebar:
    st.markdown('<div class="sub-header">⚙️ Configuración</div>', unsafe_allow_html=True)
    
    # Precisión decimal
    st.session_state.precision = st.slider("Precisión decimal", min_value=2, max_value=15, value=st.session_state.precision)
    
    # Exportar historial
    if st.button("📤 Exportar Historial"):
        if st.session_state.history:
            history_text = "=== HISTORIAL DE CALCULADORA AVANZADA ===\n\n"
            for entry in st.session_state.history:
                history_text += entry + "\n"
            
            st.download_button(
                label="Descargar Historial",
                data=history_text,
                file_name=f"historial_calculadora_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("No hay historial para exportar")
    
    # Limpiar historial
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.history = []
        st.success("Historial limpiado")
    
    st.markdown('<div class="sub-header">📚 Historial</div>', unsafe_allow_html=True)
    
    # Mostrar historial
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history[:10]):
            st.markdown(f'<div class="history-item">{entry}</div>', unsafe_allow_html=True)
    else:
        st.info("No hay cálculos en el historial")

# Contenido principal con pestañas
tab1, tab2, tab3, tab4 = st.tabs(["🧮 Calculadora", "📊 Gráficos", "📈 Estadísticas", "🔬 Avanzado"])

# Pestaña de Calculadora
with tab1:
    st.markdown('<div class="sub-header">Calculadora Científica</div>', unsafe_allow_html=True)
    
    # Pantalla de la calculadora
    st.markdown(f'<div class="result-display">{st.session_state.current_expression}</div>', unsafe_allow_html=True)
    
    # Botones de la calculadora
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("sin", key="sin"):
            add_to_expression("sin(")
        if st.button("cos", key="cos"):
            add_to_expression("cos(")
        if st.button("tan", key="tan"):
            add_to_expression("tan(")
        if st.button("π", key="pi"):
            add_to_expression(str(math.pi))
        if st.button("7", key="7"):
            add_to_expression("7")
        if st.button("4", key="4"):
            add_to_expression("4")
        if st.button("1", key="1"):
            add_to_expression("1")
        if st.button("0", key="0"):
            add_to_expression("0")
    
    with col2:
        if st.button("asin", key="asin"):
            add_to_expression("asin(")
        if st.button("acos", key="acos"):
            add_to_expression("acos(")
        if st.button("atan", key="atan"):
            add_to_expression("atan(")
        if st.button("e", key="e"):
            add_to_expression(str(math.e))
        if st.button("8", key="8"):
            add_to_expression("8")
        if st.button("5", key="5"):
            add_to_expression("5")
        if st.button("2", key="2"):
            add_to_expression("2")
        if st.button(".", key="dot"):
            add_to_expression(".")
    
    with col3:
        if st.button("ln", key="ln"):
            add_to_expression("log(")
        if st.button("log", key="log"):
            add_to_expression("log10(")
        if st.button("e^x", key="exp"):
            add_to_expression("exp(")
        if st.button("√", key="sqrt"):
            add_to_expression("sqrt(")
        if st.button("9", key="9"):
            add_to_expression("9")
        if st.button("6", key="6"):
            add_to_expression("6")
        if st.button("3", key="3"):
            add_to_expression("3")
        if st.button("±", key="sign"):
            toggle_sign()
    
    with col4:
        if st.button("x²", key="square"):
            add_to_expression("**2")
        if st.button("x³", key="cube"):
            add_to_expression("**3")
        if st.button("x^y", key="power"):
            add_to_expression("**")
        if st.button("x!", key="factorial"):
            add_to_expression("!")
        if st.button("/", key="divide"):
            add_to_expression("/")
        if st.button("*", key="multiply"):
            add_to_expression("*")
        if st.button("-", key="subtract"):
            add_to_expression("-")
        if st.button("+", key="add"):
            add_to_expression("+")
    
    with col5:
        if st.button("(", key="open_paren"):
            add_to_expression("(")
        if st.button(")", key="close_paren"):
            add_to_expression(")")
        if st.button("C", key="clear"):
            clear_expression()
        if st.button("=", key="equals"):
            calculate_result()
        if st.button("|x|", key="abs"):
            add_to_expression("abs(")
        if st.button("mod", key="mod"):
            add_to_expression("%")
        if st.button("10^x", key="10power"):
            add_to_expression("10**(")
        if st.button("2^x", key="2power"):
            add_to_expression("2**(")

# Pestaña de Gráficos
with tab2:
    st.markdown('<div class="sub-header">Gráfico de Funciones</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        function_input = st.text_input("Función f(x):", value="sin(x)", placeholder="Ej: sin(x), x**2, log(x)")
        
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            x_min = st.number_input("X mínimo:", value=-10.0, step=1.0)
        with col1b:
            x_max = st.number_input("X máximo:", value=10.0, step=1.0)
        with col1c:
            num_points = st.number_input("Número de puntos:", value=1000, min_value=100, max_value=10000)
    
    with col2:
        st.markdown("**Opciones del gráfico**")
        show_grid = st.checkbox("Mostrar cuadrícula", value=True)
        show_legend = st.checkbox("Mostrar leyenda", value=True)
    
    if st.button("📈 Graficar Función"):
        try:
            # Crear array de x
            x = np.linspace(x_min, x_max, num_points)
            
            # Preparar la función para evaluación
            func_str = function_input.replace('sin', 'np.sin')
            func_str = func_str.replace('cos', 'np.cos')
            func_str = func_str.replace('tan', 'np.tan')
            func_str = func_str.replace('log', 'np.log')
            func_str = func_str.replace('exp', 'np.exp')
            func_str = func_str.replace('sqrt', 'np.sqrt')
            func_str = func_str.replace('pi', 'np.pi')
            func_str = func_str.replace('e', 'np.e')
            
            # Evaluar la función
            y = eval(func_str, {"np": np, "x": x})
            
            # Crear gráfico con matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, color='#FF6B9D', linewidth=2, label=f'f(x) = {function_input}')
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Gráfico de f(x) = {function_input}')
            
            if show_grid:
                ax.grid(True, alpha=0.3)
            if show_legend:
                ax.legend()
            
            # Estilo pastel
            ax.set_facecolor('#FFF5F7')
            fig.patch.set_facecolor('#FFF9FA')
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error al graficar: {str(e)}")

# Pestaña de Estadísticas
with tab3:
    st.markdown('<div class="sub-header">Análisis Estadístico</div>', unsafe_allow_html=True)
    
    # Entrada de datos
    data_input = st.text_area("Introduce los datos (separados por comas):", 
                             placeholder="Ej: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
                             height=100)
    
    if st.button("📊 Analizar Datos"):
        if data_input:
            try:
                # Procesar datos
                data = [float(x.strip()) for x in data_input.split(',') if x.strip()]
                
                if len(data) < 2:
                    st.warning("Se necesitan al menos 2 datos para el análisis")
                else:
                    # Calcular estadísticas
                    stats = {
                        "Cantidad de datos": len(data),
                        "Media": statistics.mean(data),
                        "Mediana": statistics.median(data),
                        "Moda": statistics.mode(data) if len(set(data)) < len(data) else "No hay moda única",
                        "Desviación Estándar": statistics.stdev(data) if len(data) > 1 else 0,
                        "Varianza": statistics.variance(data) if len(data) > 1 else 0,
                        "Mínimo": min(data),
                        "Máximo": max(data),
                        "Rango": max(data) - min(data)
                    }
                    
                    # Mostrar estadísticas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Estadísticas Descriptivas**")
                        for key, value in list(stats.items())[:5]:
                            if isinstance(value, float):
                                st.info(f"{key}: {value:.{st.session_state.precision}f}")
                            else:
                                st.info(f"{key}: {value}")
                    
                    with col2:
                        st.markdown("**Medidas de Dispersión**")
                        for key, value in list(stats.items())[5:]:
                            if isinstance(value, float):
                                st.info(f"{key}: {value:.{st.session_state.precision}f}")
                            else:
                                st.info(f"{key}: {value}")
                    
                    # Crear visualizaciones
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                    
                    # Histograma
                    ax1.hist(data, bins=min(20, len(data)//2), color='#FF9EC0', alpha=0.7, edgecolor='white')
                    ax1.set_title('Histograma de Frecuencias')
                    ax1.set_xlabel('Valores')
                    ax1.set_ylabel('Frecuencia')
                    ax1.grid(True, alpha=0.3)
                    
                    # Diagrama de caja
                    ax2.boxplot(data, patch_artist=True, 
                               boxprops=dict(facecolor='#FF6B9D', color='black'),
                               medianprops=dict(color='white'))
                    ax2.set_title('Diagrama de Caja')
                    ax2.set_ylabel('Valores')
                    
                    # Estilo pastel
                    ax1.set_facecolor('#FFF5F7')
                    ax2.set_facecolor('#FFF5F7')
                    fig.patch.set_facecolor('#FFF9FA')
                    
                    st.pyplot(fig)
                    
            except Exception as e:
                st.error(f"Error en el análisis: {str(e)}")
        else:
            st.warning("Por favor, introduce algunos datos para analizar")

# Pestaña Avanzado
with tab4:
    st.markdown('<div class="sub-header">Cálculo Simbólico y Avanzado</div>', unsafe_allow_html=True)
    
    # Derivadas
    st.markdown("**Cálculo de Derivadas**")
    col1, col2 = st.columns([3, 1])
    with col1:
        derivative_input = st.text_input("Función para derivar:", placeholder="x**2 + 3*x + 1")
    with col2:
        if st.button("Calcular Derivada"):
            if derivative_input:
                try:
                    x = sp.Symbol('x')
                    expr = sp.sympify(derivative_input)
                    derivative = sp.diff(expr, x)
                    st.success(f"Derivada de {expr}: {derivative}")
                    st.latex(f"\\frac{{d}}{{dx}}({sp.latex(expr)}) = {sp.latex(derivative)}")
                except Exception as e:
                    st.error(f"Error en el cálculo de la derivada: {str(e)}")
    
    # Integrales
    st.markdown("**Cálculo de Integrales**")
    col1, col2 = st.columns([3, 1])
    with col1:
        integral_input = st.text_input("Función para integrar:", placeholder="x**2")
    with col2:
        if st.button("Calcular Integral"):
            if integral_input:
                try:
                    x = sp.Symbol('x')
                    expr = sp.sympify(integral_input)
                    integral = sp.integrate(expr, x)
                    st.success(f"Integral de {expr}: {integral} + C")
                    st.latex(f"\\int ({sp.latex(expr)})  dx = {sp.latex(integral)} + C")
                except Exception as e:
                    st.error(f"Error en el cálculo de la integral: {str(e)}")
    
    # Límites
    st.markdown("**Cálculo de Límites**")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        limit_input = st.text_input("Función para el límite:", placeholder="sin(x)/x")
    with col2:
        limit_point = st.text_input("x →", placeholder="0")
    with col3:
        if st.button("Calcular Límite"):
            if limit_input and limit_point:
                try:
                    x = sp.Symbol('x')
                    expr = sp.sympify(limit_input)
                    point = sp.sympify(limit_point)
                    limit = sp.limit(expr, x, point)
                    st.success(f"Límite de {expr} cuando x → {point}: {limit}")
                    st.latex(f"\\lim_{{x \\to {sp.latex(point)}}} ({sp.latex(expr)}) = {sp.latex(limit)}")
                except Exception as e:
                    st.error(f"Error en el cálculo del límite: {str(e)}")

# Información de la aplicación
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #FF6B9D;">
    <p>Calculadora Científica Avanzada - Desarrollada con Streamlit</p>
    <p>© 2023 - Todos los derechos reservados</p>
</div>
""", unsafe_allow_html=True)