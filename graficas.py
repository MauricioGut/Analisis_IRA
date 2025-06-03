import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Cargar datos ---
archivo = "informacion-publica-respiratorias-nacional-hasta-20240405.xlsx"
df = pd.read_excel(archivo)

# --- Limpiar datos ---
df["cantidad_casos"] = pd.to_numeric(df["cantidad_casos"], errors="coerce").fillna(0).astype(int)
df = df.dropna(subset=["evento_nombre", "grupo_edad_desc", "provincia_nombre", "año", "semanas_epidemiologicas"])

# --- Crear columna de fecha desde año y semana ---
df["fecha"] = pd.to_datetime(df["año"].astype(str) + "-W" + df["semanas_epidemiologicas"].astype(str) + "-1", format="%Y-W%W-%w", errors="coerce")

# === GRÁFICAS ===

# 1. Casos totales por tipo de evento
plt.figure(figsize=(10,5))
df.groupby("evento_nombre")["cantidad_casos"].sum().sort_values(ascending=False).plot(kind="bar")
plt.title("Casos totales por tipo de evento")
plt.ylabel("Cantidad de casos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Casos totales por grupo etario
plt.figure(figsize=(10,5))
df.groupby("grupo_edad_desc")["cantidad_casos"].sum().sort_values(ascending=False).plot(kind="bar")
plt.title("Casos totales por grupo etario")
plt.ylabel("Cantidad de casos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Series de tiempo por evento
serie_evento = df.groupby(["fecha", "evento_nombre"])["cantidad_casos"].sum().reset_index()
plt.figure(figsize=(12,6))
sns.lineplot(data=serie_evento, x="fecha", y="cantidad_casos", hue="evento_nombre")
plt.title("Evolución semanal por tipo de evento")
plt.ylabel("Casos")
plt.xlabel("Fecha")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Series de tiempo por grupo etario (opcional)
serie_edad = df.groupby(["fecha", "grupo_edad_desc"])["cantidad_casos"].sum().reset_index()
plt.figure(figsize=(12,6))
sns.lineplot(data=serie_edad, x="fecha", y="cantidad_casos", hue="grupo_edad_desc")
plt.title("Evolución semanal por grupo etario")
plt.ylabel("Casos")
plt.xlabel("Fecha")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 5. Dispersión: semana vs. casos
plt.figure(figsize=(10,6))
sns.scatterplot(data=df.sample(3000), x="semanas_epidemiologicas", y="cantidad_casos", alpha=0.3)
plt.title("Dispersión: semana epidemiológica vs cantidad de casos")
plt.xlabel("Semana epidemiológica")
plt.ylabel("Cantidad de casos")
plt.tight_layout()
plt.show()

# 6. Gráfico de barras: Casos por región
region_total = df.groupby('provincia_nombre')['cantidad_casos'].sum().sort_values(ascending=False)
region_total.plot(kind='bar', figsize=(10,5), title='Casos totales por región')
plt.ylabel("Cantidad de casos")
plt.tight_layout()
plt.show()

# 7. Gráfico de torta: porcentaje de casos por grupo etario
grupo_total = df.groupby("grupo_edad_desc")["cantidad_casos"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,8))
plt.pie(grupo_total, labels=grupo_total.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribución porcentual de casos por grupo etario")
plt.axis('equal')
plt.tight_layout()
plt.show()

# 8. Gráfico de barras apiladas: Casos por evento y grupo etario
plt.figure(figsize=(12,6))
df_pivot = df.pivot_table(index="fecha", columns="evento_nombre", values="cantidad_casos", aggfunc="sum").fillna(0)
df_pivot.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title("Casos por evento y grupo etario")
plt.ylabel("Cantidad de casos")
plt.xlabel("Fecha")
plt.xticks(rotation=45)
plt.legend(title='Tipo de Evento', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 9. Gráfico de calor: Casos por semana y grupo etario
plt.figure(figsize=(12,6))
heatmap_data = df.pivot_table(index="semanas_epidemiologicas", columns="grupo_edad_desc", values="cantidad_casos", aggfunc="sum").fillna(0)
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Cantidad de casos'})
plt.title("Calor: Casos por semana y grupo etario")
plt.xlabel("Grupo etario")
plt.ylabel("Semana epidemiológica")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()