import streamlit as st

# Título de la aplicación
st.title("¡Hola, Streamlit!")

# Texto
st.write("Esta es tu primera aplicación con Streamlit. 🎉")

# Input de usuario
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.write(f"¡Hola, {nombre}!")

# Gráfico sencillo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Datos aleatorios
data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["A", "B", "C"]
)

st.line_chart(data)
