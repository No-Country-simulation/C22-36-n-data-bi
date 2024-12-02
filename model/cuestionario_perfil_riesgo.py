import streamlit as st
import numpy as np
import pandas as pd

# Import the portfolio analysis classes
from data_loader import DataLoader
from portfolio_analysis import PortfolioAnalyzer, CompoundPortfolioAnalyzer
from ml_predictor import PortfolioPredictor

# Inicialización de variables de estado
if 'started' not in st.session_state:
    st.session_state.started = False
if 'section' not in st.session_state:
    st.session_state.section = 1
if 'score_section_1' not in st.session_state:
    st.session_state.score_section_1 = 0
if 'score_section_2' not in st.session_state:
    st.session_state.score_section_2 = 0
if 'score_section_3' not in st.session_state:
    st.session_state.score_section_3 = 0
if 'submitted_section_1' not in st.session_state:
    st.session_state.submitted_section_1 = False
if 'submitted_section_2' not in st.session_state:
    st.session_state.submitted_section_2 = False


def iniciar_cuestionario():
    st.session_state.started = True
    st.rerun()

# Resto de funciones existentes
def calcular_perfil(total_score):
    if total_score <= 18:
        return "Conservador", "80% Bonos, 20% ETFs"
    elif 19 <= total_score <= 27:
        return "Moderado", "40% Bonos, 40% ETFs, 20% Acciones"
    elif 28 <= total_score <= 36:
        return "Agresivo", "10% Bonos, 30% ETFs, 50% Acciones, 10% Futuros"
    else:
        return "Muy Agresivo", "60% Acciones, 20% Futuros, 20% Criptomonedas"

def cambiar_seccion(nueva_seccion):
    st.session_state.section = nueva_seccion

def reiniciar_cuestionario():
    st.session_state.started = False
    st.session_state.section = 1
    st.session_state.score_section_1 = 0
    st.session_state.score_section_2 = 0
    st.session_state.score_section_3 = 0
    st.session_state.submitted_section_1 = False
    st.session_state.submitted_section_2 = False
    st.rerun()


# Add new functions for portfolio analysis
def analyze_portfolio(profile_weights):
    # Define portfolios as in main.py
    portfolios = {
        "Bonos": ["^IRX", "^FVX", "^TNX", "^TYX"],
        "ETFs": ["SPY", "QQQ", "VTI", "IVV", "XLV"],
        "Acciones": ["MSFT", "GOOGL", "O", "PG", "ISRG", "MDT", "JPM"],
        "Futuros": ["GC=F", "CL=F", "SI=F", "NQ=F", "ES=F"],
        "Criptomonedas": ["BTC-USD", "ETH-USD", "BNB-USD", "TRX-USD", "DOGE-USD"]
    }
    
    # Initialize data loader
    loader = DataLoader()
    portfolio_data = loader.process_portfolios(portfolios)
    
    # Analyze each portfolio
    portfolio_results = {}
    for name, data in portfolio_data.items():
        analyzer = PortfolioAnalyzer(data)
        returns, volatility = analyzer.calculate_metrics()
        optimal_weights = analyzer.optimize_weights()
        
        portfolio_results[name] = {
            'returns': returns,
            'volatility': volatility,
            'optimal_weights': optimal_weights
        }
    
    # Create and analyze the compound portfolio
    compound_analyzer = CompoundPortfolioAnalyzer(
        portfolio_data, 
        portfolio_weights=profile_weights
    )
    compound_metrics = compound_analyzer.get_compound_metrics()
    
    # Predictor for the compound portfolio
    compound_predictor = PortfolioPredictor(
        compound_analyzer.compound_returns, 
        weights=None  # Compound returns are already weighted
    )
    compound_predictor.train_model()
    
    # Predictions for the compound portfolio
    investment = 100000  # $100,000 initial
    compound_pred_3y = compound_predictor.predict_returns(investment, 3)
    compound_pred_5y = compound_predictor.predict_returns(investment, 5)
    compound_pred_10y = compound_predictor.predict_returns(investment, 10)
    
    return {
        'portfolio_results': portfolio_results,
        'compound_metrics': compound_metrics,
        'predictions': {
            '3y': compound_pred_3y,
            '5y': compound_pred_5y,
            '10y': compound_pred_10y
        }
    }

# Mapping of risk profiles to portfolio weights
RISK_PROFILE_WEIGHTS = {
    "Conservador": {"Bonos": 0.8, "ETFs": 0.2, "Acciones": 0, "Futuros": 0, "Criptomonedas": 0},
    "Moderado": {"Bonos": 0.4, "ETFs": 0.4, "Acciones": 0.2, "Futuros": 0, "Criptomonedas": 0},
    "Agresivo": {"Bonos": 0.1, "ETFs": 0.3, "Acciones": 0.5, "Futuros": 0.1, "Criptomonedas": 0},
    "Muy Agresivo": {"Bonos": 0, "ETFs": 0, "Acciones": 0.6, "Futuros": 0.2, "Criptomonedas": 0.2}
}

# Portada
if not st.session_state.started:
    st.title("Cuestionario de Perfil de Riesgo de Inversión")
    
    # Contenedor principal con padding
    main_container = st.container()
    with main_container:
        st.markdown("""
        ### ¿Qué es el Perfil de Riesgo?
        El perfil de riesgo del inversionista  nos ayuda a determinar qué estrategia de inversión 
        se adapta mejor a tus características personales y objetivos financieros.
        
        ### ¿Qué evaluamos?
        Este cuestionario analiza tres aspectos clave:
        1. **Necesidad de Riesgo**: Tus objetivos financieros y horizonte temporal
        2. **Capacidad de Riesgo**: Tu situación financiera actual
        3. **Tolerancia al Riesgo**: Tu actitud personal frente a las fluctuaciones del mercado
        
        ### Tiempo estimado: 5-10 minutos
        """)
        
        # Centrar el botón usando columnas
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Espacio antes del botón
            if st.button("Comenzar Cuestionario", key="start_button", use_container_width=True):
                iniciar_cuestionario()

# Si ya comenzó el cuestionario, mostrar el contenido original
elif st.session_state.started:
    # Título de la aplicación
    st.title("Cuestionario de Perfil de Riesgo de Inversión")

    # Indicador de progreso
    if st.session_state.section < 4:
        progress = (st.session_state.section - 1) / 3
        st.progress(progress)
        st.write(f"Sección {st.session_state.section} de 3")



    # Sección 1
    if st.session_state.section == 1:
        st.subheader("Sección 1: Necesidad de Riesgo")
        
        q1 = st.radio("¿Cuál es el objetivo principal de su inversión?", 
                    ["Preservar el capital", "Generar ingresos estables", "Aumentar el valor de su capital moderadamente", "Maximizar el crecimiento de su capital"],
                    key="q1")
        q2 = st.radio("¿Cuánto tiempo planea mantener su inversión?", 
                    ["Menos de 3 años", "Entre 3 y 5 años", "Entre 5 y 10 años", "Más de 10 años"],
                    key="q2")
        q3 = st.radio("¿Qué tasa de retorno esperada necesita para alcanzar sus metas financieras?", 
                    ["Menos del 4% anual", "Entre el 4% y el 6% anual", "Entre el 6% y el 10% anual", "Más del 10% anual"],
                    key="q3")
        
        if st.button("Siguiente", key="btn_section_1"):
            st.session_state.score_section_1 = 0
            st.session_state.score_section_1 += [1, 2, 3, 4][["Preservar el capital", "Generar ingresos estables", "Aumentar el valor de su capital moderadamente", "Maximizar el crecimiento de su capital"].index(q1)]
            st.session_state.score_section_1 += [1, 2, 3, 4][["Menos de 3 años", "Entre 3 y 5 años", "Entre 5 y 10 años", "Más de 10 años"].index(q2)]
            st.session_state.score_section_1 += [1, 2, 3, 4][["Menos del 4% anual", "Entre el 4% y el 6% anual", "Entre el 6% y el 10% anual", "Más del 10% anual"].index(q3)]
            st.session_state.submitted_section_1 = True
            cambiar_seccion(2)
            st.rerun()

    # Sección 2
    elif st.session_state.section == 2:
        st.subheader("Sección 2: Capacidad para Asumir Riesgos")
        
        q4 = st.radio("¿Cuál es su nivel de ingresos o ahorros adicionales?", 
                    ["Muy bajo", "Bajo", "Moderado", "Alto"],
                    key="q4")
        q5 = st.radio("¿Qué tan importantes son las distribuciones regulares de esta inversión para usted?", 
                    ["Críticas", "Moderadamente importantes", "Poco importantes", "No son importantes"],
                    key="q5")
        q6 = st.radio("Si su cartera perdiera el 20% de su valor, ¿cómo afectaría esto su situación financiera?", 
                    ["Sería catastrófico", "Sería un inconveniente significativo", "Podría manejarlo sin problemas graves", "No tendría impacto significativo"],
                    key="q6")
        
        if st.button("Siguiente", key="btn_section_2"):
            st.session_state.score_section_2 = 0
            st.session_state.score_section_2 += [1, 2, 3, 4][["Muy bajo", "Bajo", "Moderado", "Alto"].index(q4)]
            st.session_state.score_section_2 += [1, 2, 3, 4][["Críticas", "Moderadamente importantes", "Poco importantes", "No son importantes"].index(q5)]
            st.session_state.score_section_2 += [1, 2, 3, 4][["Sería catastrófico", "Sería un inconveniente significativo", "Podría manejarlo sin problemas graves", "No tendría impacto significativo"].index(q6)]
            st.session_state.submitted_section_2 = True
            cambiar_seccion(3)
            st.rerun()

    # Sección 3
    elif st.session_state.section == 3:
        st.subheader("Sección 3: Tolerancia Conductual al Riesgo")
        
        q7 = st.radio("¿Qué tan cómodo se siente al aceptar fluctuaciones en el valor de su inversión?", 
                    ["Muy incómodo", "Incómodo", "Moderadamente cómodo", "Muy cómodo"],
                    key="q7")
        q8 = st.radio("¿Qué haría si su inversión perdiera el 30% de su valor en el corto plazo?", 
                    ["Vendería inmediatamente para evitar más pérdidas", "Esperaría a que los mercados se recuperen", "Invertiría más para aprovechar los precios bajos"],
                    key="q8")
        q9 = st.radio("¿Qué tan familiarizado está con los conceptos y productos financieros?", 
                    ["Nada familiarizado", "Algo familiarizado", "Moderadamente informado", "Muy informado"],
                    key="q9")
        
        if st.button("Ver resultados", key="btn_section_3"):
            st.session_state.score_section_3 = 0
            st.session_state.score_section_3 += [1, 2, 3, 4][["Muy incómodo", "Incómodo", "Moderadamente cómodo", "Muy cómodo"].index(q7)]
            st.session_state.score_section_3 += [1, 3, 5][["Vendería inmediatamente para evitar más pérdidas", "Esperaría a que los mercados se recuperen", "Invertiría más para aprovechar los precios bajos"].index(q8)]
            st.session_state.score_section_3 += [1, 2, 3, 4][["Nada familiarizado", "Algo familiarizado", "Moderadamente informado", "Muy informado"].index(q9)]
            cambiar_seccion(4)
            st.rerun()

    # Sección 4 (Resultados)
    # En la sección donde se muestran los resultados del cuestionario (sección 4)
    elif st.session_state.section == 4:
        st.subheader("Resultados de tu Perfil de Riesgo")
        
        # Calcular resultados
        total_score = st.session_state.score_section_1 + st.session_state.score_section_2 + st.session_state.score_section_3
        perfil, portafolio = calcular_perfil(total_score)
        
        # Mostrar resultados en cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**Tu perfil de riesgo es:**")
            st.markdown(f"### {perfil}")
            
        with col2:
            st.success("**Estrategia de inversión sugerida:**")
            st.markdown(f"### {portafolio}")
        
        # Desglose de puntuaciones
        st.markdown("---")
        st.subheader("Desglose de tu evaluación")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Necesidad de Riesgo", f"{st.session_state.score_section_1} pts")
        with col2:
            st.metric("Capacidad de Riesgo", f"{st.session_state.score_section_2} pts")
        with col3:
            st.metric("Tolerancia al Riesgo", f"{st.session_state.score_section_3} pts")
        
        # Modificación: Quitar la línea anterior de Puntuación Total
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Puntuación Total", f"{total_score} pts")
        with col3:
            # Add a button to view portfolio analysis
            if st.button("Analizar Portafolio", key="btn_portfolio_analysis"):
                st.session_state.section = 5  # Nuevo estado para la sección de análisis de portafolio
                st.rerun()
        
        # Botón para reiniciar al final
        st.markdown("---")
        if st.button("Realizar nuevo cuestionario", key="btn_reinicio"):
            reiniciar_cuestionario()

    # Nueva sección para análisis de portafolio
    elif st.session_state.section == 5:
        st.title("Análisis Detallado de Portafolio")
        
        # Recuperar información del perfil y portafolio
        total_score = st.session_state.score_section_1 + st.session_state.score_section_2 + st.session_state.score_section_3
        perfil, portafolio = calcular_perfil(total_score)
        
        # Obtener pesos del portafolio
        portfolio_weights = RISK_PROFILE_WEIGHTS[perfil]
        
        # Realizar análisis de portafolio
        with st.spinner('Analizando portafolio...'):
            analysis_results = analyze_portfolio(portfolio_weights)
        
        # Contenido similar al análisis anterior...
        st.subheader("Métricas del Portafolio Compuesto")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Retorno Anual", f"{analysis_results['compound_metrics']['return'].iloc[0]:.2%}")
        with col2:
            st.metric("Volatilidad", f"{analysis_results['compound_metrics']['volatility'].iloc[0]:.2%}")
        with col3:
            st.metric("Ratio Sharpe", f"{analysis_results['compound_metrics']['sharpe_ratio'].iloc[0]:.2%}")
        
        # Predictions Visualization
        st.markdown("### Proyecciones de Inversión")
        
        # Create tabs for different prediction periods
        tab_3y, tab_5y, tab_10y = st.tabs(["3 Años", "5 Años", "10 Años"])
        
        prediction_periods = {
            "3 Años": analysis_results['predictions']['3y'],
            "5 Años": analysis_results['predictions']['5y'], 
            "10 Años": analysis_results['predictions']['10y']
        }
        
        # Plot for each period
        for period, pred_data in zip(["3 Años", "5 Años", "10 Años"], 
                                    [analysis_results['predictions']['3y'], 
                                    analysis_results['predictions']['5y'], 
                                    analysis_results['predictions']['10y']]):
            if period == "3 Años":
                with tab_3y:
                    st.line_chart(pred_data.set_index('Day')['Portfolio_Value'])
                    st.dataframe(pred_data)
            elif period == "5 Años":
                with tab_5y:
                    st.line_chart(pred_data.set_index('Day')['Portfolio_Value'])
                    st.dataframe(pred_data)
            else:
                with tab_10y:
                    st.line_chart(pred_data.set_index('Day')['Portfolio_Value'])
                    st.dataframe(pred_data)
        
        # Detailed portfolio composition
        st.markdown("### Composición del Portafolio")
        for name, portfolio in analysis_results['portfolio_results'].items():
            st.markdown(f"#### {name}")
            col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Retorno Anual", f"{portfolio['returns'].mean():.2%}")
        with col2:
            st.metric("Volatilidad", f"{portfolio['volatility'].mean():.2%}")
        with col3:
            st.metric("Peso Optimizado", f"{portfolio['optimal_weights']['weights'].mean():.2%}")
        
        # Botón para volver
        st.markdown("---")
        if st.button("Volver a Resultados", key="btn_volver_resultados"):
            st.session_state.section = 4
            st.rerun()
