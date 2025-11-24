import json
from pathlib import Path

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/LSTM.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell = nb['cells'][25]
print("".join(cell['source']))
