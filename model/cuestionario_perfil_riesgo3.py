import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="PortfolioOp",
    page_icon="🏦",
    layout="wide" #"centered"
)

image_path = "./assets/logo.jpg"
# Import the necessary classes
from data_loader import DataLoader
from portfolio_analysis import PortfolioAnalyzer
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
force_download = st.sidebar.checkbox("Descargar datos nuevamente", value=False)
def reiniciar_cuestionario():
    st.session_state.started = False
    st.session_state.section = 1
    st.session_state.score_section_1 = 0
    st.session_state.score_section_2 = 0
    st.session_state.score_section_3 = 0
    st.session_state.submitted_section_1 = False
    st.session_state.submitted_section_2 = False
    st.rerun()
def run_portfolio_analysis(portfolio_allocation):
    """
    Run portfolio optimization and prediction based on allocation
    """
    # 1. Define portfolios
    portfolios = {
        "Bonos": ["^IRX", "^FVX", "^TNX", "^TYX"],
        "ETFs": ["SPY", "QQQ", "VTI", "IVV", "XLV"],
        "Acciones": ["MSFT", "GOOGL", "O", "PG", "ISRG", "MDT", "JPM"],
        "Futuros": ["GC=F", "CL=F", "SI=F", "NQ=F", "ES=F"],
        "Criptomonedas": ["BTC-USD", "ETH-USD", "BNB-USD", "TRX-USD", "DOGE-USD"]
    }

    # 2. Load data
    loader = DataLoader(start_date="2017-11-09", end_date="2024-10-31")
    portfolio_data = loader.process_portfolios(portfolios, force_download=force_download)

    # 3. Analyze and optimize each selected portfolio
    investment_total = 100000  # Initial capital
    results = {}

    for portfolio_name, allocation in portfolio_allocation.items():
        if allocation > 0 and portfolio_name in portfolio_data:
            # Skip if portfolio is empty
            if portfolio_data[portfolio_name].empty:
                st.warning(f"No data available for {portfolio_name} portfolio")
                continue

            # Perform analysis
            analyzer = PortfolioAnalyzer(portfolio_data[portfolio_name])
            
            # Calculate metrics
            returns, volatility = analyzer.calculate_metrics()
            
            # Optimize weights
            optimal_weights = analyzer.optimize_weights()
            
            # Calculate portfolio performance
            performance = analyzer.portfolio_performance(optimal_weights['weights'])
            
            # Predict returns
            investment = investment_total * allocation
            predictor = PortfolioPredictor(portfolio_data[portfolio_name], optimal_weights['weights'])
            predictor.train_model()
            
            # Predictions for different time horizons
            predictions = {
                3: predictor.predict_returns(investment, 3),
                5: predictor.predict_returns(investment, 5),
                10: predictor.predict_returns(investment, 10)
            }
            
            
            # Store results
            results[portfolio_name] = {
                'returns': returns,
                'volatility': volatility,
                'optimal_weights': optimal_weights,
                'performance': performance,
                'predictions': predictions
            }
            predictions_summary = {}
            for years, pred in predictions.items():
                final_value = pred['Portfolio_Value'].iloc[-1]
                total_return = (final_value - investment) / investment * 100
                predictions_summary[years] = {
                    'predictions': pred,
                    'initial_value': investment,  # Valor inicial del portafolio
                    'final_value': final_value,
                    'total_return': total_return
                }

            # Update the results dictionary
            results[portfolio_name]['predictions'] = predictions_summary
            
            


    return results


def display_portfolio_results(results):
    """
    Display portfolio analysis results in Streamlit
    """
    st.header("Análisis Detallado de Portafolio")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4= st.tabs([
        "Rendimientos y Volatilidad", 
        "Distribución de Pesos", 
        "Predicciones a Largo Plazo", 
        "Comparación de Rendimiento"
    ])
    
    
    with tab1:
        st.subheader("Rendimientos y Volatilidad por Activo")
        metrics_data = []
        for portfolio_name, portfolio_data in results.items():
            for asset, ret, vol in zip(
                portfolio_data['returns'].index, 
                portfolio_data['returns'], 
                portfolio_data['volatility']
            ):
                metrics_data.append({
                    'Portafolio': portfolio_name,
                    'Activo': asset,
                    'Rendimiento Anual (%)': ret * 100,
                    'Volatilidad Anual (%)': vol * 100
                })
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df.style.format({
            'Rendimiento Anual (%)': '{:.2f}%',
            'Volatilidad Anual (%)': '{:.2f}%'
        }))
    
    with tab2:
        st.subheader("Distribución de Pesos en Portafolios")
        fig, axes = plt.subplots(1, len(results), figsize=(15, 5))
        
        for i, (portfolio_name, portfolio_data) in enumerate(results.items()):
            weights = portfolio_data['optimal_weights']['weights']
            asset_names = portfolio_data['returns'].index
            
            axes[i].pie(weights, labels=asset_names, autopct='%1.1f%%')
            axes[i].set_title(f'Pesos de {portfolio_name}')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Proyecciones de Valor a Largo Plazo")
        horizons = [3, 5, 10]
        fig, axes = plt.subplots(1, len(horizons), figsize=(15, 5))

        predictions_table = []
        for i, years in enumerate(horizons):
            for portfolio_name, portfolio_data in results.items():
                predictions = portfolio_data['predictions'][years]['predictions']
                initial_value = portfolio_data['predictions'][years]['initial_value']
                final_value = portfolio_data['predictions'][years]['final_value']
                total_return = portfolio_data['predictions'][years]['total_return']

                axes[i].plot(
                    predictions['Day'], 
                    predictions['Portfolio_Value'], 
                    label=f'{portfolio_name} (Final: ${final_value:,.2f})'
                )

                # Collect data for the table
                predictions_table.append({
                    'Portafolio': portfolio_name,
                    'Horizonte (Años)': years,
                    'Valor Inicial': initial_value,
                    'Valor Final': final_value,
                    'Retorno Total (%)': total_return
                })

            axes[i].set_title(f'Proyección a {years} Años')
            axes[i].set_xlabel('Días')
            axes[i].set_ylabel('Valor del Portafolio ($)')
            axes[i].legend()

        plt.tight_layout()
        st.pyplot(fig)

        # Display predictions table
        predictions_df = pd.DataFrame(predictions_table)
        st.subheader("Resumen de Proyecciones")
        st.dataframe(predictions_df.style.format({
            'Valor Inicial': '${:,.2f}',
            'Valor Final': '${:,.2f}',
            'Retorno Total (%)': '{:.2f}%'
        }))
        summary_data = []
        for years in horizons:
            total_final_value = predictions_df.loc[
                predictions_df['Horizonte (Años)'] == years, 'Valor Final'
            ].sum()
            summary_data.append({
                'Horizonte (Años)': years,
                'Suma Total de Valor Final': total_final_value
            })

        # Crear un DataFrame con los valores totales
        summary_df = pd.DataFrame(summary_data)

        # Mostrar la tabla resumen
        st.subheader("Resumen Total de Valores Finales por Horizonte")
        st.dataframe(summary_df.style.format({
            'Suma Total de Valor Final': '${:,.2f}'
        }))
        
    with tab4:
        st.subheader("Comparación de Rendimiento y Riesgo")
        performance_data = []
        for portfolio_name, portfolio_data in results.items():
            performance = portfolio_data['performance']
            performance_data.append({
                'Portafolio': portfolio_name,
                'Rendimiento Anual (%)': performance['return'] * 100,
                'Volatilidad Anual (%)': performance['volatility'] * 100,
                'Ratio Sharpe': performance['sharpe_ratio']
            })

        performance_df = pd.DataFrame(performance_data)
        
        # Verificar y convertir columnas
        performance_df['Rendimiento Anual (%)'] = pd.to_numeric(performance_df['Rendimiento Anual (%)'], errors='coerce')
        performance_df['Volatilidad Anual (%)'] = pd.to_numeric(performance_df['Volatilidad Anual (%)'], errors='coerce')
        performance_df['Ratio Sharpe'] = pd.to_numeric(performance_df['Ratio Sharpe'], errors='coerce')
        performance_df = performance_df.fillna(0)  # Manejar NaN si los hubiera

        # Mostrar en Streamlit
        st.dataframe(performance_df.style.format({
            'Rendimiento Anual (%)': '{:.2f}%',
            'Volatilidad Anual (%)': '{:.2f}%',
            'Ratio Sharpe': '{:.2f}'
        }))
        
        
    

# Portada
if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
     # Centrar el botón usando columnas
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2: 
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.image(image_path, caption="", use_container_width=False, width=180)
        st.markdown("""
        <div style="text-align: center; padding: 1px;">
            <h1 style="font-size: 42px; font-weight: bold;">Perfil de Riesgo de Inversión</h1>
        </div>   
        <div style="text-align: left; padding: 15px;">
            <p style="font-size: 18px; line-height: 1.6; margin-top: 20px;">
                <strong>¿Qué es el Perfil de Riesgo?</strong><br>
                El perfil de riesgo del inversionista nos ayuda a determinar qué estrategia de inversión 
                se adapta mejor a tus características personales y objetivos financieros.
            </p>
            <p style="font-size: 18px; line-height: 1.6; margin-top: 20px;">
                <strong>¿Qué evaluamos?</strong><br>
                Este cuestionario analiza tres aspectos clave:
            </p>
            <ol style="font-size: 18px; line-height: 1.6; text-align: left; display: inline-block;">
                <li><strong>Necesidad de Riesgo</strong>: Tus objetivos financieros y horizonte temporal</li>
                <li><strong>Capacidad de Riesgo</strong>: Tu situación financiera actual</li>
                <li><strong>Tolerancia al Riesgo</strong>: Tu actitud personal frente a las fluctuaciones del mercado</li>
            </ol>
            <p style="font-size: 18px; margin-top: 20px;">Tiempo estimado: 5-10 minutos</p>
        </div>
        """, unsafe_allow_html=True)
    

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Espacio antes del botón
        if st.button("Comenzar Cuestionario", key="start_button", use_container_width=True):
            st.session_state.started = True

# Si ya comenzó el cuestionario, mostrar el contenido original
elif st.session_state.started:
    # Título de la aplicación
    if st.session_state.section < 4:
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:   
            st.title("Cuestionario de Perfil de Riesgo de Inversión")

        # Indicador de progreso
            if st.session_state.section < 4:
                progress = (st.session_state.section - 1) / 3
                st.progress(progress)
                st.write(f"Sección {st.session_state.section} de 3")

    # Sección 1
    if st.session_state.section == 1:
        col1, col2, col3 = st.columns(3)
        
        with col2:          
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
        col1, col2, col3 = st.columns(3)
        
        with col2:          
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
        
        col1, col2, col3 = st.columns(3)
        
        with col2:  
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
        
        st.metric("Puntuación Total", f"{total_score} pts")
        
        # Botón para reiniciar
        st.markdown("---")
        if st.button("Realizar nuevo cuestionario", key="btn_reinicio"):
            reiniciar_cuestionario()


        if st.button("Generar Análisis de Portafolio Detallado", key="btn_portfolio_analysis"):
            # Determine portfolio allocation based on risk profile
            if perfil == "Conservador":
                portfolio_allocation = {
                    "Bonos": 0.8,
                    "ETFs": 0.2,
                    "Acciones": 0,
                    "Futuros": 0,
                    "Criptomonedas": 0
                }
            elif perfil == "Moderado":
                portfolio_allocation = {
                    "Bonos": 0.4,
                    "ETFs": 0.4,
                    "Acciones": 0.2,
                    "Futuros": 0,
                    "Criptomonedas": 0
                }
            elif perfil == "Agresivo":
                portfolio_allocation = {
                    "Bonos": 0.1,
                    "ETFs": 0.3,
                    "Acciones": 0.5,
                    "Futuros": 0.1,
                    "Criptomonedas": 0
                }
            else:  # Muy Agresivo
                portfolio_allocation = {
                    "Bonos": 0,
                    "ETFs": 0.0,
                    "Acciones": 0.6,
                    "Futuros": 0.2,
                    "Criptomonedas": 0.2
                }
            
            # Run portfolio analysis
            with st.spinner('Generando análisis de portafolio...'):
                portfolio_results = run_portfolio_analysis(portfolio_allocation)
            
            # Display results
            display_portfolio_results(portfolio_results)