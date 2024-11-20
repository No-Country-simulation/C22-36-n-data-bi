import streamlit as st

# Título de la aplicación
st.title("Ingresar Monto de Inversión")

# Recuperar el perfil y estrategia del cuestionario anterior
perfil = st.session_state.get("perfil", "No definido")
estrategia = st.session_state.get("estrategia", "No definida")

# Mostrar los resultados del perfil
st.subheader("Resumen de tu Perfil de Riesgo")
st.info(f"**Perfil:** {perfil}")
st.success(f"**Estrategia de Inversión Sugerida:** {estrategia}")

# Selección del tipo de inversión
st.markdown("---")
st.subheader("Configura tu inversión")
tipo_inversion = st.radio(
    "Selecciona el tipo de inversión:",
    ["Inversión Mensual", "Inversión Anual", "Inversión Única"],
    key="tipo_inversion"
)

# Ingreso del monto según el tipo seleccionado
if tipo_inversion == "Inversión Mensual":
    monto = st.number_input("Monto de inversión mensual (en tu moneda local):", min_value=0.0, step=100.0, key="monto_mensual")
elif tipo_inversion == "Inversión Anual":
    monto = st.number_input("Monto de inversión anual (en tu moneda local):", min_value=0.0, step=1000.0, key="monto_anual")
else:
    monto = st.number_input("Monto de inversión única (en tu moneda local):", min_value=0.0, step=1000.0, key="monto_unico")

# Botones para guardar o regresar
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("Guardar Inversión", key="guardar_inversion"):
        st.success("Inversión registrada con éxito.")
        st.session_state["monto_inversion"] = monto
        st.session_state["tipo_inversion"] = tipo_inversion

with col2:
    if st.button("Volver al Cuestionario", key="volver_cuestionario"):
        st.session_state.section = 1
        st.experimental_rerun()
