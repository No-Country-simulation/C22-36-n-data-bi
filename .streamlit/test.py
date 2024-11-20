import streamlit as st

# Título de la aplicación
st.title("Cuestionario Simplificado de Perfil de Riesgo de Inversión")

# Inicialización de variables de estado
if 'section' not in st.session_state:
    st.session_state.section = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Función para calcular el perfil de riesgo
def calcular_perfil(total_score):
    if total_score <= 2:
        return "Conservador", "80% Bonos, 20% ETFs"
    elif total_score == 3:
        return "Moderado", "40% Bonos, 40% ETFs, 20% Acciones"
    else:
        return "Agresivo", "20% Bonos, 40% Acciones, 40% Criptomonedas"

# Función para reiniciar el cuestionario
def reiniciar_cuestionario():
    st.session_state.section = 1
    st.session_state.score = 0
    st.session_state.show_results = False
    st.rerun()

# Sección 1
if st.session_state.section == 1:
    st.subheader("Sección 1: Necesidad de Riesgo")
    q1 = st.radio(
        "¿Cuál es tu principal objetivo de inversión?", 
        ["Preservar el capital", "Aumentar moderadamente", "Maximizar el crecimiento"],
        key="q1"
    )
    if st.button("Siguiente"):
        st.session_state.score += [1, 2, 3][["Preservar el capital", "Aumentar moderadamente", "Maximizar el crecimiento"].index(q1)]
        st.session_state.section += 1
        st.rerun()

# Sección 2
elif st.session_state.section == 2:
    st.subheader("Sección 2: Capacidad para Asumir Riesgo")
    q2 = st.radio(
        "¿Qué harías si tu inversión perdiera el 20% de su valor?", 
        ["Vendería inmediatamente", "Esperaría a que se recupere", "Invertiría más"],
        key="q2"
    )
    if st.button("Siguiente"):
        st.session_state.score += [1, 2, 3][["Vendería inmediatamente", "Esperaría a que se recupere", "Invertiría más"].index(q2)]
        st.session_state.section += 1
        st.rerun()

# Sección 3
elif st.session_state.section == 3:
    st.subheader("Sección 3: Familiaridad Financiera")
    q3 = st.radio(
        "¿Qué tan familiarizado estás con productos financieros?", 
        ["Nada", "Algo", "Muy familiarizado"],
        key="q3"
    )
    if st.button("Descubrir mi perfil"):
        st.session_state.score += [1, 2, 3][["Nada", "Algo", "Muy familiarizado"].index(q3)]
        st.session_state.show_results = True
        st.rerun()

# Mostrar resultados
if st.session_state.show_results:
    perfil, portafolio = calcular_perfil(st.session_state.score)
    st.success(f"Tu perfil de riesgo es: **{perfil}**")
    st.info(f"Estrategia de inversión sugerida: **{portafolio}**")
    if st.button("Reiniciar Cuestionario"):
        reiniciar_cuestionario()
