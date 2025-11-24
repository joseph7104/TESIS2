import json
from pathlib import Path

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Comparación de Modelos: XGBoost vs Random Forest vs LSTM\n",
    "\n",
    "Este notebook compara las métricas de desempeño de los tres modelos entrenados por segmento (plato).\n",
    "\n",
    "**Modelos:**\n",
    "1. **XGBoost**\n",
    "2. **Random Forest**\n",
    "3. **LSTM**\n",
    "\n",
    "**Métricas:**\n",
    "- MAE (Mean Absolute Error)\n",
    "- RMSE (Root Mean Squared Error)\n",
    "- sMAPE (Symmetric Mean Absolute Percentage Error)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from pathlib import Path\n",
    "\n",
    "# Configuración de estilo\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "plt.rcParams[\"figure.figsize\"] = (12, 6)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Rutas de los archivos de métricas\n",
    "METRICS_DIR = Path(\"../../reports/metrics\")\n",
    "\n",
    "xgb_path = METRICS_DIR / \"xgboost_metrics.csv\"\n",
    "rf_path = METRICS_DIR / \"rf_metrics.csv\"\n",
    "lstm_path = METRICS_DIR / \"lstm_metrics.csv\"\n",
    "\n",
    "# Cargar datos\n",
    "try:\n",
    "    df_xgb = pd.read_csv(xgb_path)\n",
    "    df_rf = pd.read_csv(rf_path)\n",
    "    df_lstm = pd.read_csv(lstm_path)\n",
    "    print(\"Métricas cargadas correctamente.\")\n",
    "except FileNotFoundError as e:\n",
    "    print(f\"Error: No se encontró el archivo {e.filename}. Asegúrate de haber ejecutado los notebooks de entrenamiento.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Estandarización de columnas\n",
    "# XGBoost y RF tienen 'segmento', LSTM tiene 'plato' (o index)\n",
    "\n",
    "if 'plato' in df_lstm.columns:\n",
    "    df_lstm = df_lstm.rename(columns={'plato': 'segmento'})\n",
    "\n",
    "# Asegurar que todos tengan 'segmento'\n",
    "df_xgb['Modelo'] = 'XGBoost'\n",
    "df_rf['Modelo'] = 'Random Forest'\n",
    "df_lstm['Modelo'] = 'LSTM'\n",
    "\n",
    "# Seleccionar columnas relevantes\n",
    "cols = ['segmento', 'MAE', 'RMSE', 'sMAPE', 'Modelo']\n",
    "\n",
    "df_all = pd.concat([\n",
    "    df_xgb[cols],\n",
    "    df_rf[cols],\n",
    "    df_lstm[cols]\n",
    "], ignore_index=True)\n",
    "\n",
    "df_all.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Comparación Global (Promedio por Modelo)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "global_metrics = df_all.groupby('Modelo')[['MAE', 'RMSE', 'sMAPE']].mean().reset_index()\n",
    "display(global_metrics)\n",
    "\n",
    "# Gráfico de barras global\n",
    "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
    "\n",
    "sns.barplot(data=global_metrics, x='Modelo', y='MAE', ax=axes[0], palette='viridis')\n",
    "axes[0].set_title('MAE Promedio Global (Menor es mejor)')\n",
    "\n",
    "sns.barplot(data=global_metrics, x='Modelo', y='RMSE', ax=axes[1], palette='viridis')\n",
    "axes[1].set_title('RMSE Promedio Global (Menor es mejor)')\n",
    "\n",
    "sns.barplot(data=global_metrics, x='Modelo', y='sMAPE', ax=axes[2], palette='viridis')\n",
    "axes[2].set_title('sMAPE Promedio Global (Menor es mejor)')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Comparación por Segmento (Plato)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gráfico de barras agrupado por segmento para MAE\n",
    "plt.figure(figsize=(15, 8))\n",
    "sns.barplot(data=df_all, x='segmento', y='MAE', hue='Modelo', palette='viridis')\n",
    "plt.title('Comparación de MAE por Plato')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gráfico de barras agrupado por segmento para sMAPE\n",
    "plt.figure(figsize=(15, 8))\n",
    "sns.barplot(data=df_all, x='segmento', y='sMAPE', hue='Modelo', palette='viridis')\n",
    "plt.title('Comparación de sMAPE por Plato')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Tabla Resumen - Mejor Modelo por Segmento"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Encontrar el mejor modelo para cada segmento (basado en MAE)\n",
    "best_models = df_all.loc[df_all.groupby('segmento')['MAE'].idxmin()]\n",
    "best_models = best_models[['segmento', 'Modelo', 'MAE', 'sMAPE']].sort_values('MAE')\n",
    "\n",
    "print(\"Mejor modelo por segmento (Criterio: Menor MAE):\")\n",
    "display(best_models)\n",
    "\n",
    "# Conteo de victorias\n",
    "wins = best_models['Modelo'].value_counts()\n",
    "print(\"\\nConteo de 'Victorias' por Modelo:\")\n",
    "print(wins)\n",
    "\n",
    "plt.figure(figsize=(6, 6))\n",
    "plt.pie(wins, labels=wins.index, autopct='%1.1f%%', colors=sns.color_palette('viridis', len(wins)))\n",
    "plt.title('Distribución de Mejores Modelos')\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

output_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/Comparison.ipynb")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1, ensure_ascii=False)

print(f"Notebook created at {output_path}")
