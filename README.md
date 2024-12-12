# C22-36-n-data-bi

# <h1 align= 'center'>Proyecto sobre Tendencias de Inversión- Smartreade</h1>
<p align = center>
  <img src= 'assets/logo2.png' width= 100% >
</p>

![Markdown](https://img.shields.io/badge/-Markdown-black?style=flat-square&logo=markdown)
![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=python)
![Numpy](https://img.shields.io/badge/-Numpy-black?style=flat-square&logo=numpy)
![Pandas](https://img.shields.io/badge/-Pandas-black?style=flat-square&logo=pandas)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-black?style=flat-square&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-black?style=flat-square&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-black?style=flat&logo=scikitlearn)
![Power BI](https://img.shields.io/badge/-Power%20BI-black?style=flat-square&logo=powerbi)
![Power Query](https://img.shields.io/badge/-Power%20Query-black?style=flat-square&logo=powerquery)
![Microsoft Excel](https://img.shields.io/badge/-Microsoft%20Excel-black?style=flat-square&logo=excel)
![Git](https://img.shields.io/badge/-Git-black?style=flat-square&logo=git)
![GitHub](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github)
![Google Drive](https://img.shields.io/badge/-Google%20Drive-black?style=flat-square&logo=googledrive)
![Google Colaboratory](https://img.shields.io/badge/-Google%20Colaboratory-black?style=flat-square&logo=googlecolaboratory)
![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-black?style=flat&logo=visual-studio-code&logoColor=007ACC)

# Producto

- [Presentación del Producto]()
- [Documentación Completa del Desarrollo del Proyecto]()

# Índice

- [Introducción](#Introducción)
- [Objetivos](#Objetivos)
- [Datos](#Datos)
- [Desarrollo](#Desarrollo)
  - [ETL](#ETL)
  - [EDA](#EDA)
  - [Dashboard](#Dashboard)
  - [Modelo](#Modelo)
  - [Deploy](#Deploy)
- [Tecnologías](#Tecnologías)
- [Conclusiones](#Conclusiones)
- [Equipo](#Equipo)

# Introducción

Nuestro cliente el Banco de Inversión Latinoamericano (BILA) quiere resolver la falta de herramientas accesibles para que sus clientes puedan identificar su perfil de riesgo y tomar decisiones de inversión informadas y personalizadas. Actualmente, muchas personas tienen dificultades para entender cuánto riesgo están dispuestas a asumir y cómo podrían crecer sus inversiones bajo diferentes escenarios de mercado. Esto resulta en inversiones mal ajustadas al perfil de riesgo, baja satisfacción y resultados financieros inesperados.

# Objetivos

Desarrollar una solución que permita a los clientes de BILA recibir asesoría personalizada en sus inversiones, en función de su perfil de riesgo, optimizando el portafolio de inversión  y proporcionando proyecciones de rendimiento para aumentar la satisfacción, retención y fidelización de los clientes.

Para ello debemos proporcionar:

* Un marco de análisis el cual será conformado por un análisis de la
### **Objetivos Específicos**

- **1. Identificar y clasificar el perfil de riesgo de cada cliente** mediante un cuestionario que permita definir su tolerancia al riesgo y horizonte de inversión, categorizándolo en un perfil adecuado (conservador, moderado, agresivo).
- **2. Proporcionar recomendaciones personalizadas de distribución de activos** (bonos, ETFs, acciones, criptomonedas, etc) según el perfil de riesgo de cada cliente, optimizando la asignación de acuerdo con sus preferencias y objetivos financieros.
- **3. Desarrollar proyecciones de rendimiento en diferentes escenarios de mercado**  para que el cliente visualice el posible crecimiento de su inversión y tome decisiones informadas.

# Datos
El proyecto utiliza datos financieros históricos para analizar y optimizar portafolios de inversión. Estos datos son extraídos de fuentes confiables a través de la API de Yahoo Finance utilizando la librería yfinance.

### Fuente de Datos
* Proveedor: Yahoo Finance
* Contenido: Precios históricos de cierre para activos financieros como:
*   Acciones: Microsoft (MSFT), Apple (AAPL), Google (GOOGL), entre otros.
*   Bonos: Índices como ^IRX, ^FVX.
*   ETFs: SPY, QQQ, VTI, entre otros.
*   Futuros: Oro (GC=F), Petróleo (CL=F).
*   Criptomonedas: Bitcoin (BTC-USD), Ethereum (ETH-USD).
### Descripción del Dataset
Rango temporal:
Los datos abarcan desde el 9 de noviembre de 2017 hasta el 31 de octubre de 2024 (configurable).
### Variables principales:
* Close: Precio de cierre diario para cada activo.
* Fecha: Índice temporal de los precios.
# Desarrollo
## ETL
### Extracción de Datos
Utilizando la librería yfinance, se obtienen datos históricos de precios de cierre de una lista de activos financieros para un rango de fechas definido. Esto asegura que los datos sean precisos y estén actualizados.

* Método: download_data(assets: List[str])
* Entrada: Lista de activos financieros (por ejemplo, ["MSFT", "AAPL"]).
* Salida: DataFrame consolidado con precios de cierre para cada activo.
### Transformación de Datos
Los datos extraídos se transforman para mantener únicamente las columnas relevantes (por ejemplo, los precios de cierre). Se renombran las columnas con los nombres de los activos para facilitar su análisis posterior.

### Procesamiento de Portafolios
La función process_portfolios(portfolios: Dict[str, List[str]]) organiza los datos en portafolios categorizados por tipo de activo (acciones, bonos, ETFs, etc.).

* Entrada: Un diccionario donde las claves son los nombres de los portafolios (por ejemplo, "Bonos") y los valores son listas de activos correspondientes.
* Salida: Un diccionario donde cada clave contiene un DataFrame con los datos históricos de los activos de ese portafolio.
## EDA
## Dashboard
<table>
  <tr>
    <td >
      <img src='assets/dash1.png' width="600" height="400">
    </td>
    <td >
      <img src='assets/dash2.png' width="600" height="400">
    </td>
      <tr>
    <td >
      <img src='assets/dash3.png' width="600" height="400">
    </td>
  </tr>

  </tr>
</table>


## Modelo
### Modelo: Random Forest Regressor
El modelo Random Forest Regressor es una técnica de ensamble basada en árboles de decisión que combina múltiples modelos débiles para mejorar la precisión y reducir el sobreajuste. Este modelo es particularmente adecuado para predicciones financieras, dado su capacidad para manejar relaciones no lineales y datos heterogéneos.

### Implementación:
Se inicializa el modelo con los siguientes parámetros:
  from sklearn.ensemble import RandomForestRegressor
  self.model = RandomForestRegressor(
      n_estimators=100,  # Número de árboles en el bosque
      random_state=42    # Semilla para reproducibilidad
  )

### Características del modelo:
* Número de estimadores (n_estimators): 100 árboles para garantizar un balance entre precisión y tiempo de entrenamiento.
* Estado aleatorio (random_state): Fijado para garantizar resultados reproducibles.
## Deploy

# Tecnologías
El proyecto utiliza las siguientes herramientas y librerías:

* Python para el desarrollo general.
* Streamlit para crear la interfaz interactiva.
* YFinance para obtener datos históricos de activos.
* Pandas y Numpy para manipulación y análisis de datos.
* Matplotlib y Seaborn para visualización de datos.
* Scikit-learn para predicciones basadas en modelos de machine learning.
# Resultados

  <img src='assets/vista1app.png' width="80%" >
   <img src='assets/vista2app.png' width="80%" >
     <img src='assets/vista3app.png' width="80%" >
       <img src='assets/vista4app.png' width="80%" >
         <img src='assets/vista5app.png' width="80%" > 

# Equipo

<div align="center">

<!-- Primera fila -->
<table>
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/12752331?v=4" width="200" height="200"><br><strong>Manuel</strong><br>
      <a href="https://www.linkedin.com/in/manuel-carruitero-b8b50688/"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/mcarruitero"><img src="assets/github.png" style="width:20px;"></a>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/56092179?s=400&u=9dea3de0613e5ee359f0e7f38babdadf71fff133&v=4" width="200" height="200"><br><strong>José</strong><br>
      <a href="https://www.linkedin.com/in/joselo-ardiles-ugaz/"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/JoseloArdiles"><img src="assets/github.png" style="width:20px;"></a>
    </td>
      <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/152358919?s=400&u=360b4d22b4075bad0278c7826c792b4c6684afe2&v=4" width="200" height="200"><br><strong>Mario</strong><br>
      <a href="https://www.linkedin.com/in/mario-hernández-/"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/mao-bio"><img src="assets/github.png" style="width:20px;"></a>
    </td>
  </tr>

  </tr>
</table>

</div>
