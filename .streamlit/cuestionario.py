import streamlit as st

# Definir las preguntas y opciones
preguntas = {
    "Sección 1: Necesidad de Riesgo": [
        {
            "pregunta": "¿Cuál es el objetivo principal de su inversión?",
            "opciones": ["Preservar el capital", "Generar ingresos estables", "Aumentar el valor de su capital moderadamente", "Maximizar el crecimiento de su capital"],
            "puntos": [1, 2, 3, 4]
        },
        {
            "pregunta": "¿Cuánto tiempo planea mantener su inversión?",
            "opciones": ["Menos de 3 años", "Entre 3 y 5 años", "Entre 5 y 10 años", "Más de 10 años"],
            "puntos": [1, 2, 3, 4]
        },
        {
            "pregunta": "¿Qué tasa de retorno esperada necesita para alcanzar sus metas financieras?",
            "opciones": ["Menos del 4% anual", "Entre el 4% y el 6% anual", "Entre el 6% y el 10% anual", "Más del 10% anual"],
            "puntos": [1, 2, 3, 4]
        }
    ],
    "Sección 2: Capacidad para Asumir Riesgos": [
        {
            "pregunta": "¿Cuál es su nivel de ingresos o ahorros adicionales que no dependen de esta inversión?",
            "opciones": ["Muy bajo", "Bajo", "Moderado", "Alto"],
            "puntos": [1, 2, 3, 4]
        },
        {
            "pregunta": "¿Qué tan importantes son las distribuciones regulares (liquidez) de esta inversión para usted?",
            "opciones": ["Críticas", "Moderadamente importantes", "Poco importantes", "No son importantes"],
            "puntos": [1, 2, 3, 4]
        },
        {
            "pregunta": "Si su cartera perdiera el 20% de su valor, ¿cómo afectaría esto su situación financiera?",
            "opciones": ["Sería catastrófico", "Sería un inconveniente significativo", "Podría manejarlo sin problemas graves", "No tendría impacto significativo"],
            "puntos": [1, 2, 3, 4]
        }
    ],
    "Sección 3: Tolerancia Conductual al Riesgo": [
        {
            "pregunta": "¿Qué tan cómodo se siente al aceptar fluctuaciones en el valor de su inversión?",
            "opciones": ["Muy incómodo", "Incómodo", "Moderadamente cómodo", "Muy cómodo"],
            "puntos": [1, 2, 3, 4]
        },
        {
            "pregunta": "¿Qué haría si su inversión perdiera el 30% de su valor en el corto plazo?",
            "opciones": ["Vendería inmediatamente para evitar más pérdidas", "Esperaría a que los mercados se recuperen", "Invertiría más para aprovechar los precios bajos"],
            "puntos": [1, 3, 5]
        },
        {
            "pregunta": "¿Qué tan familiarizado está con los conceptos y productos financieros?",
            "opciones": ["Nada familiarizado", "Algo familiarizado", "Moderadamente informado", "Muy informado"],
            "puntos": [1, 2, 3, 4]
        }
    ]
}

# Configurar la app de Streamlit
st.title("Cuestionario de Perfil de Riesgo")

total_puntos = 0

# Mostrar preguntas y calcular puntos
for seccion, preguntas_seccion in preguntas.items():
    st.header(seccion)
    for pregunta in preguntas_seccion:
        respuesta = st.radio(pregunta["pregunta"], pregunta["opciones"], key=pregunta["pregunta"])
        total_puntos += pregunta["puntos"][pregunta["opciones"].index(respuesta)]

# Evaluar el perfil y asignar portafolio
st.subheader("Resultado")
if total_puntos <= 18:
    perfil = "Conservador"
    portafolio = "80% Bonos, 20% ETFs"
elif 19 <= total_puntos <= 27:
    perfil = "Moderado"
    portafolio = "40% Bonos, 40% ETFs, 20% Acciones"
elif 28 <= total_puntos <= 36:
    perfil = "Agresivo"
    portafolio = "10% Bonos, 30% ETFs, 50% Acciones, 10% Futuros"
else:
    perfil = "Muy Agresivo"
    portafolio = "60% Acciones, 20% Futuros, 20% Criptomonedas"

st.write(f"**Perfil de Riesgo:** {perfil}")
st.write(f"**Portafolio sugerido:** {portafolio}")

# Ordenar activos por nivel de riesgo
st.subheader("Nivel de Riesgo de los Activos")
riesgos = {
    "Bonos": "Bajo",
    "ETFs": "Medio-Bajo",
    "Acciones": "Medio",
    "Futuros": "Alto",
    "Criptomonedas": "Muy Alto"
}

for activo, riesgo in sorted(riesgos.items(), key=lambda x: x[1]):
    st.write(f"- **{activo}**: {riesgo}")
