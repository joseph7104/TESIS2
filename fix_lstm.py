import json
from pathlib import Path

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/LSTM.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Fix CANDIDATE_PATHS
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        source_text = "".join(source)
        if "CANDIDATE_PATHS = [" in source_text:
            new_line = '    Path("../../data/processed/dataset_forecast_diario.csv"),\n'
            # Check if already present
            if new_line not in source:
                # Find insertion point
                idx = -1
                for i, line in enumerate(source):
                    if 'Path("data/processed/dataset_forecast_diario.csv")' in line:
                        idx = i
                        break
                if idx != -1:
                    source.insert(idx, new_line)
                    print("Path inserted.")

# 2. Comment out Colab git clone cell
# Looking for cell with !git clone
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        source_text = "".join(source)
        if "!git clone" in source_text and "joseph7104" in source_text:
            new_source = ["# " + line if not line.startswith("#") else line for line in source]
            cell['source'] = new_source
            print("Git clone cell commented out.")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
