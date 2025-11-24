import json
from pathlib import Path
import re

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/RF_TUNING.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("=== START OF NOTEBOOK ANALYSIS ===\n")

for i, cell in enumerate(nb['cells']):
    # Print Markdown content to understand the "Why"
    if cell['cell_type'] == 'markdown':
        source = "".join(cell['source']).strip()
        if source:
            print(f"--- Markdown (Cell {i}) ---")
            print(source)
            print("\n")
    
    # Print Code outputs if they contain metrics, to understand the "Result"
    elif cell['cell_type'] == 'code':
        # Check outputs
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'text' in output:
                    text = "".join(output['text'])
                    # Filter for relevant metrics keywords
                    if any(x in text for x in ["Accuracy", "MAE", "RMSE", "Global", "Métrica"]):
                        print(f"--- Output (Cell {i}) ---")
                        print(text)
                        print("\n")
                elif 'data' in output and 'text/plain' in output['data']:
                     text = "".join(output['data']['text/plain'])
                     if any(x in text for x in ["Accuracy", "MAE", "RMSE", "Global", "Métrica"]):
                        print(f"--- Output (Cell {i}) ---")
                        print(text)
                        print("\n")

print("=== END OF NOTEBOOK ANALYSIS ===")
