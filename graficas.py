import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# --- Cargar y preparar los datos ---
archivo = "informacion-publica-respiratorias-nacional-hasta-20240405.xlsx"
df = pd.read_excel(archivo)

# Convertir cantidad_casos a entero
df["cantidad_casos"] = pd.to_numeric(df["cantidad_casos"], errors="coerce").fillna(0).astype(int)

# Filtrar datos válidos
df = df.dropna(subset=["semanas_epidemiologicas", "cantidad_casos"])

# Agrupar por semana epidemiológica (promedia todas las provincias, edades y eventos)
df_reg = df.groupby("semanas_epidemiologicas")["cantidad_casos"].sum().reset_index()

# Variables independientes y dependientes
X = df_reg[["semanas_epidemiologicas"]]
y = df_reg["cantidad_casos"]

# Crear y ajustar modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Predicciones y evaluación
y_pred = modelo.predict(X)
r2 = r2_score(y, y_pred)
pendiente = modelo.coef_[0]
intercepto = modelo.intercept_

# --- Visualización ---
plt.figure(figsize=(10,6))
sns.scatterplot(x=X["semanas_epidemiologicas"], y=y, label="Datos observados", alpha=0.6)
plt.plot(X, y_pred, color="red", label="Regresión lineal")
plt.title("Regresión lineal: Semana epidemiológica vs. cantidad de casos")
plt.xlabel("Semana epidemiológica")
plt.ylabel("Cantidad de casos")
plt.legend()
plt.tight_layout()
plt.show()

# --- Resultados del modelo ---
print("📊 Resultados de la regresión lineal:")
print(f"Intercepto (β₀): {intercepto:.2f}")
print(f"Pendiente (β₁): {pendiente:.2f}")
print(f"Coeficiente de determinación R²: {r2:.3f}")

# Interpretación básica
if pendiente > 0:
    tendencia = "aumentan"
else:
    tendencia = "disminuyen"
print(f"\nInterpretación: Por cada semana que avanza, los casos tienden a {tendencia} en promedio.")
