import json
from pathlib import Path

notebook_path = Path(r"c:/Users/josep/OneDrive/Desktop/PUCP/2025-2/Tesis2/Resultados esperados/RESULTADO 3/Modelo/-1INF46-Plan_Compras_Produccion/notebooks/tuning/LSTM.ipynb")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell = nb['cells'][25]
source = cell['source']

already_added = False
for line in source:
    if "lstm_metrics.csv" in line:
        already_added = True
        break

if not already_added:
    new_code = [
        "\n",
        "# Save metrics to CSV\n",
        "output_dir = Path(\"../../reports/metrics\")\n",
        "output_dir.mkdir(parents=True, exist_ok=True)\n",
        "lstm_segment_metrics_df.to_csv(output_dir / \"lstm_metrics.csv\")\n",
        "print(f\"Metrics saved to {output_dir / 'lstm_metrics.csv'}\")\n"
    ]
    cell['source'].extend(new_code)
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("LSTM.ipynb modified.")
else:
    print("LSTM.ipynb already has save code.")
