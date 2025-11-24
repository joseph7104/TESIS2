import json
from pathlib import Path

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/LSTM.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with model.save(model_path)
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        source_text = "".join(source)
        if "model.save(model_path)" in source_text and 'f"plato_{plato_id}"' in source_text:
            # We found the cell. We need to update the model_path definition.
            new_source = []
            for line in source:
                if 'model_path = lstm_output_dir / f"plato_{plato_id}"' in line:
                    # Replace with .keras extension
                    new_line = line.replace('f"plato_{plato_id}"', 'f"plato_{plato_id}.keras"')
                    new_source.append(new_line)
                    print("Updated model_path definition.")
                else:
                    new_source.append(line)
            cell['source'] = new_source
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
